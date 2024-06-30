import frappe
import json
from frappe.model.document import Document

class ApprovalRequest(Document):
	pass


@frappe.whitelist()
def initialize_approval(doc):
    doc_data = frappe.parse_json(doc)
    doc = frappe.get_doc(doc_data)
    workflow_settings = frappe.get_doc('Approval Workflow Settings', {'document_type': doc_data['document_type']})
    first_step = min(workflow_settings.approval_steps, key=lambda x: x.sequence)
    doc.current_approver = first_step.approver
    doc.previous_approver = None
    doc.status = 'Submitted'
    doc.save()
    frappe.db.commit()


@frappe.whitelist()
def process_approval(doc):
    doc_data = frappe.parse_json(doc)
    doc = frappe.get_doc(doc_data)
    if doc_data['status'] == 'Approved':
        second_last_doc = frappe.get_last_doc(doc.doctype, {
			'document_id': doc_data['document_id'],
			'name': ('!=', doc_data['name']),
			'status': ('!=', "Rejected")
		})
        workflow_settings = frappe.get_doc('Approval Workflow Settings', {'document_type': doc_data['document_type']})
        previous_sequence = frappe.db.sql("""
				SELECT sequence 
				FROM `tabApproval Step` 
				WHERE approver=%s 
				AND parent=%s
			""", (second_last_doc.current_approver, workflow_settings.name), as_dict=True)
        current_seq = previous_sequence[0]['sequence'] + 1
        current_user = frappe.db.sql(" select approver from `tabApproval Step` where sequence=%s and parent=%s",(current_seq, workflow_settings.name), as_dict=True)
    
        if current_user:
            doc.previous_approver = second_last_doc.current_approver
            doc.current_approver = current_user[0]['approver']
            doc.save()
            frappe.db.commit()
    else:
        pass
        
