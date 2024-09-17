import frappe
from frappe.utils import getdate, now
from ccavenue_integration.IFRAME_KIT.ccavRequestHandler import ccav_request_handler
import json
from ccavenue_integration.IFRAME_KIT.ccavutil import encrypt , decrypt
from pay_ccavenue import CCAvenue
from Crypto.Random import get_random_bytes
from datetime import datetime

# ccavenue.py


def get_parameters():
    doc = frappe.get_doc("Quotation", "SAL-QTN-2024-00015")

    from_date = doc.transaction_date.strftime('%d-%m-%Y')

    to_date = getdate().strftime('%d-%m-%Y')

    form_data = {
        "from_date": from_date,
        "to_date": to_date,
        "invoice_Id": "4486111418",
        "page_count": "1"
        }

    # form_data = {
    #     "to_date" : getdate(),
    #     "invoice_no" : doc.name,
    #     "reference_no" : doc.custom_ccavenue_invoice_id,
    #     "page_no":1
    # }

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
        print("enc : " , encrypted_data)
        
        url = "https://api.ccavenue.com/apis/servlet/DoWebTrans"

        payload = {
            "request_type": "JSON",
            "access_code": ACCESS_CODE,
            "command": "invoiceList",
            "version": "1.1",
            "response_type": "JSON",
            "enc_request": encrypted_data
        }

        try:
            response = requests.post(url, data=payload, headers={})
            
            print("CCAvenue :", response)
            print("text : ", response.text)
            
            response = response.text.split('=')[2]
            
            print(response)
            
            data = decrypt(response, key)
            return data
        except Exception as e:
            frappe.log_error(response)
            frappe.log_error(e)

