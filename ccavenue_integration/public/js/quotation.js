frappe.ui.form.on('Quotation', {
    refresh:frm=>{
        if(!frm.doc.taxes_and_charges && frm.doc.docstatus < 1){
            frm.set_value("taxes_and_charges", 'Output GST In-state - BC')
        }
        if (frm.doc.docstatus == 1 && (frappe.user.has_role("Purchase Admin") || frappe.user.has_role("System Manager"))){
            frm.add_custom_button(__("Send Payment Link"), () => {
				frappe.call({
                    method : "ccavenue_integration.IFRAME_KIT.process_payment.send_email_link",
                    args : {
                        docname : frm.doc.name
                    },
                    callback : () =>{

                    }
                })
			});
        }
    },
    
})

frappe.ui.form.on('Payment Schedule', {
    generate_payment_link:(frm, cdt, cdn)=>{
        if (frm.doc.docstatus != 1){
            frappe.throw({message:__("First Submit the document."), title:__("Message")})
        }
        if (frm.doc.__unsaved){
            frappe.throw({message:__("First Save the document."), title:__("Message")})
        }
        if (!frm.doc.custom_ccavenue_invoice_id){
            let d = locals[cdt][cdn]
            frappe.call({
                method : "ccavenue_integration.IFRAME_KIT.process_payment.trigger_partial_ccavanue_payments",
                args : {
                    doc : frm.doc,
                    grand_total : d.payment_amount
                },
                callback:(r)=>{
                    if (r.message){
                        frappe.msgprint("Payment link is successfulli generate")
                    }
                }
            })
        }
    }
})