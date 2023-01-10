from unittest import TestCase

from frostfs_testlib.utils import converters


class TestConverters(TestCase):
    def test_str_to_ascii_hex(self):
        source_str = ""
        result_str = ""
        self.assertEqual(converters.str_to_ascii_hex(source_str), result_str)

        source_str = '"test_data" f0r ^convert*'
        result_str = "22746573745f646174612220663072205e636f6e766572742a"
        self.assertEqual(converters.str_to_ascii_hex(source_str), result_str)

    def test_ascii_hex_to_str(self):
        source_str = ""
        result_bytes = b""
        self.assertEqual(converters.ascii_hex_to_str(source_str), result_bytes)

        source_str = "22746573745f646174612220663072205e636f6e766572742a"
        result_bytes = b'"test_data" f0r ^convert*'
        self.assertEqual(converters.ascii_hex_to_str(source_str), result_bytes)

    def test_process_b64_bytearray_reverse(self):
        source_str = ""
        result_bytes = b""
        self.assertEqual(converters.process_b64_bytearray_reverse(source_str), result_bytes)

        source_str = "InRlc3RfZGF0YSIgZjByIF5jb252ZXJ0Kg=="
        result_bytes = b"2a747265766e6f635e207230662022617461645f7473657422"
        self.assertEqual(converters.process_b64_bytearray_reverse(source_str), result_bytes)

    def test_process_b64_bytearray(self):
        source_str = ""
        result_bytes = b""
        self.assertEqual(converters.process_b64_bytearray(source_str), result_bytes)

        source_str = "InRlc3RfZGF0YSIgZjByIF5jb252ZXJ0Kg=="
        result_bytes = b"22746573745f646174612220663072205e636f6e766572742a"
        self.assertEqual(converters.process_b64_bytearray(source_str), result_bytes)

    def test_contract_hash_to_address(self):
        source_str = "d01a381aae45f1ed181db9d554cc5ccc69c69f4e"
        result_str = "NT5hJ5peVmvYdZCsFKUM5MTcEGw5TB4k89"
        self.assertEqual(converters.contract_hash_to_address(source_str), result_str)
