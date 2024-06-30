frappe.listview_settings['Approval Request'] = {
    has_indicator_for_cancelled: true,
    has_indicator_for_Submitted: true,
    get_indicator(doc)  {
      
        if (doc.docstatus == 1 && doc.status == "Submitted") {
            return [__("Submitted"), "blue", "docstatus,=,1"];
        }
        else if (doc.docstatus == 1 && doc.status == "Approved") {
            return [__("Approved"), "green", "docstatus,=,1"];
        }
        else if(doc.docstatus == 1 && doc.status == "Rejected"){
            return [__("Rejected"), "red", "docstatus,=,1"];
        }
    },
 }
 