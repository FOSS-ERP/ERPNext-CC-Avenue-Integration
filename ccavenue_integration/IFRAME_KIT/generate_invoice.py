import frappe
from ccavenue_integration.IFRAME_KIT.ccavRequestHandler import ccav_request_handler
import json
from frappe.utils import flt

def get_quotation(self, method=None):
    form_data =  {
        "customer_name": self.customer_name,
        "customer_email_id": self.contact_email,
        "customer_email_subject": "Invoice",
        "customer_mobile_no": self.contact_mobile,
        "currency": "INR",
        "valid_for": "2",
        "valid_type": "days",
        "item_List": [],
        "merchant_reference": self.name,
        "merchant_reference_no1": self.name,
        "merchant_reference_no2": self.name,
        "merchant_reference_no3": self.name,
        "merchant_reference_no4": self.name,
        "sub_acc_id": "sub1",
        "terms_and_conditions": "terms and condition",
        "sms_content": "Pls payyourLegalEntity_Namebill#Invoice_IDfor Invoice_Currency Invoice_Amount online at Pay_Link."
    }

    item_List = []
    taxes = []
    for row in self.items:
        for d in self.taxes:
            if "CGST" in d.description or "SGST" in d.description:
                item_List.append({
                        "name": row.item_code,
                        "description": row.item_code,
                        "quantity": str(int(row.qty)),
                        "unit_cost": str(row.rate),
                        "tax_List": [
                            {
                            "name": "CGST",
                            "amount": str(flt(d.rate))
                            },
                            {
                            "name": "SGST",
                            "amount": str(flt(d.rate))
                            }
                        ]
                    })
            if "IGST" in d.description:
                item_List.append({
                        "name": row.item_code,
                        "description": row.item_code,
                        "quantity": str(int(row.qty)),
                        "unit_cost": str(row.rate),
                        "tax_List": [
                            {
                            "name": "IGST",
                            "amount": str(flt(d.rate))
                            }
                        ]
                    })
    form_data.update({ "item_List" : item_List })

    form_data = json.dumps(frappe._dict(form_data))

    response = ccav_request_handler(form_data, "generateInvoice")
    try:
        response = json.loads(response)
        self.custom_payment_url = response.get('tiny_url')
        self.custom_ccavenue_invoice_id = response.get('invoice_id')
    except Exception as e:
        frappe.log_error(response)
        frappe.log_error(e)


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


