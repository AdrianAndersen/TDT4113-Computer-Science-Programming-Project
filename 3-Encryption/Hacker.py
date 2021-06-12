import string

from Receiver import Receiver


class Hacker(Receiver):
    words = None
    ALPHABET = string.printable

    def __init__(self):
        with open("supplemental_files/english_words.txt") as f:
            self.words = f.read().splitlines()

    def hack(self, encrypted_text, cipher_type):
        candidates = []
        if cipher_type == "caesar" or cipher_type == "multiplicative":
            for i in range(0, 210):
                self.set_key(i)
                candidate = self.operate_cipher(encrypted_text)
                if candidate in self.words and candidate not in candidates:
                    candidates.append(candidate)
        if cipher_type == "unbreakable":
            for word in self.words:

                decryption_key = ""
                for char in word:
                    char_index = (len(self.ALPHABET) - self.ALPHABET.index(char)) % len(
                        self.ALPHABET
                    )
                    decryption_key += self.ALPHABET[char_index]

                self.set_key(decryption_key)
                candidate = self.operate_cipher(encrypted_text)
                if candidate in self.words and candidate not in candidates:
                    candidates.append(candidate)
                    return candidate
        return candidates
