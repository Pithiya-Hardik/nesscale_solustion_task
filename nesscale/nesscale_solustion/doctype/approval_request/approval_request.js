frappe.ui.form.on('Approval Request', {
    onload:function(frm){
        var current_user = frappe.session.user;
        frm.set_value('requestor', current_user);
    },
    refresh: function(frm) {
        if (frm.doc.status === "Submitted" && !frm.doc.current_approver) {
            console.log("this calll")
            frappe.call({
                method: 'nesscale.nesscale_solustion.doctype.approval_request.approval_request.initialize_approval',
                args: {
                    doc: frm.doc
                },
                callback: function(r) {
                    if (!r.exc) {
                        frm.reload_doc();
                    }
                }
            });
        }
    },
    after_save: function(frm) {
        frappe.call({
            method: 'nesscale.nesscale_solustion.doctype.approval_request.approval_request.process_approval',
            args: {
                doc: frm.doc
            },
            callback: function(r) {
                if (!r.exc) {
                    frm.reload_doc();
                }
            }
        });
    }
});

