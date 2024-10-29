import frappe
from ccavenue_integration.IFRAME_KIT.ccavRequestHandler import ccav_request_handler
import json

def get_quotation(doc):
    form_data = {
                "customer_name": doc.customer_name,
                "customer_email_id": doc.contact_email,
                "customer_email_subject": "Quotation",
                "customer_mobile_no":"7990225354",
                "valid_for": 2,
                "valid_type": "days",
                "bill_delivery_type":"EMAIL",
                "currency": doc.currency,
                "merchant_reference_no": doc.name,
                "merchant_reference_no1": doc.name,
                "merchant_reference_no2": doc.name,
                "merchant_reference_no3": doc.name,
                "merchant_reference_no4": doc.name,
            }

    item_List = []
    taxes = []
    for row in doc.items:
        item_List.append({
                "name": row.item_code,
                "description": row.item_code,
                "quantity": row.qty,
                "unit_cost": row.rate,
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
    form_data["item_List"] = item_List

    print(type(form_data))

    data =  json.dumps(form_data)
    
    response = ccav_request_handler(data, "generateInvoice")

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


