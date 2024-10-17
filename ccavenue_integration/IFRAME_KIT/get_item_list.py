import frappe
from ccavenue_integration.IFRAME_KIT.ccavRequestHandler import ccav_request_handler
import json
import frappe
from frappe import _
from ccavenue_integration.IFRAME_KIT.ccavutil import encrypt , decrypt
from string import Template
from Crypto.Random import get_random_bytes
import json
from frappe.utils import now
from pay_ccavenue import CCAvenue


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
            "response_type": "JSON",
        }

        import requests
        response = requests.post(url, data=payload, headers={})
        
        response = response.text.split('=')[2]

        data = decrypt(response, key)

        json_data = json.loads(data)

        print(json_data["Invoice_Item_Result"]["item_List"]["item"])

        for row in json_data["Invoice_Item_Result"]["item_List"]["item"]:
            if frappe.db.exists("Item", row.get('name')):
                continue
            else:
                print(row.name)

        # return data
