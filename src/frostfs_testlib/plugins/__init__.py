import sys
from typing import Any

if sys.version_info < (3, 10):
    # On Python prior 3.10 we need to use backport of entry points
    from importlib_metadata import entry_points
else:
    from importlib.metadata import entry_points


def load_plugin(plugin_group: str, name: str) -> Any:
    """Loads plugin using entry point specification.

    Args:
        plugin_group: Name of plugin group that contains the plugin.
        name: Name of the plugin in the group.

    Returns:
        Plugin class if the plugin was found; otherwise returns None.
    """
    plugins = entry_points(group=plugin_group)
    if name not in plugins.names:
        return None
    plugin = plugins[name]
    return plugin.load()
