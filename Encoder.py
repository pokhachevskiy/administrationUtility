from pygost.gost3412 import *


class Encoder:
    def __init__(self):
        self.encoder = None
        self.mode = False

    def set_key(self, key):
        self.encoder = GOST3412Kuznechik(key)

    def set_mode(self, mode):
        self.mode = mode

    def encrypt(self, text):
        if isinstance(text, str):
            text = text.encode()
        if not self.mode:
            return text
        ans = b''
        for i in range(0, len(text), 16):
            st = text[i:i + 16]
            if len(st) < 16:
                st = st + b' ' * (16 - len(st))
            ans += self.encoder.encrypt(st)
        return ans

    def decrypt(self, enc_text):
        if not self.mode:
            return enc_text
        ans = b''
        for i in range(0, len(enc_text), 16):
            st = enc_text[i:i + 16]
            ans += self.encoder.decrypt(st)
        return ans.rstrip()
