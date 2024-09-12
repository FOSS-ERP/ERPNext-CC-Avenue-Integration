import frappe
from frappe import _
from ccavenue_integration.IFRAME_KIT.ccavutil import encrypt , decrypt
from string import Template
from Crypto.Random import get_random_bytes
import json
from frappe.utils import now
from pay_ccavenue import CCAvenue


access_code = 'AVVN05LG82AH39NVHA'
WORKING_KEY = '44A32D0608BE8D3263A9D0F4E859592E' 
ACCESS_CODE = 'AVVN05LG82AH39NVHA'
MERCHANT_CODE = '2689730'
REDIRECT_URL = "https://bc.fosscrm.com/api/method/.ccavenue_integration.IFRAME_KIT.ccavRequestHandler.ccav_response_handler"
CANCEL_URL = "https://bc.fosscrm.com/api/method/.ccavenue_integration.IFRAME_KIT.ccavRequestHandler.ccav_response_handler"
command = "orderStatusTracker"

def get_status_data():
    doc = frappe.get_doc("CCAvenue Settings")
    if doc.enable:
        access_code = doc.access_code
        WORKING_KEY = doc.working_key
        ACCESS_CODE = doc.access_code
        MERCHANT_CODE = doc.merchant_code
        REDIRECT_URL = doc.redirect_url
        CANCEL_URL = doc.cancel_url
        
        form_data = {
            "order_no":"4467687448",
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

        print(response)

        response = response.text.split('=')[2]

        data = decrypt(response, key)

        return data