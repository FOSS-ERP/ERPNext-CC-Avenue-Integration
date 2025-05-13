import frappe
import json
import requests

from frappe.utils import getdate, get_datetime, now
from ccavenue_integration.IFRAME_KIT.ccavRequestHandler import ccav_request_handler
from ccavenue_integration.IFRAME_KIT.ccavutil import encrypt, decrypt
from pay_ccavenue import CCAvenue
from Crypto.Random import get_random_bytes
from datetime import datetime
from erpnext.selling.doctype.quotation.quotation import make_sales_order


def get_parameters():
    quotations = frappe.db.get_list(
        "Quotation",
        filters={"custom_ccavenue_invoice_id": ["!=", ""]},
        pluck="name"
    )

    if not quotations:
        return

    cc_settings = frappe.get_cached_doc("CCAvenue Settings")
    if not cc_settings.enable:
        return

    key = cc_settings.working_key
    url = "https://api.ccavenue.com/apis/servlet/DoWebTrans"

    for quotation_name in quotations:
        doc = frappe.get_doc("Quotation", quotation_name)

        if not doc.custom_ccavenue_invoice_id:
            continue

        form_data = {
            "from_date": doc.transaction_date.strftime('%d-%m-%Y'),
            "to_date": getdate().strftime('%d-%m-%Y'),
            "invoice_id": doc.custom_ccavenue_invoice_id,
            "page_count": "1"
        }

        encrypted_data = encrypt(form_data, key)
        payload = {
            "request_type": "JSON",
            "access_code": cc_settings.access_code,
            "command": "invoiceList",
            "version": "1.1",
            "response_type": "JSON",
            "enc_request": encrypted_data
        }

        try:
            response = requests.post(url, data=payload)
            encrypted_response = response.text.split('=')[2]
            decrypted_data = decrypt(encrypted_response, key)
            json_data = json.loads(decrypted_data)
            print(json_data)
            invoice_list = json_data.get('invoice_List')
            if not invoice_list:
                continue

            invoice_info = invoice_list[0]
            order_amt = invoice_info.get("order_Amt")
            gross_amt = invoice_info.get("order_Gross_Amt")
            status = invoice_info.get("invoice_status")
            status_datetime = invoice_info.get("order_Status_Date_time")

            # Confirmed Payment handling
            payment_ref = frappe.db.exists("Confirmed Payment", {'reference_id': quotation_name})
            if not payment_ref:
                payment_confirm_doc = frappe.get_doc({
                    "doctype": "Confirmed Payment",
                    "reference_id": quotation_name,
                    "paid_amount": gross_amt,
                    "invoice_status": status
                })
                payment_confirm_doc.insert(ignore_permissions=True)
            else:
                cp_doc = frappe.get_doc("Confirmed Payment", payment_ref)
                if cp_doc.invoice_status != status:
                    cp_doc.invoice_status = status
                    cp_doc.last_checked_time = invoice_info.get('order_Date_time')
                    cp_doc.save()

            # Create Sales Order if payment is successful
            if (
                gross_amt
                and status == "Successful"
                and doc.status != "Ordered"
                and order_amt == doc.grand_total
                and not frappe.db.exists("Sales Order Item", {"prevdoc_docname": quotation_name})
            ):
                if doc.quotation_to == "Lead" and frappe.db.exits("Customer", {"lead_name" : doc.party_name}):
                    validate_party_address(doc)
                sales_order = make_sales_order(source_name=quotation_name)
                sales_order.payment_schedule[0].due_date = getdate()
                sales_order.delivery_date = getdate()
                sales_order.save()
                sales_order.submit()

                # Update Quotation with payment info
                doc.paid_amount = gross_amt
                doc.custom_payment_status = status
                doc.custom_payment_received_date = get_datetime(status_datetime)
                doc.save()
            elif (gross_amt and status == "Successful" and (doc.custom_payment_status != "Successful" or not doc.custom_payment_received_date)  and order_amt == doc.grand_total):
                doc.custom_payment_status = "Successful"
                doc.paid_amount = order_amt
                doc.custom_payment_received_date = get_datetime(status_datetime)
                doc.save()
            if (status == "Successful" and doc.order_type == "Shopping Cart"):
                for row in doc.items:
                    if row.item_code in ["Digital Learning", "Testing Shoping Cart"]:
                        cource_list = frappe.db.get_list("LMS Course", pluck="name")
                        for d in cource_list:
                            le_doc = frappe.new_doc("LMS Enrollment")
                            le_doc.course = d
                            le_doc.member = doc.owner
                            le_doc.insert()
            frappe.db.commit()

        except Exception as e:
            frappe.log_error(title="CCAvenue Payment Sync Failed", message=frappe.get_traceback())


# from ccavenue_integration.IFRAME_KIT.invoice_lookup import get_parameters
#{"invoice_List":[{"invoice_Id":4544188405,"reference_no":"","invoice_ref_no":"SAL-QTN-2024-00669","invoice_Created_By":"API","order_No":"","order_Type":"","order_Currency":"INR","order_Amt":1.0,"order_Date_time":"","order_Notes":"","order_Ip":"","order_Status":"","order_Bank_Response":"","order_Bank_Mid":"","order_Bank_Ref_No":"","order_Fraud_Status":"","order_Status_Date_time":"","order_Card_Type":"","order_Card_Name":"","order_Gtw_Id":"","order_Gross_Amt":0.0,"order_Discount":0.0,"order_Capt_Amt":0.0,"order_Fee_Perc":0.0,"order_Fee_Perc_Value":0.0,"order_Fee_Flat":0.0,"order_Tax":0.0,"order_Delivery_Details":"","order_Bill_Name":"","order_Bill_Address":"","order_Bill_Zip":"","order_Bill_Tel":"","order_Bill_Email":"","order_Bill_Country":"","order_Bill_City":"","order_Bill_State":"","order_Ship_Name":"","order_Ship_Address":"","order_Ship_Country":"","order_Ship_Tel":"","order_Ship_City":"","order_Ship_State":"","order_Ship_Zip":"","order_Ship_Email":"","order_Bill_Exp_Date_time":"2024-10-09 17:46:30.15","invoice_status":"Pending","sub_acc_id":""}],"error_Desc":"","page_count":1,"total_records":1,"error_code":""}

def validate_party_address(doc):
    if customer := frappe.db.exits("Customer", {"lead_name" : doc.party_name}):
        address_doc = frappe.get_doc("Address", doc.customer_address)
        customer_links = False
        for row in address_doc.links:
            if row.link_doctype == "Customer" and row.link_name == customer:
                customer_links = True
                break
        if not customer_links:
            address_doc.append("links", {
                "link_doctype" : "Customer",
                "link_name" : customer
            })
            address_doc.save()