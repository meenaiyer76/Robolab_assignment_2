import unittest
from hamming_code import HammingCode

class TestHammingCode(unittest.TestCase):
    def setUp(self):
        """ Set up the HammingCode instance """
        self.hamming = HammingCode()

    def test_instance(self):
        """ Essential: Test class instantiation """
        self.assertIsInstance(self.hamming, HammingCode)

    def test_encode(self):
        """ Essential: Test method encode() """
        encode_tests = [
            (0, 1, 1, 0, 1, 1),
            (0, 0, 0, 0, 0, 0),
            (1, 0, 1, 1, 0, 1),
            (1, 1, 1, 1, 1, 0)
        ]
        for test in encode_tests:
            encoded = self.hamming.encode(test)
            print(f"Encoded {test}: {encoded}")
            # Decode the encoded value and check if it matches the original input
            decoded,status = self.hamming.decode(encoded)
            assert decoded == test, f"Decoded value {decoded} does not match original input {test}"

    def test_decode_valid(self):
        """ Essential: Test method decode() with VALID input """
        decode_tests = [
            (0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0),
            (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1),
            (1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1),
            (1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1)
        ]
        for test in decode_tests:
            decoded, status = self.hamming.decode(test)
            print(f"Decoded {test}: {decoded},{status.value}")

    def test_decode_corrected(self):
        """ Essential: Test method decode() with CORRECTED input """
        correctable_code = (1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1)
        decoded_correctable, status = self.hamming.decode(correctable_code)
        print(f"Decoded correctable code {correctable_code}: {decoded_correctable}")
        assert decoded_correctable == (1, 0, 1, 1, 0, 1), "Correctable code did not decode correctly"

    def test_decode_uncorrectable(self):
        """ Essential: Test method decode() with UNCORRECTABLE input """
        uncorrectable_code = (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
        try:
            self.hamming.decode(uncorrectable_code)
        except ValueError as e:
            print(f"Uncorrectable code {uncorrectable_code} raised an error: {e}")

if __name__ == '__main__':
    unittest.main()
