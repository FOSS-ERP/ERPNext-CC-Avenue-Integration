import frappe
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64
from hashlib import md5


def hextobin(hex_string):
    return bytes.fromhex(hex_string)

def encrypt(plain_text, key):
    key = md5(key.encode('utf-8')).digest()
    init_vector = bytes([0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f])
    cipher = AES.new(key, AES.MODE_CBC, init_vector)
    padded_text = pad(str(plain_text).encode('utf-8'), AES.block_size)
    encrypted_text = cipher.encrypt(padded_text)
    return encrypted_text.hex()

def decrypt(encrypted_text, key):
    key = md5(key.encode('utf-8')).digest()
    init_vector = bytes([0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f])
    print(encrypted_text)
    encrypted_text = hextobin(encrypted_text)
    cipher = AES.new(key, AES.MODE_CBC, init_vector)
    decrypted_text = unpad(cipher.decrypt(encrypted_text), AES.block_size)
    return decrypted_text.decode('utf-8')


