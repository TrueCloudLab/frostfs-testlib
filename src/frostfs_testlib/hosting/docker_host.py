import json
import logging
import os
import re
import time
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional

import docker
from requests import HTTPError

from frostfs_testlib.hosting.config import ParsedAttributes
from frostfs_testlib.hosting.interfaces import Host
from frostfs_testlib.shell import LocalShell, Shell, SSHShell
from frostfs_testlib.shell.command_inspectors import SudoInspector

logger = logging.getLogger("frostfs.testlib.hosting")


@dataclass
class HostAttributes(ParsedAttributes):
    """Represents attributes of host where Docker with neoFS runs.

    Attributes:
        sudo_shell: Specifies whether shell commands should be auto-prefixed with sudo.
        docker_endpoint: Protocol, address and port of docker where neoFS runs. Recommended format
            is tcp socket (https://docs.docker.com/engine/reference/commandline/dockerd/#daemon-socket-option),
            for example: tcp://{address}:2375 (where 2375 is default docker port).
        ssh_login: Login for SSH connection to the machine where docker runs.
        ssh_password: Password for SSH connection.
        ssh_private_key_path: Path to private key for SSH connection.
        ssh_private_key_passphrase: Passphrase for the private key.
    """

    sudo_shell: bool = False
    docker_endpoint: Optional[str] = None
    ssh_login: Optional[str] = None
    ssh_password: Optional[str] = None
    ssh_private_key_path: Optional[str] = None
    ssh_private_key_passphrase: Optional[str] = None


@dataclass
class ServiceAttributes(ParsedAttributes):
    """Represents attributes of service running as Docker container.

    Attributes:
        container_name: Name of Docker container where the service runs.
        volume_name: Name of volume where storage node service stores the data.
        start_timeout: Timeout (in seconds) for service to start.
        stop_timeout: Timeout (in seconds) for service to stop.
    """

    container_name: str
    volume_name: Optional[str] = None
    start_timeout: int = 90
    stop_timeout: int = 90


