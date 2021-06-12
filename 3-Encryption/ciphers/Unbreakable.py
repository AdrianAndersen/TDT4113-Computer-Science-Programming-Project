import random

from ciphers.Cipher import Cipher
from logger.Logger import Logger


class Unbreakable(Cipher):
    __logger = Logger()

    def encode(self, encryption_key, text):
        result = ""
        keyword_index = 0
        for char in text:
            keyword_value = self.ALPHABET.index(encryption_key[keyword_index])
            text_value = self.ALPHABET.index(char)
            result_value = (text_value + keyword_value) % len(self.ALPHABET)
            result += self.ALPHABET[result_value]

            keyword_index = (keyword_index + 1) % len(encryption_key)

        return result

    def decode(self, decryption_key, encrypted_text):
        return self.encode(decryption_key, encrypted_text)

    def generate_keys(self):
        possible_keys = None
        with open("supplemental_files/english_words.txt") as f:
            possible_keys = f.read().splitlines()
        encryption_key = possible_keys[random.randint(0, len(possible_keys))]
        decryption_key = ""
        for char in encryption_key:
            char_index = (len(self.ALPHABET) - self.ALPHABET.index(char)) % len(
                self.ALPHABET
            )
            decryption_key += self.ALPHABET[char_index]

        return {"encryption": encryption_key, "decryption": decryption_key}
