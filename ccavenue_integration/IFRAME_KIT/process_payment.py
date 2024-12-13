import frappe
import json
from frappe.utils import now
from ccavenue_integration.IFRAME_KIT.generate_invoice import process_full_payment_invoice
from ccavenue_integration.ccavenue_integration.quotation import process_partial_payment

def trigger_ccavanue_payments(self, method):
    if not self.is_partial_payment_quotation:
        process_full_payment_invoice(self)

@frappe.whitelist()
def trigger_partial_ccavanue_payments(doc, grand_total):
    doc = json.loads(doc)
    doc['grand_total'] =  grand_total
    try:
        response = process_partial_payment(frappe._dict(doc))
        frappe.msgprint("Payment link generated successfully")
        # frappe.db.set_value("Quotation", doc.get('name'), "custom_payment_url", response.get("custom_payment_url"))
        frappe.db.set_value("Quotation", doc.get('name'), "custom_ccavenue_invoice_id", response.get("custom_ccavenue_invoice_id"))
        frappe.db.set_value("Quotation", doc.get('name'), "custom_proforma_invoice_date", now())
        return "Success"
    except:
        frappe.log_error("error")

