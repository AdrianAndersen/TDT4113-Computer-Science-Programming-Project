from Person import Person


class Receiver(Person):
    def operate_cipher(self, encrypted_text):
        return self.get_cipher_algorithm().decode(self.get_key(), encrypted_text)
