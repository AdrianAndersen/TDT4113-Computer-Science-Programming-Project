class Person:
    __key = None
    __cipher_algorithm = None

    def get_key(self):
        return self.__key

    def set_key(self, new_key):
        self.__key = new_key

    def operate_cipher(self, encrypted_text):
        pass

    def set_cipher_algorithm(self, cipher_algorithm):
        self.__cipher_algorithm = cipher_algorithm

    def get_cipher_algorithm(self):
        return self.__cipher_algorithm
