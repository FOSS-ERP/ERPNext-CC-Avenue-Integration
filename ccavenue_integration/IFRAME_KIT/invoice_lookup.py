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
    get_quotation_list = frappe.db.get_list("Quotation", {"custom_payment_status" : "Unpaid", "custom_ccavenue_invoice_id" : ["!=" , ""]}, pluck="name")

    for row in get_quotation_list:
        doc = frappe.get_doc("Quotation", row)

        from_date = doc.transaction_date.strftime('%d-%m-%Y')

        to_date = getdate().strftime('%d-%m-%Y')

        form_data = {
            "from_date": from_date,
            "to_date": to_date,
            "invoice_id": doc.custom_ccavenue_invoice_id,
            "page_count": "1"
            }

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
                
                if data:
                    order_status = data.get('invoice_List')[0].get("order_Status")
                    print(order_status)
            except Exception as e:
                frappe.log_error(response)
                frappe.log_error(e)

#{"invoice_List":[{"invoice_Id":4544188405,"reference_no":"","invoice_ref_no":"SAL-QTN-2024-00669","invoice_Created_By":"API","order_No":"","order_Type":"","order_Currency":"INR","order_Amt":1.0,"order_Date_time":"","order_Notes":"","order_Ip":"","order_Status":"","order_Bank_Response":"","order_Bank_Mid":"","order_Bank_Ref_No":"","order_Fraud_Status":"","order_Status_Date_time":"","order_Card_Type":"","order_Card_Name":"","order_Gtw_Id":"","order_Gross_Amt":0.0,"order_Discount":0.0,"order_Capt_Amt":0.0,"order_Fee_Perc":0.0,"order_Fee_Perc_Value":0.0,"order_Fee_Flat":0.0,"order_Tax":0.0,"order_Delivery_Details":"","order_Bill_Name":"","order_Bill_Address":"","order_Bill_Zip":"","order_Bill_Tel":"","order_Bill_Email":"","order_Bill_Country":"","order_Bill_City":"","order_Bill_State":"","order_Ship_Name":"","order_Ship_Address":"","order_Ship_Country":"","order_Ship_Tel":"","order_Ship_City":"","order_Ship_State":"","order_Ship_Zip":"","order_Ship_Email":"","order_Bill_Exp_Date_time":"2024-10-09 17:46:30.15","invoice_status":"Pending","sub_acc_id":""}],"error_Desc":"","page_count":1,"total_records":1,"error_code":""}