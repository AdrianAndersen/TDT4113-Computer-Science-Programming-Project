import random

from ciphers.Cipher import Cipher
from logger.Logger import Logger


class Caesar(Cipher):
    __logger = Logger()

    def encode(self, encryption_key, text):
        self.__logger.debug("\nCaesar Encryption:")
        result = ""
        for char in text:
            original_index = self.ALPHABET.index(char)
            new_index = (original_index + encryption_key) % len(self.ALPHABET)
            result += self.ALPHABET[new_index]
            self.__logger.debug(
                f"alphabet[{original_index}]={self.ALPHABET[original_index]} => alphabet[{new_index}]={self.ALPHABET[new_index]}"
            )

        return result

    def decode(self, decryption_key, encrypted_text):
        self.__logger.debug("\nCaesar Decryption:")
        result = ""

        for char in encrypted_text:
            encrypted_index = self.ALPHABET.index(char)
            original_index = (encrypted_index - decryption_key) % len(self.ALPHABET)
            result += self.ALPHABET[original_index]
            self.__logger.debug(
                f"alphabet[{encrypted_index}]={self.ALPHABET[encrypted_index]} => alphabet[{original_index}]={self.ALPHABET[original_index]}"
            )
        return result

    def generate_keys(self):
        key = random.randint(1, 200)
        return {"encryption": key, "decryption": key}
