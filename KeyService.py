from pygost.utils import *
import random


def generate_random_key():
    enhex = lambda x: ''.join(hex(ord(i))[2:] for i in x)

    abc = 'abcdefghijklmnopqrstuvwxyz'
    random_key = lambda: enhex(''.join(random.choice(abc) for i in range(32)))

    key = hexdec(random_key())
    return key


# Утилита для генерации ключей
class KeyService:
    def __init__(self, filename="keyfile.txt"):
        f = open(filename, "r")
        config_key = bytes.fromhex(f.read())
        if len(config_key) == 0:
            f.close()
            f = open(filename, "w")
            config_key = generate_random_key()
            self.key = config_key
            f.write(config_key.hex())
        else:
            self.key = config_key
        f.close()
