from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Optional

from frostfs_testlib.hosting.config import CLIConfig, HostConfig, ServiceConfig
from frostfs_testlib.shell.interfaces import Shell


class DiskInfo(dict):
    """Dict wrapper for disk_info for disk management commands."""


class Host(ABC):
    """Interface of a host machine where neoFS services are running.

    Allows to manage the machine and neoFS services that are hosted on it.
    """

    def __init__(self, config: HostConfig) -> None:
        self._config = config
        self._service_config_by_name = {
            service_config.name: service_config for service_config in config.services
        }
        self._cli_config_by_name = {cli_config.name: cli_config for cli_config in config.clis}

    @property
    def config(self) -> HostConfig:
        """Returns config of the host.

        Returns:
            Config of this host.
        """
        return self._config

    def get_service_config(self, service_name: str) -> ServiceConfig:
        """Returns config of service with specified name.

        The service must be hosted on this host.

        Args:
            service_name: Name of the service.

        Returns:
            Config of the service.
        """
        service_config = self._service_config_by_name.get(service_name)
        if service_config is None:
            raise ValueError(f"Unknown service name: '{service_name}'")
        return service_config

    def get_cli_config(self, cli_name: str) -> CLIConfig:
        """Returns config of CLI tool with specified name.

        The CLI must be located on this host.

        Args:
            cli_name: Name of the CLI tool.

        Returns:
            Config of the CLI tool.
        """
        cli_config = self._cli_config_by_name.get(cli_name)
        if cli_config is None:
            raise ValueError(f"Unknown CLI name: '{cli_name}'")
        return cli_config

    @abstractmethod
    def get_shell(self) -> Shell:
        """Returns shell to this host.

        Returns:
            Shell that executes commands on this host.
        """

    @abstractmethod
    def start_host(self) -> None:
        """Starts the host machine."""

    @abstractmethod
    def stop_host(self, mode: str) -> None:
        """Stops the host machine.

        Args:
            mode: Specifies mode how host should be stopped. Mode might be host-specific.
        """

    @abstractmethod
    def start_service(self, service_name: str) -> None:
        """Starts the service with specified name and waits until it starts.

        The service must be hosted on this host.

        Args:
            service_name: Name of the service to start.
        """

    @abstractmethod
    def stop_service(self, service_name: str) -> None:
        """Stops the service with specified name and waits until it stops.

        The service must be hosted on this host.

        Args:
            service_name: Name of the service to stop.
        """

    @abstractmethod
    def restart_service(self, service_name: str) -> None:
        """Restarts the service with specified name and waits until it starts.
        The service must be hosted on this host.
        Args:
            service_name: Name of the service to restart.
        """

    @abstractmethod
    def delete_storage_node_data(self, service_name: str, cache_only: bool = False) -> None:
        """Erases all data of the storage node with specified name.

        Args:
            service_name: Name of storage node service.
            cache_only: To delete cache only.
        """

    @abstractmethod
    def detach_disk(self, device: str) -> DiskInfo:
        """Detaches disk device to simulate disk offline/failover scenario.

        Args:
            device: Device name to detach.

        Returns:
            internal service disk info related to host plugin (i.e. volume id for cloud devices),
            which may be used to identify or re-attach existing volume back.
        """

    @abstractmethod
    def attach_disk(self, device: str, disk_info: DiskInfo) -> None:
        """Attaches disk device back.

        Args:
            device: Device name to attach.
            service_info: any info required for host plugin to identify/attach disk.
        """

    @abstractmethod
    def is_disk_attached(self, device: str, disk_info: DiskInfo) -> bool:
        """Checks if disk device is attached.

        Args:
            device: Device name to check.
            service_info: any info required for host plugin to identify disk.

        Returns:
            True if attached.
            False if detached.
        """

    @abstractmethod
    def dump_logs(
        self,
        directory_path: str,
        since: Optional[datetime] = None,
        until: Optional[datetime] = None,
        filter_regex: Optional[str] = None,
    ) -> None:
        """Dumps logs of all services on the host to specified directory.

        Args:
            directory_path: Path to the directory where logs should be stored.
            since: If set, limits the time from which logs should be collected. Must be in UTC.
            until: If set, limits the time until which logs should be collected. Must be in UTC.
            filter_regex: regex to filter output
        """

    @abstractmethod
    def is_message_in_logs(
        self,
        message_regex: str,
        since: Optional[datetime] = None,
        until: Optional[datetime] = None,
    ) -> bool:
        """Checks logs on host for specified message regex.

        Args:
            message_regex: message to find.
            since: If set, limits the time from which logs should be collected. Must be in UTC.
            until: If set, limits the time until which logs should be collected. Must be in UTC.

        Returns:
            True if message found in logs in the given time frame.
            False otherwise.
        """