class DockerHost(Host):
    """Manages services hosted in Docker containers running on a local or remote machine."""

    def get_shell(self) -> Shell:
        host_attributes = HostAttributes.parse(self._config.attributes)
        command_inspectors = []
        if host_attributes.sudo_shell:
            command_inspectors.append(SudoInspector())

        if not host_attributes.ssh_login:
            # If there is no SSH connection to the host, use local shell
            return LocalShell(command_inspectors)

        # If there is SSH connection to the host, use SSH shell
        return SSHShell(
            host=self._config.address,
            login=host_attributes.ssh_login,
            password=host_attributes.ssh_password,
            private_key_path=host_attributes.ssh_private_key_path,
            private_key_passphrase=host_attributes.ssh_private_key_passphrase,
            command_inspectors=command_inspectors,
        )

    def start_host(self) -> None:
        # We emulate starting machine by starting all services
        # As an alternative we can probably try to stop docker service...
        for service_config in self._config.services:
            self.start_service(service_config.name)

    def stop_host(self) -> None:
        # We emulate stopping machine by stopping all services
        # As an alternative we can probably try to stop docker service...
        for service_config in self._config.services:
            self.stop_service(service_config.name)

    def start_service(self, service_name: str) -> None:
        service_attributes = self._get_service_attributes(service_name)

        client = self._get_docker_client()
        client.start(service_attributes.container_name)

        self._wait_for_container_to_be_in_state(
            container_name=service_attributes.container_name,
            expected_state="running",
            timeout=service_attributes.start_timeout,
        )

    def stop_service(self, service_name: str) -> None:
        service_attributes = self._get_service_attributes(service_name)

        client = self._get_docker_client()
        client.stop(service_attributes.container_name)

        self._wait_for_container_to_be_in_state(
            container_name=service_attributes.container_name,
            expected_state="exited",
            timeout=service_attributes.stop_timeout,
        )

    def restart_service(self, service_name: str) -> None:
        service_attributes = self._get_service_attributes(service_name)

        client = self._get_docker_client()
        client.restart(service_attributes.container_name)

        self._wait_for_container_to_be_in_state(
            container_name=service_attributes.container_name,
            expected_state="running",
            timeout=service_attributes.start_timeout,
        )

    def delete_storage_node_data(self, service_name: str, cache_only: bool = False) -> None:
        service_attributes = self._get_service_attributes(service_name)

        client = self._get_docker_client()
        volume_info = client.inspect_volume(service_attributes.volume_name)
        volume_path = volume_info["Mountpoint"]

        shell = self.get_shell()
        meta_clean_cmd = f"rm -rf {volume_path}/meta*/*"
        data_clean_cmd = f"; rm -rf {volume_path}/data*/*" if not cache_only else ""
        cmd = f"{meta_clean_cmd}{data_clean_cmd}"
        shell.exec(cmd)

    def dump_logs(
        self,
        directory_path: str,
        since: Optional[datetime] = None,
        until: Optional[datetime] = None,
        filter_regex: Optional[str] = None,
    ) -> None:
        client = self._get_docker_client()
        for service_config in self._config.services:
            container_name = self._get_service_attributes(service_config.name).container_name
            try:
                logs = client.logs(container_name, since=since, until=until)
            except HTTPError as exc:
                logger.info(f"Got exception while dumping logs of '{container_name}': {exc}")
                continue

            if filter_regex:
                logs = (
                    "\n".join(match[0] for match in re.findall(filter_regex, logs, re.IGNORECASE))
                    or f"No matches found in logs based on given filter '{filter_regex}'"
                )

            # Save logs to the directory
            file_path = os.path.join(
                directory_path,
                f"{self._config.address}-{container_name}-log.txt",
            )
            with open(file_path, "wb") as file:
                file.write(logs)

    def is_message_in_logs(
        self,
        message_regex: str,
        since: Optional[datetime] = None,
        until: Optional[datetime] = None,
    ) -> bool:
        client = self._get_docker_client()
        for service_config in self._config.services:
            container_name = self._get_service_attributes(service_config.name).container_name
            try:
                logs = client.logs(container_name, since=since, until=until)
            except HTTPError as exc:
                logger.info(f"Got exception while dumping logs of '{container_name}': {exc}")
                continue

            if message_regex:
                matches = re.findall(message_regex, logs, re.IGNORECASE)
                if matches:
                    return True

        return False

    def _get_service_attributes(self, service_name) -> ServiceAttributes:
        service_config = self.get_service_config(service_name)
        return ServiceAttributes.parse(service_config.attributes)

    def _get_docker_client(self) -> docker.APIClient:
        docker_endpoint = HostAttributes.parse(self._config.attributes).docker_endpoint

        if not docker_endpoint:
            # Use default docker client that talks to unix socket
            return docker.APIClient()

        # Otherwise use docker client that talks to specified endpoint
        return docker.APIClient(base_url=docker_endpoint)

    def _get_container_by_name(self, container_name: str) -> dict[str, Any]:
        client = self._get_docker_client()
        containers = client.containers(all=True)

        for container in containers:
            # Names in local docker environment are prefixed with /
            clean_names = set(name.strip("/") for name in container["Names"])
            if container_name in clean_names:
                return container
        return None

    def _wait_for_container_to_be_in_state(
        self, container_name: str, expected_state: str, timeout: int
    ) -> None:
        iterations = 10
        iteration_wait_time = timeout / iterations

        # To speed things up, we break timeout in smaller iterations and check container state
        # several times. This way waiting stops as soon as container reaches the expected state
        for _ in range(iterations):
            container = self._get_container_by_name(container_name)
            logger.debug(f"Current container state\n:{json.dumps(container, indent=2)}")

            if container and container["State"] == expected_state:
                return
            time.sleep(iteration_wait_time)

        raise RuntimeError(f"Container {container_name} is not in {expected_state} state.")
