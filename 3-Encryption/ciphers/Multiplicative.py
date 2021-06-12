import random

from ciphers.Cipher import Cipher
from logger.Logger import Logger
from supplemental_files.crypto_utils import extended_gcd, modular_inverse


class Multiplicative(Cipher):
    __logger = Logger()

    def encode(self, encryption_key, text):
        self.__logger.debug("\nMultiplicative Encryption:")
        result = ""
        result_indexes = []
        for char in text:
            original_index = self.ALPHABET.index(char)
            new_index = (original_index * encryption_key) % len(self.ALPHABET)
            result_indexes.append(new_index)
            result += self.ALPHABET[new_index]
            self.__logger.debug(
                f"alphabet[{original_index}]={self.ALPHABET[original_index]} => alphabet[{new_index}]={self.ALPHABET[new_index]}"
            )

        return result

    def decode(self, decryption_key, encrypted_text):
        self.__logger.debug("\nMultiplicative Decryption:")
        result = ""

        for char in encrypted_text:
            encrypted_index = self.ALPHABET.index(char)
            original_index = (encrypted_index * decryption_key) % len(self.ALPHABET)
            result += self.ALPHABET[original_index]
            self.__logger.debug(
                f"alphabet[{encrypted_index}]={self.ALPHABET[encrypted_index]} => alphabet[{original_index}]={self.ALPHABET[original_index]}"
            )
        return result

    def generate_keys(self):
        key = None
        gcd_value = None
        while key is None or gcd_value != 1:
            key = random.randint(1, 210)
            gcd_value, x, y = extended_gcd(key, len(self.ALPHABET))
        return {
            "encryption": key,
            "decryption": modular_inverse(key, len(self.ALPHABET)),
        }
