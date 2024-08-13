access_code = "AVVN05LG82AH39NVHA"
working_key = "44A32D0608BE8D3263A9D0F4E859592E"
form_data = {
    "customer_name":"Viral Patel",
    "customer_email_id":"viral@fosserp.com",
    "customer_email_submit" : "Quotation",
    "valid_for":2,
    "valid_type":"days",
    "Currency":"INR",
    "amount":4000,
    "customer_mobile_no":7990225354,
    "due_date" : "11th Aug 2024",
}

import requests

url = "https://apitest.ccavenue.com/apis/servlet/DoWebTrans"
payload = {
    "merchant_id":"2689730",
	"access_code": "AVVN05LG82AH39NVHA",
    "request_type": "JSON",
    "command": "generateInvoice",
    "version": "1.2",
    "enc_request": ""
}
response = requests.post(url, data=payload, headers={})

print(response.text)