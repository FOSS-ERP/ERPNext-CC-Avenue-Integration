import frappe
from frappe import _
from ccavenue_integration.IFRAME_KIT.ccavutil import encrypt , decrypt
from string import Template
from Crypto.Random import get_random_bytes
import json
from frappe.utils import now
from pay_ccavenue import CCAvenue



def update_payment_status():
    data = frappe.db.sql(f"""
                Select name, custom_ccavenue_invoice_id
                From `tabQuotation` 
                Where docstatus = 1 and custom_payment_status = "Unpaid"
    """, as_dict=1)

    for row in data:
        responce = get_status_data(row.custom_ccavenue_invoice_id)
        print(responce)

def get_status_data(custom_ccavenue_invoice_id):
    doc = frappe.get_doc("CCAvenue Settings")
    if doc.enable:
        access_code = doc.access_code
        WORKING_KEY = doc.working_key
        ACCESS_CODE = doc.access_code
        MERCHANT_CODE = doc.merchant_code
        REDIRECT_URL = doc.redirect_url
        CANCEL_URL = doc.cancel_url
        command = "orderStatusTracker"



        form_data = {
            "order_no": custom_ccavenue_invoice_id,
        }
        ccavenue = CCAvenue(WORKING_KEY, ACCESS_CODE, MERCHANT_CODE, REDIRECT_URL, CANCEL_URL)
        key = WORKING_KEY
                
        encrypted_data = encrypt(form_data, key)

        import requests

        url = "https://api.ccavenue.com/apis/servlet/DoWebTrans"

        payload = {
            "request_type": "JSON",
            "access_code": ACCESS_CODE,
            "command": command,
            "version": "1.2",
            "response_type": "JSON",
            "enc_request": encrypted_data
        }
        
        response = requests.post(url, data=payload, headers={})

        response = response.text.split('=')[2]

        data = decrypt(response, key)

        return data