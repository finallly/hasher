class CaesarKeyCipher(object):

    def __init__(self, text=None, keyword=None):
        self.text = text
        self.key = sum([ord(symbol) for symbol in keyword]) if keyword is not None else int(False)
        self.symbols = [symbol for symbol in self.text]

    def encrypt(self) -> str:
        """
        this method uses caesar with key method of encryption
        :return: encrypted text
        """
        return ''.join([chr(ord(symbol) + self.key) for symbol in self.symbols])

    def decrypt(self) -> str:
        """
        this method uses caesar with key method of encryption
        :return: decrypted text
        """
        try:
            return ''.join([chr(ord(symbol) - self.key) for symbol in self.symbols])
        except ValueError:
            pass
