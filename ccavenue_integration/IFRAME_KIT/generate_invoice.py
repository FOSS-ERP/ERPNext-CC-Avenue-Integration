import frappe
from ccavenue_integration.IFRAME_KIT.ccavRequestHandler import ccav_request_handler
import json

def get_quotation(doc):
    form_data = {
            "customer_name": doc.customer_name,
            "customer_email_id": doc.contact_email,
            "customer_email_subject": "Quotation",
            "customer_mobile_no": doc.contact_mobile,
            "valid_for": 5,
            "valid_type": "days",
            "due_date" : str(doc.valid_till), 
            "bill_delivery_type":"EMAIL",
            "currency": doc.currency,
            "amount": doc.grand_total,
            "merchant_reference_no": doc.name,
            "merchant_reference_no1": doc.name,
            "merchant_reference_no2": doc.name,
            "merchant_reference_no3": doc.name,
            "merchant_reference_no4": doc.name,
        }
    item_List = []
    for row in doc.items:
        item_List.append({
            "name" : row.item_code,
            "description" : row.description,
            "quantity" : row.qty,
            "unit_cost"  : row.rate,
            "tax_List" : []
         })
    form_data.update({'item_List' : item_List})

    print(form_data)

    response = ccav_request_handler(form_data, "generateInvoice")

    print(response)