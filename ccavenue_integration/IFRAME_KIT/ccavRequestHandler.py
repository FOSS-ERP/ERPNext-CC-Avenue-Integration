# ccavenue.py

import frappe
from frappe import _
from ccavenue_integration.IFRAME_KIT.ccavutil import encrypt , decrypt
from string import Template
from Crypto.Random import get_random_bytes
import json
from frappe.utils import now
from pay_ccavenue import CCAvenue



@frappe.whitelist(allow_guest=True)
def ccav_response_handler():
    enc_resp = frappe.form_dict['encResp']
    plain_text = res(enc_resp)
    return plain_text

@frappe.whitelist(allow_guest=True)
def ccav_request_handler(form_data):
    doc = frappe.get_doc("CCAvenue Settings")
    if doc.enable:
        access_code = doc.access_code
        WORKING_KEY = doc.working_key
        ACCESS_CODE = doc.access_code
        MERCHANT_CODE = doc.merchant_code
        REDIRECT_URL = doc.redirect_url
        CANCEL_URL = doc.cancel_url

        my_string = WORKING_KEY
        
        key = my_string
            
        encrypted_data = encrypt(form_data, key)

        import requests

        url = "https://apitest.ccavenue.com/apis/servlet/DoWebTrans"
        print(ACCESS_CODE)
        payload = {
            "request_type": "JSON",
            "access_code": ACCESS_CODE,
            "command": "generateQuickInvoice",
            "version": "1.2",
            "response_type": "JSON",
            "enc_request": encrypted_data
        }
        try:
            response = requests.post(url, data=payload, headers={})
            print("CCAvenue :", response)
            response = response.text.split('=')[2]
            data = decrypt(response, key)
            return data
        except Exception as e:
            frappe.log_error(response)
            frappe.log_error(e)


def caesar_cipher_encrypt(text, shift):
    encrypted_text = ""
    for char in text:
        if char.isalpha():
            encrypted_char = chr((ord(char) + shift - ord('a')) % 26 + ord('a'))
        else:
            encrypted_char = char
        encrypted_text += encrypted_char
    return encrypted_text