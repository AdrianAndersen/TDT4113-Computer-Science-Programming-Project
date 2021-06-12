from Person import Person


class Sender(Person):
    def operate_cipher(self, text):
        return self.get_cipher_algorithm().encode(self.get_key(), text)
