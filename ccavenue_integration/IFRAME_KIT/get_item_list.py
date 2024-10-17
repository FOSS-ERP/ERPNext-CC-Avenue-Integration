import frappe
from ccavenue_integration.IFRAME_KIT.ccavRequestHandler import ccav_request_handler
import json

def get_items():
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
        form_data = {}
        encrypted_data = encrypt(form_data, key)
        url = "https://api.ccavenue.com/apis/servlet/DoWebTrans"
        # print(ACCESS_CODE)
        payload = {
            "request_type": "JSON",
            "access_code": ACCESS_CODE,
            "command": "getInvoiceItems",
            "version": "1.2",
            "response_type": "JSON",
            "enc_request": encrypted_data
        }

        try:
            response = requests.post(url, data=payload, headers={})
        
            response = response.text.split('=')[2]

            data = decrypt(response, key)
            return data
        except Exception as e:
            frappe.log_error(response)
            frappe.log_error(e)