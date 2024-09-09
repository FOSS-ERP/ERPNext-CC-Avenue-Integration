import frappe
from ccavenue_integration.IFRAME_KIT.ccavRequestHandler import ccav_request_handler
import json

def before_submit(self, method):
    if frappe.db.get_single_value('CCAvenue Settings', 'enable'):
        doc = frappe.get_doc("CCAvenue Settings")
        form_data = {
                "merchant_id": doc.merchant_code,
                "customer_id": self.party_name,
                "customer_name": self.customer_name,
                "customer_email_id": self.contact_email,
                "customer_email_subject": "Quotation",
                "valid_for": 2,
                "valid_type": "days",
                "currency": self.currency,
                "bill_delivery_type":"EMAIL",
                "amount": self.grand_total,
                "customer_mobile_no": self.contact_mobile,
                "merchant_reference_no": self.name,
                "sub_acc_id": "sub1",
                "terms_and_conditions": "terms and condition",
                "due_date": "3",
                "late_payment_fees": "0",
                "late_payment_fees_type": "Perc",
                "discount_if_paid_within_due_date": "4",
                "discount_value": "0",
                "discount_type": "Perc",
                "sms_content": "PlspayyourLegalEntity_Namebill#Invoice_IDforInvoice_Currency Invoice_Amount online at Pay_Link."
            }
        form_data = json.dumps(form_data)
        response = ccav_request_handler(form_data)
        try:
            response = json.loads(response)
            self.custom_payment_url = response.get('tiny_url')
            self.custom_ccavenue_invoice_id = response.get('invoice_id')
        except Exception as e:
            frappe.log_error(response)
            frappe.log_error(e)

def test_ccavenue(quotation):
    if frappe.db.get_single_value('CCAvenue Settings', 'enable'):
        doc = frappe.get_doc("CCAvenue Settings")
        form_data = {
                "merchant_id": doc.merchant_code,
                "customer_id": quotation.get("party_name"),
                "customer_name": quotation.get("customer_name"),
                "customer_email_id": quotation.get("contact_email"),
                "customer_email_subject": "Quotation",
                "valid_for": 2,
                "valid_type": "days",
                "currency": quotation.get("currency"),
                "bill_delivery_type":"EMAIL",
                "amount": quotation.get("grand_total"),
                "customer_mobile_no": quotation.get("contact_mobile"),
                "merchant_reference_no": quotation.get("name"),
                "sub_acc_id": "sub1",
                "terms_and_conditions": "terms and condition",
                "due_date": "3",
                "late_payment_fees": "0",
                "late_payment_fees_type": "Perc",
                "discount_if_paid_within_due_date": "4",
                "discount_value": "0",
                "discount_type": "Perc",
                "sms_content": "PlspayyourLegalEntity_Namebill#Invoice_IDforInvoice_Currency Invoice_Amount online at Pay_Link."
            }
        response = ccav_request_handler(form_data)
        try:
            print(response)
            response = json.loads(response)
            custom_payment_url = response.get('tiny_url')
            custom_ccavenue_invoice_id = response.get('invoice_id')
            print(custom_payment_url)
            print(custom_ccavenue_invoice_id)
        except Exception as e:
            frappe.log_error(response)
            frappe.log_error(e)
            