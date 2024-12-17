frappe.ui.form.on('Quotation', {
    refresh:frm=>{
        if(!frm.doc.taxes_and_charges && frm.doc.docstatus < 1){
            frm.set_value("taxes_and_charges", 'Output GST In-state - BC')
        }
    },
    
})