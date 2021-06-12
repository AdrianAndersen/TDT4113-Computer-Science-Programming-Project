from ciphers.Caesar import Caesar
from ciphers.Cipher import Cipher
from ciphers.Multiplicative import Multiplicative
from logger.Logger import Logger


class Affine(Cipher):
    __logger = Logger()
    __caesar_cipher = Caesar()
    __multiplicative_cipher = Multiplicative()

    def encode(self, encryption_key, text):
        return self.__caesar_cipher.encode(
            encryption_key[1],
            self.__multiplicative_cipher.encode(encryption_key[0], text),
        )

    def decode(self, decryption_key, encrypted_text):
        return self.__multiplicative_cipher.decode(
            decryption_key[0],
            self.__caesar_cipher.decode(decryption_key[1], encrypted_text),
        )

    def generate_keys(self):
        caesar_keys = self.__caesar_cipher.generate_keys()
        mult_keys = self.__multiplicative_cipher.generate_keys()

        return {
            "encryption": (mult_keys["encryption"], caesar_keys["encryption"]),
            "decryption": (mult_keys["decryption"], caesar_keys["decryption"]),
        }
