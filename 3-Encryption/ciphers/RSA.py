import random

from ciphers.Cipher import Cipher
from logger.Logger import Logger
from supplemental_files.crypto_utils import (blocks_from_text, extended_gcd,
                                             generate_random_prime,
                                             modular_inverse, text_from_blocks)


class RSA(Cipher):
    __logger = Logger()

    def encode(self, encryption_key, text):
        blocks = blocks_from_text(text, 2)
        encrypted_blocks = []
        print("before encryption from blocks: ", text_from_blocks(blocks, 2))
        for t in blocks:
            n = encryption_key[0]
            e = encryption_key[1]
            encrypted_block = pow(t, e, n)
            encrypted_blocks.append(encrypted_block)
        
        return encrypted_blocks

    def decode(self, decryption_key, encrypted_text):
        blocks = []

        for t in encrypted_text:
            n = decryption_key[0]
            d = decryption_key[1]
            decrypted_block = pow(t, d, n)
            blocks.append(decrypted_block)

        return text_from_blocks(blocks, 2)

    def generate_keys(self):
        p = None
        q = None
        n = None
        e = None
        d = None
        gcd_value = None

        while p == None or p == q or gcd_value != 1:
            p = generate_random_prime(8)
            q = generate_random_prime(8)

            n = p * q
            fi = (p - 1) * (q - 1)
            e = random.randint(3, fi - 1)
            gcd_value, x, y = extended_gcd(e, fi)
            if gcd_value != 1:
                continue
            d = modular_inverse(e, fi)
        return {"encryption": (n, e), "decryption": (n, d)}
