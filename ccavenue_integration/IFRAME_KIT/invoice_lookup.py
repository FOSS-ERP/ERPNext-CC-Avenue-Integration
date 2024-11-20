import frappe
from frappe.utils import getdate, now, get_datetime
from ccavenue_integration.IFRAME_KIT.ccavRequestHandler import ccav_request_handler
import json
from ccavenue_integration.IFRAME_KIT.ccavutil import encrypt , decrypt
from pay_ccavenue import CCAvenue
from Crypto.Random import get_random_bytes
from datetime import datetime
from erpnext.selling.doctype.quotation.quotation import make_sales_order

# ccavenue.py


def get_parameters():
    get_quotation_list = frappe.db.get_list("Quotation", {"custom_payment_status" : "Pending", "custom_ccavenue_invoice_id" : ["!=" , ""]}, pluck="name")
    get_quotation_list = [ "SAL-QTN-2024-00968", "SAL-QTN-2024-00967"]
    for row in get_quotation_list:
        doc = frappe.get_doc("Quotation", row)
        if not doc.custom_ccavenue_invoice_id:
            continue
        from_date = doc.transaction_date.strftime('%d-%m-%Y')

        to_date = getdate().strftime('%d-%m-%Y')

        form_data = {
            "from_date": from_date,
            "to_date": to_date,
            "invoice_id": doc.custom_ccavenue_invoice_id,
            "page_count": "1"
            }

        cc_doc = frappe.get_doc("CCAvenue Settings")
        if cc_doc.enable:
            access_code = cc_doc.access_code
            WORKING_KEY = cc_doc.working_key
            ACCESS_CODE = cc_doc.access_code
            MERCHANT_CODE = cc_doc.merchant_code
            REDIRECT_URL = cc_doc.redirect_url
            CANCEL_URL = cc_doc.cancel_url

            my_string = WORKING_KEY
            
            key = my_string
                
            encrypted_data = encrypt(form_data, key)

            import requests
            
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
                
                response = response.text.split('=')[2]
                
                data = decrypt(response, key)
                
                json_data = json.loads(data)

                print(json_data)

                order_Gross_Amt = json_data.get('invoice_List')[0].get("order_Gross_Amt")
                invoice_status = json_data.get('invoice_List')[0].get("invoice_status")
                order_Status_Date_time = json_data.get('invoice_List')[0].get("order_Status_Date_time")

                if order_Gross_Amt or invoice_status == "Successful" and doc.status != "Ordered":
                    if frappe.db.get_value("Quotation", row, 'status') != "Ordered":
                        so = make_sales_order(source_name = row)
                        so.payment_schedule[0].due_date = getdate()
                        so.delivery_date = getdate()
                        so.save()
                        so.submit()
                        frappe.db.set_value("Quotation", row, 'paid_amount', order_Gross_Amt)
                        frappe.db.set_value("Quotation", row, 'custom_payment_status', invoice_status)
                        frappe.db.set_value("Quotation", row, 'custom_payment_received_time', get_datetime(order_Status_Date_time))
                        frappe.db.commit()
                if doc.status == "Ordered" and (order_Gross_Amt or invoice_status == "Successful"):
                    frappe.db.set_value("Quotation", row, 'custom_payment_status', invoice_status)
                    frappe.db.commit()
            except Exception as e:
                frappe.log_error(e)


#{"invoice_List":[{"invoice_Id":4544188405,"reference_no":"","invoice_ref_no":"SAL-QTN-2024-00669","invoice_Created_By":"API","order_No":"","order_Type":"","order_Currency":"INR","order_Amt":1.0,"order_Date_time":"","order_Notes":"","order_Ip":"","order_Status":"","order_Bank_Response":"","order_Bank_Mid":"","order_Bank_Ref_No":"","order_Fraud_Status":"","order_Status_Date_time":"","order_Card_Type":"","order_Card_Name":"","order_Gtw_Id":"","order_Gross_Amt":0.0,"order_Discount":0.0,"order_Capt_Amt":0.0,"order_Fee_Perc":0.0,"order_Fee_Perc_Value":0.0,"order_Fee_Flat":0.0,"order_Tax":0.0,"order_Delivery_Details":"","order_Bill_Name":"","order_Bill_Address":"","order_Bill_Zip":"","order_Bill_Tel":"","order_Bill_Email":"","order_Bill_Country":"","order_Bill_City":"","order_Bill_State":"","order_Ship_Name":"","order_Ship_Address":"","order_Ship_Country":"","order_Ship_Tel":"","order_Ship_City":"","order_Ship_State":"","order_Ship_Zip":"","order_Ship_Email":"","order_Bill_Exp_Date_time":"2024-10-09 17:46:30.15","invoice_status":"Pending","sub_acc_id":""}],"error_Desc":"","page_count":1,"total_records":1,"error_code":""}