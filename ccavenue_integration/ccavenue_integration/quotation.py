import frappe
from ccavenue_integration.IFRAME_KIT.ccavRequestHandler import ccav_request_handler
import json

def before_submit(self, method):
    if frappe.db.get_single_value('CCAvenue Settings', 'enable'):
        doc = frappe.get_doc("CCAvenue Settings")
        form_data = {
                "customer_id": self.party_name,
                "customer_name": self.customer_name,
                "customer_email_id": self.contact_email,
                "customer_email_subject": "Quotation",
                "valid_for": 2,
                "valid_type": "days",
                "currency": self.currency,
                "amount": self.grand_total,
                "merchant_reference_no": self.name,
                "merchant_reference_no1": self.name,
                "merchant_reference_no2": self.name,
                "merchant_reference_no3": self.name,
                "merchant_reference_no4": self.name,
                "sub_acc_id": "",
                "terms_and_conditions": "terms and condition",
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
                "customer_id": quotation.party_name,
                "customer_name": quotation.customer_name,
                "customer_email_id": quotation.contact_email,
                "customer_email_subject": "Quotation",
                "valid_for": 2,
                "valid_type": "days",
                "bill_delivery_type":"EMAIL",
                "currency": quotation.currency,
                "amount": quotation.grand_total,
                "merchant_reference_no": quotation.name,
                "merchant_reference_no1": quotation.name,
                "merchant_reference_no2": quotation.name,
                "merchant_reference_no3": quotation.name,
                "merchant_reference_no4": quotation.name,
                "sub_acc_id": "",
                "terms_and_conditions": "terms and condition",
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
            