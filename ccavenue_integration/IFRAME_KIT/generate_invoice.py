import frappe
from ccavenue_integration.IFRAME_KIT.ccavRequestHandler import ccav_request_handler
import json

def get_quotation(doc):
    form_data = {
            "customer_name": "{0}".format(doc.customer_name),
            "customer_email_id": "{0}".format("viral.kansodiya77@gmail.com"),
            "customer_email_subject": "Invoice",
            "customer_mobile_no": "{0}".format(doc.contact_mobile),
            "valid_for": "2",
            "valid_type": "days",
            "currency": "{0}".format(doc.currency),
            "merchant_reference": "{0}-1".format(doc.name),
            "merchant_reference_no1": "{0}-2".format(doc.name),
            "merchant_reference_no2": "{0}-3".format(doc.name),
            "merchant_reference_no3": "{0}-4".format(doc.name),
            "merchant_reference_no4": "{0}-5".format(doc.name),
            "sub_acc_id": "sub1",
            "amount" : "{0}".format(doc.grand_total),
            # "due_date" : 1,
            # "late_payment_fees" : 1,
            # "late_payment_fees_type" : "Flat",
            "item_List": [],
            "terms_and_conditions": "terms and condition",
            "sms_content": "Pls payyourLegalEntity_Namebill#Invoice_IDfor Invoice_Currency Invoice_Amount online at Pay_Link."
        }

    item_List = []
    taxes = []
    for row in doc.items:
        item_List.append({
                "name": "{0}".format(row.item_code),
                "description": "{0}".format(row.item_code),
                "quantity": row.qty,
                "unit_cost": row.rate-200,
                "tax_List": [
                    {
                    "name": "CGST",
                    "amount": 9.0
                    },
                    {
                    "name": "SGST",
                    "amount": 9.0
                    }
                ]
            })
    form_data.update({"item_List" : item_List})
   
    json_string = json.dumps(form_data, indent=4)
    
    print(json_string)

    response = ccav_request_handler(json_string, "generateInvoice")

    print(response)



def get_date_format(date_str):
    from datetime import datetime


    # Convert to datetime object
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")

    day_with_suffix = add_ordinal_suffix(date_obj.day)

    # Format the date to "15th Jan 2024"
    formatted_date = f"{day_with_suffix} {date_obj.strftime('%b %Y')}"

    return formatted_date


def add_ordinal_suffix(day):
    if 11 <= day <= 13:
        return f"{day}th"
    last_digit = day % 10
    if last_digit == 1:
        return f"{day}st"
    elif last_digit == 2:
        return f"{day}nd"
    elif last_digit == 3:
        return f"{day}rd"
    else:
        return f"{day}th"

# Get day with ordinal suffix


