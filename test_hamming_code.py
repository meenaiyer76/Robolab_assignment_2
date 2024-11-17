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
            (1, 0, 1, 1, 0),
            (1, 1, 1, 1, 1, 0)
        ]
        for test in encode_tests:

            if len(test) == 6:
             encoded = self.hamming.encode(test)
             print(f"Input Word: {test}")
             print(f"Encoded word: {encoded}")
            # Decode the encoded value and check if it matches the original input
             decoded,status = self.hamming.decode(encoded)
             assert decoded == test, f"Decoded value {decoded} does not match original input {test}"
            else:
             with self.assertRaises(ValueError):
              self.hamming.encode(test)
              self.fail("failed")

    def test_decode_valid(self):
        """ Essential: Test method decode() with VALID input """
        decode_tests = [
            (1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1),
            (1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0)
        ]
        for test in decode_tests:
            if len(test) == 11:
              decoded, status = self.hamming.decode(test)
              print(f"Input Word: {test}")
              print(f"Valid word and Status: {decoded}, {status.value}")
              assert "OK" == status.value, "Incorrect Output for valid input test"
            else:
             with self.assertRaises(ValueError):
              self.hamming.encode(test)

    def test_decode_corrected(self):
        """ Essential: Test method decode() with CORRECTED input """
        correctable_code = [
            (1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1),
            (0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0),
            (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1),
            (1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1)
        ]
        for test in correctable_code:
            try:
              decoded_correctable, status = self.hamming.decode(test)
              print(f"Entered code: {test}")
              print(f"Corrected Code and status: {decoded_correctable}, {status.value}")
              assert "FIXED" == status.value, "Incorrect Output for Correctable test"
            except ValueError as e:
              print(f"{e}")


    def test_decode_uncorrectable(self):
        """ Essential: Test method decode() with UNCORRECTABLE input """
        uncorrectable_code = [
            (1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0),
            (1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1)
        ]
        for test in uncorrectable_code:
         try:
            decoded_uncorrectable, status = self.hamming.decode(test)
            print(f"Entered code: {test}")
            print(f"Uncorrected Code and status: {decoded_uncorrectable}, {status.value}")
            assert "ERROR" == status.value, "Incorrect Output for Uncorrectable test"


         except ValueError as e:
            print(f"{e}")

if __name__ == '__main__':
    unittest.main()
