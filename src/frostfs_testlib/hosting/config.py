from dataclasses import dataclass, field, fields
from typing import Any


@dataclass
class ParsedAttributes:
    """Base class for data structures representing parsed attributes from configs."""

    @classmethod
    def parse(cls, attributes: dict[str, Any]):
        # Pick attributes supported by the class
        field_names = set(field.name for field in fields(cls))
        supported_attributes = {
            key: value for key, value in attributes.items() if key in field_names
        }
        return cls(**supported_attributes)


@dataclass
class CLIConfig:
    """Describes CLI tool on some host.

    Attributes:
        name: Name of the tool.
        exec_path: Path to executable file of the tool.
        attributes: Dict with extra information about the tool.
    """

    name: str
    exec_path: str
    attributes: dict[str, str] = field(default_factory=dict)


@dataclass
class ServiceConfig:
    """Describes neoFS service on some host.

    Attributes:
        name: Name of the service that uniquely identifies it across all hosts.
        attributes: Dict with extra information about the service. For example, we can store
            name of docker container (or name of systemd service), endpoints, path to wallet,
            path to configuration file, etc.
    """

    name: str
    attributes: dict[str, str] = field(default_factory=dict)


@dataclass
class HostConfig:
    """Describes machine that hosts neoFS services.

    Attributes:
        plugin_name: Name of plugin that should be used to manage the host.
        address: Address of the machine (IP or DNS name).
        services: List of services hosted on the machine.
        clis: List of CLI tools available on the machine.
        attributes: Dict with extra information about the host. For example, we can store
            connection parameters in this dict.
    """

    plugin_name: str
    address: str
    services: list[ServiceConfig] = field(default_factory=list)
    clis: list[CLIConfig] = field(default_factory=list)
    attributes: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.services = [ServiceConfig(**service) for service in self.services or []]
        self.clis = [CLIConfig(**cli) for cli in self.clis or []]
