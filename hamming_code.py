from enum import Enum
from typing import List, Tuple, Union


# IMPORTANT NOTE: DO NOT IMPORT THE ev3dev.ev3 MODULE IN THIS FILE

class HCResult(Enum):
    """
    Return codes for the Hamming Code interface
    """
    VALID = 'OK'
    CORRECTED = 'FIXED'
    UNCORRECTABLE = 'ERROR'


class HammingCode:
    """
    Provides decoding capabilities for the specified Hamming Code
    """

    def __init__(self):
        """
        Initializes the class HammingCode with all values necessary.
        """
        self.total_bits = 10  # n
        self.data_bits = 6  # k
        self.parity_bits = 4  # r = (n-k)

        # Predefined non-systematic generator matrix G'
        gns = [
            [1, 1, 1, 0, 0, 0, 0, 1, 0, 0],
            [0, 1, 0, 0, 1, 0, 0, 1, 0, 0],
            [1, 0, 0, 1, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 1, 1, 0, 0],
            [1, 1, 0, 1, 0, 0, 0, 1, 1, 0],
            [1, 0, 0, 1, 0, 0, 0, 1, 0, 1]
        ]

        # Convert non-systematic G' into systematic matrices G, H
        self.g = self.__convert_to_g(gns)
        self.h = self.__derive_h(self.g)

    def __convert_to_g(self, gns: List) -> List:
        """
        Converts a non-systematic generator matrix into a systematic form.

        Args:
            gns (List[List[int]]): Non-systematic generator matrix
        Returns:
            List[List[int]]: Systematic generator matrix
        """
        # Apply the series of XOR-based row reductions
        operations = [
            (1, 3), (1, 5), (1, 6),
            (2, 1), (2, 3), (2, 6),
            (3, 1), (3, 5), (3, 6),
            (4, 1), (4, 3),
            (5, 2), (5, 3),
            (6, 1), (6, 2), (6, 5)
        ]

        for from_row, target_row in operations:
            # Subtract (XOR) from_row from target_row (adjusting for 0-indexing)
            for j in range(len(gns[0])):
                gns[target_row - 1][j] ^= gns[from_row - 1][j]

        return gns  # Return the now systematic matrix

    def __derive_h(self, g: List) -> List:
        idm = self.data_bits
        # Extract columns other than identity matrix for P
        P = [row[idm:] for row in g]
        #print("\nExtracted P matrix (non-identity part):")
        #for m in P:
          #print(m)
        P_Trans = [[P[j][i] for j in range(len(P))] for i in range(len(P[0]))]
        id_s = len(P_Trans)
        # get identity matrix to append to transpose P matrix and get parity check matrix
        I = [[1 if i == j else 0 for j in range(id_s)] for i in range(id_s)]
        H = [P_Trans[i] + I[i] for i in range(id_s)]
        #print("Derived Parity-Check matrix H:")

        #for k in H:
            #print(k)

        return H

    def encode(self, source_word: Tuple[int, ...]) -> Tuple[int, ...]:
        source_word = list(source_word)
        encoded_word = []

        # Perform the matrix multiplication with the generator matrix G
        for i in range(len(self.g[0])):  # Iterate over the rows of G
            bs = 0
            for j in range(len(source_word)):  # Iterate over the columns of G
                bs = bs + source_word[j] * self.g[j][i]  # XOR for binary addition
            encoded_word.append(bs % 2)

        encoded_bit = sum(encoded_word) % 2
        encoded_word.append(encoded_bit)

        return tuple(encoded_word)

    def decode(self, encoded_word: Tuple[int, ...]) -> Tuple[Union[None, Tuple[int, ...]], HCResult]:
        d_and_p_bts = encoded_word[:-1]
        even_org_pbit = encoded_word[-1]
        print(even_org_pbit)
        # to Calculate expected even parity for d_and_p_bts (10 bits)
        even_parity = sum(d_and_p_bts) % 2
        parity_check = even_parity == even_org_pbit

        # to Calculate the syndrome vector using the parity-check matrix H
        syndrome = [0] * len(self.h)
        # print(H)
        for i in range(len(self.h)):
            syndrome[i] = sum(d_and_p_bts[j] * self.h[i][j] for j in range(self.total_bits)) % 2
        syndrome_value = 11
        # Convert syndrome to a decimal value to identify any single-bit error location
        for i in range(0,self.total_bits):
            column=tuple(row[i] for row in self.h)
            if column == tuple(syndrome):
                syndrome_value = i
                break
        if sum(syndrome) == 0:
            syndrome_value=0
        print(syndrome)
        print(syndrome_value)
        if syndrome_value == 0:
            # No error detected
            #if parity_check:
              return tuple(d_and_p_bts[:self.data_bits]), HCResult.VALID
            #else:
              #return None, HCResult.UNCORRECTABLE

        elif 1 <= syndrome_value <= self.total_bits:
            # Single-bit error detected, correctable
            crct_bit = list(d_and_p_bts)
            error_position = syndrome_value
            # Flip the erroneous bit
            crct_bit[error_position] ^= 1
            # Recalculate parity after correction
            #corrected_parity = sum(crct_bit) % 2
            #if corrected_parity == even_org_pbit:
            return tuple(crct_bit[:self.data_bits]), HCResult.CORRECTED
            #else:
              #return None, HCResult.UNCORRECTABLE
        else:
            # Multiple errors detected, uncorrectable
            return None, HCResult.UNCORRECTABLE




hamming_code = HammingCode()
print("Generator Matrix G (systematic form):")
for row in hamming_code.g:
    print(row)

print("\nParity-check Matrix H:")
for row in hamming_code.h:
    print(row)

# Example data bits to test encode and decode
test_data = (0,1,1,0,1,1)
test_dataa2=(0,0,0,0,0,0,0,0,0,0,1)
encoded_word = hamming_code.encode(test_data)
decoded_word, result = hamming_code.decode(test_dataa2)
print("Encoded word:", encoded_word)
print("decoded word:", decoded_word,result.value)

