import frappe
from ccavenue_integration.IFRAME_KIT.ccavRequestHandler import ccav_request_handler
import json
from frappe.utils import flt, getdate, get_datetime


@frappe.whitelist()
def process_full_payment_invoice(self, button=False):
    if not self.grand_total > 0:
        return
    doc = frappe.get_doc("CCAvenue Settings")
    if not len(self.taxes):
        frappe.throw("Taxes are not added in this quotation")
    if not self.contact_mobile and self.customer_address:
        contact_mobile = frappe.db.get_value("Address", self.customer_address, "phone")
    else:
        contact_mobile = self.contact_mobile
    contact_email = self.contact_email
    if not self.contact_email and self.contact_person:
        contact_email = frappe.db.get_value("Contact", self.contact_person, "email_id")
        if not contact_email:
            contact_email = frappe.db.get_value("Contact", self.contact_person, "user")
        
    form_data =  {
        "customer_name": self.customer_name or frappe.db.get_value("User", frappe.session.user, "full_name"),
        "customer_email_id": contact_email ,
        "customer_email_subject": "Invoice",
        "customer_mobile_no": contact_mobile,
        "currency": "INR",
        "valid_for": "2",
        "valid_type": "days",
        "item_List": [],
        "merchant_reference_no": "25 4TH FLOOR RAGHAVENDRA NILAYA 1ST MAIN ROAD AECS LAYOUT BENGALURU KARNATAKA",
        "merchant_reference_no1": self.custom_customer_gstin or self.name,
        "merchant_reference_no2": self.name,
        "merchant_reference_no3": self.name,
        "merchant_reference_no4": self.name,
        "sub_acc_id": "sub1",
        "terms_and_conditions": "terms and condition",
        "sms_content": "Pls payyourLegalEntity_Namebill#Invoice_IDfor Invoice_Currency Invoice_Amount online at Pay_Link."
    }

    
    for row in self.items:
        tax_List = []
        item = {
            "name": row.item_code,
            "description": row.item_code,
            "quantity": str(int(row.qty)),
            "unit_cost": str(row.rate),
        }
        for d in self.taxes:
            if "CGST" in d.description:
                tax_List.append(
                            {
                            "name": "CGST",
                            "amount": str(flt(d.rate))
                            },  
                    )
            if "SGST" in d.description:
                tax_List.append(
                    {
                    "name": "SGST",
                    "amount": str(flt(d.rate))
                    }  
                )
            if "IGST" in d.description:
                tax_List.append(
                            {
                            "name": "IGST",
                            "amount": str(flt(d.rate))
                            }
                    )
        item.update({ "tax_List" : tax_List })
        form_data["item_List"].append(item)

    form_data = json.dumps(frappe._dict(form_data))
    print(form_data)
    response = ccav_request_handler(form_data, "generateInvoice")
    print(response)
    try:
        response = json.loads(response)
        if (response.get("error_desc") != "" and response.get("error_desc")) or response.get("error_code"):
            frappe.throw("Faild to Generate Link, Error Desc : {0}, Error Code : {1}".format(response.get("error_desc"), response.get("error_code")))    
        frappe.db.set_value("Quotation", self.name, "custom_payment_url", response.get('tiny_url'))
        frappe.db.set_value("Quotation", self.name, "custom_ccavenue_invoice_id", response.get('invoice_id'))
        frappe.db.set_value("Quotation", self.name, "custom_proforma_invoice_date", get_datetime())
        frappe.db.commit()
        return response.get('tiny_url')
    except Exception as e:
        frappe.log_error(e)





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


