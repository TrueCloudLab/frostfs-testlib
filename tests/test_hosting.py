from unittest import TestCase

from frostfs_testlib.hosting import CLIConfig, Hosting, ServiceConfig


class TestHosting(TestCase):
    SERVICE_NAME_PREFIX = "service"
    HOST1_ADDRESS = "10.10.10.10"
    HOST1_PLUGIN = "docker"
    HOST1_ATTRIBUTES = {"param1": "value1"}
    SERVICE1_ATTRIBUTES = {"rpc_endpoint": "service1_endpoint"}
    HOST1_CLIS = [{"name": "cli1", "exec_path": "cli1.exe", "attributes": {"param1": "value1"}}]
    SERVICE1 = {"name": f"{SERVICE_NAME_PREFIX}1", "attributes": SERVICE1_ATTRIBUTES}
    HOST1_SERVICES = [SERVICE1]
    HOST1 = {
        "address": HOST1_ADDRESS,
        "plugin_name": HOST1_PLUGIN,
        "attributes": HOST1_ATTRIBUTES,
        "clis": HOST1_CLIS,
        "services": HOST1_SERVICES,
    }

    HOST2_ADDRESS = "localhost"
    HOST2_PLUGIN = "docker"
    HOST2_ATTRIBUTES = {"param2": "value2"}
    SERVICE2_ATTRIBUTES = {"rpc_endpoint": "service2_endpoint"}
    SERVICE3_ATTRIBUTES = {"rpc_endpoint": "service3_endpoint"}
    HOST2_CLIS = [{"name": "cli2", "exec_path": "/bin/cli", "attributes": {}}]
    SERVICE2 = {"name": f"{SERVICE_NAME_PREFIX}", "attributes": SERVICE2_ATTRIBUTES}
    SERVICE3 = {"name": f"text_before_{SERVICE_NAME_PREFIX}3", "attributes": SERVICE3_ATTRIBUTES}
    HOST2_SERVICES = [SERVICE2, SERVICE3]
    HOST2 = {
        "address": HOST2_ADDRESS,
        "plugin_name": HOST2_PLUGIN,
        "attributes": HOST2_ATTRIBUTES,
        "clis": HOST2_CLIS,
        "services": HOST2_SERVICES,
    }
    HOSTING_CONFIG = {"hosts": [HOST1, HOST2]}

    def test_hosting_configure(self):
        hosting = Hosting()
        hosting.configure(self.HOSTING_CONFIG)
        self.assertEqual(len(hosting.hosts), 2)

    def test_get_host_by_address(self):
        hosting = Hosting()
        hosting.configure(self.HOSTING_CONFIG)

        host1 = hosting.get_host_by_address(self.HOST1_ADDRESS)
        self.assertEqual(host1.config.address, self.HOST1_ADDRESS)
        self.assertEqual(host1.config.plugin_name, self.HOST1_PLUGIN)
        self.assertDictEqual(host1.config.attributes, self.HOST1_ATTRIBUTES)
        self.assertListEqual(host1.config.clis, [CLIConfig(**cli) for cli in self.HOST1_CLIS])
        self.assertListEqual(
            host1.config.services, [ServiceConfig(**service) for service in self.HOST1_SERVICES]
        )

        host2 = hosting.get_host_by_address(self.HOST2_ADDRESS)
        self.assertEqual(host2.config.address, self.HOST2_ADDRESS)
        self.assertEqual(host2.config.plugin_name, self.HOST2_PLUGIN)
        self.assertDictEqual(host2.config.attributes, self.HOST2_ATTRIBUTES)
        self.assertListEqual(host2.config.clis, [CLIConfig(**cli) for cli in self.HOST2_CLIS])
        self.assertListEqual(
            host2.config.services, [ServiceConfig(**service) for service in self.HOST2_SERVICES]
        )

    def test_get_host_by_service(self):
        hosting = Hosting()
        hosting.configure(self.HOSTING_CONFIG)

        host_with_service1 = hosting.get_host_by_service(self.SERVICE1["name"])
        host_with_service2 = hosting.get_host_by_service(self.SERVICE2["name"])
        host_with_service3 = hosting.get_host_by_service(self.SERVICE3["name"])

        self.assertEqual(host_with_service1.config.address, self.HOST1_ADDRESS)
        self.assertEqual(host_with_service2.config.address, self.HOST2_ADDRESS)
        self.assertEqual(host_with_service3.config.address, self.HOST2_ADDRESS)

    def test_get_service_config(self):
        hosting = Hosting()
        hosting.configure(self.HOSTING_CONFIG)

        service1_config = hosting.get_service_config(self.SERVICE1["name"])
        service2_config = hosting.get_service_config(self.SERVICE2["name"])
        service3_config = hosting.get_service_config(self.SERVICE3["name"])

        self.assertEqual(service1_config.name, self.SERVICE1["name"])
        self.assertDictEqual(service1_config.attributes, self.SERVICE1_ATTRIBUTES)

        self.assertEqual(service2_config.name, self.SERVICE2["name"])
        self.assertDictEqual(service2_config.attributes, self.SERVICE2_ATTRIBUTES)

        self.assertEqual(service3_config.name, self.SERVICE3["name"])
        self.assertDictEqual(service3_config.attributes, self.SERVICE3_ATTRIBUTES)

    def test_find_service_configs(self):
        hosting = Hosting()
        hosting.configure(self.HOSTING_CONFIG)

        all_services = hosting.find_service_configs(r".+")
        self.assertEqual(len(all_services), 3)

        services = hosting.find_service_configs(rf"^{self.SERVICE_NAME_PREFIX}")
        self.assertEqual(len(services), 2)
        for service in services:
            self.assertEqual(
                service.name[: len(self.SERVICE_NAME_PREFIX)], self.SERVICE_NAME_PREFIX
            )

        service1 = hosting.find_service_configs(self.SERVICE1["name"])
        self.assertEqual(len(service1), 1)
        self.assertDictEqual(service1[0].attributes, self.SERVICE1_ATTRIBUTES)
