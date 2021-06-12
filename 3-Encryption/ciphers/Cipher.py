import string

from logger.Logger import Logger


class Cipher:
    __logger = Logger()
    ALPHABET = string.printable

    def encode(self, encryption_key, text):
        pass

    def decode(self, decryption_key, encrypted_text):
        pass

    def verify(self, encryption_key, decryption_key, text):
        self.__logger.debug("\nVerify:")
        return self.decode(decryption_key, self.encode(encryption_key, text)) == text

    def generate_keys():
        pass
