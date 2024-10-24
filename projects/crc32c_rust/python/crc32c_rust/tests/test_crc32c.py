import unittest
import tempfile
import os
from crc32c_rust import calculate_crc32c

import crcmod.predefined

class TestCRC32C(unittest.TestCase):
    def test_empty_file(self):
        with tempfile.NamedTemporaryFile(delete=False) as f:
            pass
        try:
            result = calculate_crc32c(f.name)
            self.assertEqual(result, 0)  # CRC32C of empty file is 0
        finally:
            os.unlink(f.name)

    def test_known_content(self):
        # generate a random content with a size of 100MB
        content = os.urandom(100 * 1024 * 1011 +1234)
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(content)
            f.flush()
        try:
            result = calculate_crc32c(f.name)
            expected = crcmod.predefined.mkPredefinedCrcFun('crc-32c')(content)
            self.assertEqual(result, expected)
        finally:
            os.unlink(f.name)

if __name__ == '__main__':
    unittest.main()
