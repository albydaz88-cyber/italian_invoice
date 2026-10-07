import frappe


def execute():
	if frappe.db.exists("Tipologia di documento e-Invoice", "TD16"):
		frappe.db.set_value("Tipologia di documento e-Invoice", "TD16", "tipologia", "AutoFattura")