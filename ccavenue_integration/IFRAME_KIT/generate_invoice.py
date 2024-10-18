import frappe
from ccavenue_integration.IFRAME_KIT.ccavRequestHandler import ccav_request_handler
import json

def get_quotation(doc, due_date):
    form_data = {
            "customer_name": doc.customer_name,
            "customer_email_id": doc.contact_email,
            "customer_email_subject": "Quotation",
            "customer_mobile_no": "7990225354",
            "valid_for": 5,
            "valid_type": "days",
            "due_date" : due_date, 
            "bill_delivery_type":"EMAIL",
            "currency": doc.currency,
            "amount": doc.grand_total,
            "merchant_reference_no": doc.name,
            "merchant_reference_no1": doc.name,
            "merchant_reference_no2": doc.name,
            "merchant_reference_no3": doc.name,
            "merchant_reference_no4": doc.name,
            "late_payment_fees_type": "Flat",
            "late_payment_fees":1,
            "sub_acc_id":"sub1",
            "terms_and_conditions": "terms and condition",
            "sms_content":"Pls pay your LegalEntity_Name bill # Invoice_ID for Invoice_Currency Invoice_Amount online at Pay_Link."
            }

    item_List = []
    taxes = []
    for row in doc.items:
        item_List.append({
            "name" : row.item_code,
            "description" : row.item_name,
            "quantity" : row.qty,
            "unit_cost"  : row.rate,
            "tax_List" : [
                {"name": "CGST","amount": (row.qty * row.rate) * 0.09},
                {"name": "SGST","amount": (row.qty * row.rate) * 0.09}
            ]
         })
    form_data.update({'item_List' : item_List})

    print(form_data)

    form_data = {
                "customer_name": "abc",
                "customer_email_id": "abc@sify.com",
                "customer_email_subject": "Test",
                "customer_mobile_no": "9874561236",
                "currency": "INR",
                "valid_for": "2",
                "valid_type": "days",
                "item_List": [
                    {
                    "name": "ONDC Onboarding",
                    "description": "ONDC Onboarding",
                    "quantity": "1",
                    "unit_cost": "100.00",
                    "tax_List": [
                        {
                        "name": "CGST",
                        "amount": "9.0"
                        },
                        {
                        "name": "SGST",
                        "amount": "9.0"
                        }
                    ]
                    }
                ],
                "merchant_reference": "123456987-SN01",
                "merchant_reference_no1": 123456987-SN01,
                "merchant_reference_no2": 123456987-SN01,
                "merchant_reference_no3": "123456987-SN01",
                "merchant_reference_no4": "123456987-SN01s",
                "sub_acc_id": "sub1",
                "terms_and_conditions": "terms and condition",
                "sms_content": "Pls payyourLegalEntity_Namebill#Invoice_IDfor Invoice_Currency Invoice_Amount online at Pay_Link."
                }

    response = ccav_request_handler(form_data, "generateInvoice")

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


