# frostfs-testlib
This library provides building blocks and utilities to facilitate development of automated tests for FrostFS system.

## Installation
Library can be installed via pip:
```shell
$ pip install frostfs-testlib
```

## Configuration
Some library components support configuration that allows dynamic loading of extensions via plugins. Configuration of such components is described in this section.

### Reporter Configuration
Reporter is a singleton component that is used by the library to store test artifacts.

Reporter sends artifacts to handlers that are responsible for actual storing in particular system. By default reporter is initialized without any handlers and won't take any actions to store the artifacts. To add handlers directly via code you can use method `register_handler`:

```python
from frostfs_testlib.reporter import AllureHandler, get_reporter

get_reporter().register_handler(AllureHandler())
```

This registration should happen early at the test session, because any artifacts produced before handler is registered won't be stored anywhere.

Alternative approach for registering handlers is to use method `configure`. It is similar to method [dictConfig](https://docs.python.org/3/library/logging.config.html#logging.config.dictConfig) in a sense that it receives a config structure that describes handlers that should be registered in the reporter. Each handler is defined by it's plugin name; for example, to register the built-in Allure handler, we can use the following config:

```python
get_reporter().configure({ "handlers": [{"plugin_name": "allure"}] })
```

### Hosting Configuration
Hosting component is a class that represents infrastructure (machines/containers/services) where neoFS is hosted. Interaction with specific infrastructure instance (host) is encapsulated in classes that implement interface `frostfs_testlib.hosting.Host`. To pass information about hosts to the `Hosting` class in runtime we use method `configure`:

```python
from frostfs_testlib.hosting import Hosting

hosting = Hosting()
hosting.configure({ "hosts": [{ "address": "localhost", "plugin_name": "docker" ... }]})
```

## Plugins
Testlib uses [entrypoint specification](https://docs.python.org/3/library/importlib.metadata.html) for plugins. Testlib supports the following entrypoint groups for plugins:
 - `frostfs.testlib.reporter` - group for reporter handler plugins. Plugin should be a class that implements interface `frostfs_testlib.reporter.interfaces.ReporterHandler`.

### Example reporter plugin
In this example we will consider two Python projects:
 - Project "my_frostfs_plugins" where we will build a plugin that extends testlib functionality.
 - Project "my_frostfs_tests" that uses "frostfs_testlib" and "my_frostfs_plugins" to build some tests.

Let's say we want to implement some custom reporter handler that can be used as a plugin for testlib. Pseudo-code of implementation can look like that:
```python
# File my_frostfs_plugins/src/foo/bar/custom_handler.py
from contextlib import AbstractContextManager
from frostfs_testlib.reporter import ReporterHandler


class CustomHandler(ReporterHandler):
    def step(self, name: str) -> AbstractContextManager:
        ... some implementation ...

    def attach(self, content: Any, file_name: str) -> None:
        ... some implementation ...
```

Then in the file `pyproject.toml` of "my_frostfs_plugins" we should register entrypoint for this plugin. Entrypoint must belong to the group `frostfs.testlib.reporter`:
```yaml
# File my_frostfs_plugins/pyproject.toml
[project.entry-points."frostfs.testlib.reporter"]
my_custom_handler = "foo.bar.custom_handler:CustomHandler"
```

Finally, to use this handler in our test project "my_frostfs_tests", we should configure reporter with name of the handler plugin:

```python
# File my_frostfs_tests/src/conftest.py
from frostfs_testlib.reporter import get_reporter

get_reporter().configure({ "handlers": [{"plugin_name": "my_custom_handler"}] })
```

Detailed information about registering entrypoints can be found at [setuptools docs](https://setuptools.pypa.io/en/latest/userguide/entry_point.html).

## Library structure
The library provides the following primary components:
 * `blockchain` - Contains helpers that allow to interact with neo blockchain, smart contracts, gas transfers, etc.
 * `cli` - wrappers on top of neoFS command-line tools. These wrappers execute on a shell and provide type-safe interface for interacting with the tools.
 * `hosting` - management of infrastructure (docker, virtual machines, services where neoFS is hosted). The library provides host implementation for docker environment (when neoFS services are running as docker containers). Support for other hosts is provided via plugins.
 * `reporter` - abstraction on top of test reporting tool like Allure. Components of the library will report their steps and attach artifacts to the configured reporter instance.
 * `shell` - shells that can be used to execute commands. Currently library provides local shell (on machine that runs the code) or SSH shell that connects to a remote machine via SSH.
 * `utils` - Support functions.
 

## Contributing
Any contributions to the library should conform to the [contribution guideline](https://github.com/TrueCloudLab/frostfs-testlib/blob/master/CONTRIBUTING.md).
