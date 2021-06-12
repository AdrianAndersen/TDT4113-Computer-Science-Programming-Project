import sys

from ciphers.Affine import Affine
from ciphers.Caesar import Caesar
from ciphers.Multiplicative import Multiplicative
from ciphers.RSA import RSA
from ciphers.Unbreakable import Unbreakable
from Hacker import Hacker
from InputHelper import InputHelper
from logger.Logger import Logger
from Receiver import Receiver
from Sender import Sender


class Main:
    __logger = Logger()

    def __init__(self):
        self.__logger.clear_logs()

    def main(self):
        command_helper = InputHelper(
            ["caesar", "multiplicative", "affine", "unbreakable", "rsa", "exit"]
        )
        try:
            next_command = command_helper.get_legal_input("Please enter a command: \n")
            sender = Sender()
            receiver = Receiver()
            hacker = Hacker()
            cipher_algorithm = None
            if next_command == "caesar":
                cipher_algorithm = Caesar()
            if next_command == "multiplicative":
                cipher_algorithm = Multiplicative()
            if next_command == "affine":
                cipher_algorithm = Affine()
            if next_command == "unbreakable":
                cipher_algorithm = Unbreakable()
            if next_command == "rsa":
                cipher_algorithm = RSA()
                hacker = None
            if next_command == "exit":
                sys.exit(0)

            sender.set_cipher_algorithm(cipher_algorithm)
            receiver.set_cipher_algorithm(cipher_algorithm)

            keys = cipher_algorithm.generate_keys()
            self.__logger.info(f"Keyset: {keys}")

            sender.set_key(keys["encryption"])
            receiver.set_key(keys["decryption"])

            message = input("Please input a message to be encrypt:\n")

            encrypted_text = sender.operate_cipher(message)

            if hacker is not None:
                hacker.set_cipher_algorithm(cipher_algorithm)
                self.__logger.info(
                    f"Hackerman found: {hacker.hack(encrypted_text, next_command)}"
                )

            decrypted_text = receiver.operate_cipher(encrypted_text)

            self.__logger.info(
                f"{message} => {encrypted_text} => {decrypted_text} (Success={cipher_algorithm.verify(sender.get_key(), receiver.get_key(),message)})"
            )

        except KeyboardInterrupt:
            return self.main()


if __name__ == "__main__":
    Main().main()
