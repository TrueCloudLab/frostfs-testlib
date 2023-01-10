import re
from typing import Any

from frostfs_testlib.hosting.config import HostConfig, ServiceConfig
from frostfs_testlib.hosting.interfaces import Host
from frostfs_testlib.plugins import load_plugin


class Hosting:
    """Hosting manages infrastructure  where neoFS runs (machines and neoFS services)."""

    _hosts: list[Host]
    _host_by_address: dict[str, Host]
    _host_by_service_name: dict[str, Host]

    @property
    def hosts(self) -> list[Host]:
        """Returns all hosts registered in the hosting.

        Returns:
            List of hosts.
        """
        return self._hosts

    def configure(self, config: dict[str, Any]) -> None:
        """Configures hosts from specified config.

        All existing hosts will be removed from the hosting.

        Args:
            config: Dictionary with hosting configuration.
        """
        hosts = []
        host_by_address = {}
        host_by_service_name = {}

        host_configs = [HostConfig(**host_config) for host_config in config["hosts"]]
        for host_config in host_configs:
            host_class = load_plugin("frostfs.testlib.hosting", host_config.plugin_name)
            host = host_class(host_config)

            hosts.append(host)
            host_by_address[host_config.address] = host

            for service_config in host_config.services:
                host_by_service_name[service_config.name] = host

        self._hosts = hosts
        self._host_by_address = host_by_address
        self._host_by_service_name = host_by_service_name

    def get_host_by_address(self, host_address: str) -> Host:
        """Returns host with specified address.

        Args:
            host_address: Address of the host.

        Returns:
            Host that manages machine with specified address.
        """
        host = self._host_by_address.get(host_address)
        if host is None:
            raise ValueError(f"Unknown host address: '{host_address}'")
        return host

    def get_host_by_service(self, service_name: str) -> Host:
        """Returns host where service with specified name is located.

        Args:
            service_name: Name of the service.

        Returns:
            Host that manages machine where service is located.
        """
        host = self._host_by_service_name.get(service_name)
        if host is None:
            raise ValueError(f"Unknown service name: '{service_name}'")
        return host

    def get_service_config(self, service_name: str) -> ServiceConfig:
        """Returns config of service with specified name.

        Args:
            service_name: Name of the service.

        Returns:
            Config of the service.
        """
        host = self.get_host_by_service(service_name)
        return host.get_service_config(service_name)

    def find_service_configs(self, service_name_pattern: str) -> list[ServiceConfig]:
        """Finds configs of services where service name matches specified regular expression.

        Args:
            service_name_pattern - regular expression for service names.

        Returns:
            List of service configs matched with the regular expression.
        """
        service_configs = [
            service_config
            for host in self.hosts
            for service_config in host.config.services
            if re.match(service_name_pattern, service_config.name)
        ]
        return service_configs
