import frappe
import json
from frappe.utils import now
from ccavenue_integration.IFRAME_KIT.generate_invoice import process_full_payment_invoice
from ccavenue_integration.ccavenue_integration.quotation import process_partial_payment

def trigger_ccavanue_payments(self, method):
    aggr = False
    if self.opportunity:
        doc = frappe.get_doc("Opportunity", self.opportunity)
        if len(doc.custom_aggregator) > 0:
            for row in doc.custom_aggregator:
                if row.get("aggregator_name") ==  "Retail":
                    aggr = True
        else:
            frappe.throw("Please Update Aggregator in Opportunity {0}".format(self.opportunity))
    if not self.is_partial_payment_quotation and aggr:
        process_full_payment_invoice(self)

@frappe.whitelist()
def trigger_partial_ccavanue_payments(doc, grand_total):
    doc = json.loads(doc)
    doc['grand_total'] =  grand_total
    currency = doc.get('currency')
    try:
        response = process_partial_payment(frappe._dict(doc))
        frappe.msgprint("Payment link generated successfully")
        frappe.db.set_value("Quotation", doc.get('name'), "custom_payment_url", response.get("custom_payment_url"))
        frappe.db.set_value("Quotation", doc.get('name'), "custom_ccavenue_invoice_id", response.get("custom_ccavenue_invoice_id"))
        frappe.db.set_value("Quotation", doc.get('name'), "custom_proforma_invoice_date", now())
        message = f"""
            <table width="800" border="0" align="center" cellpadding="0" cellspacing="0">
        <tbody>
        <tr>
            <td align="center" valign="top" style="font-family:Arial,Helvetica,sans-serif;font-size:12px;color:#373737;background-color:#fff;padding:20px;border:solid 1px #bcc2cf">
                <table width="100%" border="0" cellspacing="0" cellpadding="0">
                    <tbody>
                    <tr>
                        <td align="left" valign="top" style="font-family:Arial,Helvetica,sans-serif;font-size:11px;color:#373737;background-color:#fff;padding:15px 20px;border:solid 1px #dbdfe6">
                            <table width="100%" border="0" cellspacing="0" cellpadding="0">
                                <tbody>
                                <tr>
                                    <td width="55%" height="18" align="left" valign="top">	{doc.get("company")}											</td>
                                    <td width="45%" rowspan="3" align="right" valign="top" style="font-family:Arial,Helvetica,sans-serif;font-size:11px;color:#373737">
                                        <table width="95%" border="0" cellspacing="0" cellpadding="5" style="border:solid 1px #e4e6eb;border-left-width:0px;border-bottom-width:0px">
                                            <tbody>
                                            <tr>
                                                <td width="50%" align="right" valign="top" style="font-family:Arial,Helvetica,sans-serif;font-size:11px;color:#373737;border-left:solid 1px #e4e6eb;border-bottom:solid 1px #e4e6eb">
                                                        <strong>Proforma Invoice No.:</strong>															</td>
                                                <td width="50%" align="left" valign="top" style="font-family:Arial,Helvetica,sans-serif;font-size:11px;color:#373737;border-left:solid 1px #e4e6eb;border-bottom:solid 1px #e4e6eb">
                                                    {response.get("custom_ccavenue_invoice_id")}
                                                </td>
                                            </tr>
                                            <tr>
                                                <td align="right" valign="top" style="font-family:Arial,Helvetica,sans-serif;font-size:11px;color:#373737;border-left:solid 1px #e4e6eb;border-bottom:solid 1px #e4e6eb">
                                                    <strong>Enterprise Name &amp; Address:</strong>
                                                </td>
                                                <td align="left" valign="top" style="font-family:Arial,Helvetica,sans-serif;font-size:11px;color:#373737;border-left:solid 1px #e4e6eb;border-bottom:solid 1px #e4e6eb;word-break:break-all;table-layout:fixed">{doc.get("name")}</td>
                                            </tr>
                                            <tr>
                                                <td align="right" valign="top" style="font-family:Arial,Helvetica,sans-serif;font-size:11px;color:#373737;border-left:solid 1px #e4e6eb;border-bottom:solid 1px #e4e6eb">																<strong>Customer GST number:</strong>														</td>
                                                <td align="left" valign="top" style="font-family:Arial,Helvetica,sans-serif;font-size:11px;color:#373737;border-left:solid 1px #e4e6eb;border-bottom:solid 1px #e4e6eb;word-break:break-all;table-layout:fixed">{doc.get("custom_customer_gstin")}</td>
                                            </tr>
                                            <tr>
                                                <td align="right" valign="top" style="font-family:Arial,Helvetica,sans-serif;font-size:11px;color:#373737;border-left:solid 1px #e4e6eb;border-bottom:solid 1px #e4e6eb">																<strong>Date:</strong>															</td>
                                                <td align="left" valign="top" style="font-family:Arial,Helvetica,sans-serif;font-size:11px;color:#373737;border-left:solid 1px #e4e6eb;border-bottom:solid 1px #e4e6eb">{now()}</td>
                                            </tr>
                                            </tbody>
                                        </table>
                                    </td>
                                </tr>
                                <tr>
                                    <td height="10" align="left" valign="top"><img src="https://ci3.googleusercontent.com/meips/ADKq_NYvDs41vFlQUiFaSMyyQPUr3Pl4ULqpgal7c5d3qDw6aRvgmi4hRSkdId1ZEf2M4nip_RCQj2ELlkmvqzNsvfsY8-9g7EfnrsMzPI9FZQ=s0-d-e1-ft#https://login.ccavenue.com/apis//images/blank_spacer.gif" width="1" height="10" class="CToWUd" data-bit="iit"></td>
                                </tr>
                                <tr>
                                    <td height="18" align="left" valign="top" style="font-family:Arial,Helvetica,sans-serif;font-size:11px;color:#373737;line-height:16px"><strong>CATALYST MANAGEMENT SERVICES PVT LTD</strong><br>25 4TH FLOOR RAGHAVENDRA NILAYA 1ST MAIN ROAD AECS LAYOUT BENGALURU KARNATAKA<br><strong>Telephone: </strong>9945972835&nbsp;&nbsp;|&nbsp;&amp;nbsp<strong>Email:</strong> <a href="mailto:business.catalyst@catalysts.org" target="_blank">business.catalyst@catalysts.<wbr>org</a><br><strong>PAN No.:</strong> AAACF3153A</td>
                                </tr>
                                </tbody>
                            </table>
                            <br>										
                            <table width="100%" border="0" cellspacing="0" cellpadding="0">
                                <tbody>
                                <tr>
                                    <td height="35" align="left" valign="middle" style="font-family:Arial,Helvetica,sans-serif;font-size:11px;color:#373737"><strong>Customer Name: </strong>FOSS ERP<strong>&nbsp;&nbsp;|&nbsp;&nbsp;Email: </strong><a href="mailto:viral@fosserp.com" target="_blank">{doc.get("contact_email")}</a><br></td>
                                </tr>
                                </tbody>
                            </table>
                            <table width="760" border="0" cellpadding="6" cellspacing="0" style="border:solid 1px #e4e6eb;border-left-width:0px;border-bottom-width:0px">
                                <tbody>
                                <tr>
                                    <td align="left" valign="top" style="font-family:Arial,Helvetica,sans-serif;font-size:11px;font-weight:bold;color:#373737;background-color:#f7f7f7;border-left:solid 1px #e4e6eb;border-bottom:solid 1px #e4e6eb">Items</td>
                                    <td align="left" valign="top" style="font-family:Arial,Helvetica,sans-serif;font-size:11px;font-weight:bold;color:#373737;background-color:#f7f7f7;border-left:solid 1px #e4e6eb;border-bottom:solid 1px #e4e6eb">Description</td>
                                    <td align="left" valign="top" style="font-family:Arial,Helvetica,sans-serif;font-size:11px;font-weight:bold;color:#373737;background-color:#f7f7f7;border-left:solid 1px #e4e6eb;border-bottom:solid 1px #e4e6eb">Curr.</td>
                                    <td align="right" valign="top" style="font-family:Arial,Helvetica,sans-serif;font-size:11px;font-weight:bold;color:#373737;background-color:#f7f7f7;border-left:solid 1px #e4e6eb;border-bottom:solid 1px #e4e6eb">	Unit Cost</td>
                                    <td align="right" valign="top" style="font-family:Arial,Helvetica,sans-serif;font-size:11px;font-weight:bold;color:#373737;background-color:#f7f7f7;border-left:solid 1px #e4e6eb;border-bottom:solid 1px #e4e6eb">Qty.</td>
                                    <td align="right" valign="top" style="font-family:Arial,Helvetica,sans-serif;font-size:11px;font-weight:bold;color:#373737;background-color:#f7f7f7;border-left:solid 1px #e4e6eb;border-bottom:solid 1px #e4e6eb">Tax1</td>
                                    <td align="right" valign="top" style="font-family:Arial,Helvetica,sans-serif;font-size:11px;font-weight:bold;color:#373737;background-color:#f7f7f7;border-left:solid 1px #e4e6eb;border-bottom:solid 1px #e4e6eb">Tax2</td>
                                    <td align="right" valign="top" style="font-family:Arial,Helvetica,sans-serif;font-size:11px;font-weight:bold;color:#373737;background-color:#f7f7f7;border-left:solid 1px #e4e6eb;border-bottom:solid 1px #e4e6eb">Line Total</td>
                                </tr>
        """
        for row in doc.get('items'):
            message += f"""
                 <tr>
                    <td align="left" valign="top" style="font-family:Arial,Helvetica,sans-serif;font-size:11px;color:#373737;border-left:solid 1px #e4e6eb;border-bottom:solid 1px #e4e6eb">{row.get('item_name')}</td>
                    <td align="left" valign="top" style="font-family:Arial,Helvetica,sans-serif;font-size:11px;color:#373737;border-left:solid 1px #e4e6eb;border-bottom:solid 1px #e4e6eb">{row.get('description')}</td>
                    <td align="left" valign="top" style="font-family:Arial,Helvetica,sans-serif;font-size:11px;color:#373737;border-left:solid 1px #e4e6eb;border-bottom:solid 1px #e4e6eb">INR</td>
                    <td align="right" valign="top" style="font-family:Arial,Helvetica,sans-serif;font-size:11px;color:#373737;border-left:solid 1px #e4e6eb;border-bottom:solid 1px #e4e6eb">{frappe.utils.fmt_money(doc.get("rate"), currency=currency)}</td>
                    <td align="right" valign="top" style="font-family:Arial,Helvetica,sans-serif;font-size:11px;color:#373737;border-left:solid 1px #e4e6eb;border-bottom:solid 1px #e4e6eb">{row.get("qty")}</td>
                    <td align="right" valign="top" style="font-family:Arial,Helvetica,sans-serif;font-size:11px;color:#373737;border-left:solid 1px #e4e6eb;border-bottom:solid 1px #e4e6eb">SGST {doc.get('taxes')[0].get('rate')}%<br>(INR {frappe.utils.fmt_money(doc.get("taxes")[0].get("tax_amount"), currency=currency)})</td>
                    <td align="right" valign="top" style="font-family:Arial,Helvetica,sans-serif;font-size:11px;color:#373737;border-left:solid 1px #e4e6eb;border-bottom:solid 1px #e4e6eb">CGST {doc.get('taxes')[1].get('rate')}%<br>(INR {frappe.utils.fmt_money(doc.get("taxes")[1].get("tax_amount"), currency=currency)})</td>
                """
            total_amount = row.get("amount") + doc.get("taxes")[0].get("tax_amount") + doc.get("taxes")[1].get("tax_amount")
            message += f"""
                    <td align="right" valign="top" style="font-family:Arial,Helvetica,sans-serif;font-size:11px;color:#373737;border-left:solid 1px #e4e6eb;border-bottom:solid 1px #e4e6eb">{frappe.utils.fmt_money(total_amount, currency=currency)}</td>
                </tr>
            """
        message += f"""        
                                    <tr>
                                        <td colspan="4" align="left" valign="top">&nbsp;</td>
                                        <td colspan="3" align="left" valign="middle" style="font-family:Arial,Helvetica,sans-serif;font-size:11px;font-weight:bold;color:#373737;background-color:#f7f7f7;border-left:solid 1px #e4e6eb;border-bottom:solid 1px #e4e6eb">Total Payable Amount</td>
                                        <td align="right" valign="top" style="font-family:Arial,Helvetica,sans-serif;font-size:11px;font-weight:bold;color:#373737;background-color:#f7f7f7;border-left:solid 1px #e4e6eb;border-bottom:solid 1px #e4e6eb;border-left-width:0px">{frappe.utils.fmt_money(doc.get("base_grand_total"), currency=currency)}</td>
                                    </tr>
                                    </tbody>
                                </table>
                                <br>	<br><strong>Terms &amp; Conditions:<br></strong>	At Business Catalyst, we ensure transparency &amp; fairness through the following policy:
                                - Clients may request a change to their originally paid service if the service delivery has not commenced.
                                - Service changes are subject to availability &amp; must be of equal/lesser value than the originally paid service.
                                - Once service delivery has begun, payments made for services are non-refundable.<br><br>										
                                <table width="100%" border="0" cellspacing="0" cellpadding="0">
                                    <tbody>
                                    <tr>
                                        <td align="left" valign="top" style="font-family:Arial,Helvetica,sans-serif;font-size:11px;color:#373737">	This is a digitally generated invoice, hence it does not require signature.<br>	<br></td>
                                    </tr>
                                    </tbody>
                                </table>
                            </td>
                        </tr>
                        </tbody>
                    </table>
                </td>
            </tr>
            </tbody>
        </table>
            """
        frappe.sendmail(recipients=[doc.get("contact_email")], content=message, subject="Business Catalyst service")

        return "Success"
    except:
        frappe.log_error("error")

