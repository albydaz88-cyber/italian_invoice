import frappe

# Serie assegnate in automatico. Qualsiasi altra serie (es. DR/.YY./ dei
# corrispettivi) è una scelta esplicita dell'utente e non va toccata.
SERIE_AUTOMATICHE = {"SINV/.YY./", "PAINV/.YY./", "NCINV/.YY./"}


def execute(doc, method=None):
	"""Assegna la naming series in base al tipo di cliente/documento, lato server.

	Eseguito in `before_naming` (gira durante set_new_name, PRIMA di validate): è
	l'unico punto in cui la naming series è ancora modificabile per il nome del
	documento. Garantisce la serie PAINV per le Pubbliche Amministrazioni su TUTTI
	i canali di creazione (Desk, API, integrazione OpenAPI, import) — il JS client
	da solo non basta perché viene bypassato dalle creazioni server-side.

	Una serie diversa da quelle automatiche (es. DR/.YY./ dei corrispettivi) è una
	scelta deliberata dell'utente e viene rispettata.
	"""
	# Le rettifiche (amend) conservano la serie del documento originale.
	if doc.amended_from:
		return

	# Serie scelta esplicitamente dall'utente: non sovrascrivere.
	if doc.naming_series and doc.naming_series not in SERIE_AUTOMATICHE:
		return

	if doc.is_return:
		doc.naming_series = "NCINV/.YY./"
		return

	is_pa = frappe.db.get_value("Customer", doc.customer, "is_public_administration")
	doc.naming_series = "PAINV/.YY./" if is_pa else "SINV/.YY./"
