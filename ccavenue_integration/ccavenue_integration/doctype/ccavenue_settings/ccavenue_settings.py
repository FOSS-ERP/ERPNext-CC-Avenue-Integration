# Copyright (c) 2024, Viral Kansodiya and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from ccavenue_integration.ccavenue_integration.generate_ecommerce_payments import process_full_payment_invoice

class CCAvenueSettings(Document):
	def validate_transaction_currency(self, currency):
		print(currency)
		return
	def get_payment_url(self, **kwargs):
		args = frappe._dict(kwargs)
		payment_request = args.reference_docname

		reference_name = frappe.db.get_value("Payment Request", payment_request, "reference_name")

		doc = frappe.get_doc("Sales Order", reference_name)
		quotation = doc.items[0].prevdoc_docname

		qo_doc = frappe.get_doc("Quotation", quotation)

		return process_full_payment_invoice(qo_doc)

		



