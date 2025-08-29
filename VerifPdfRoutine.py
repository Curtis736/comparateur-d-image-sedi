import os
import re

import VerifPdf
import Log

def _normalize_program_name(prog : str):
	if prog is None:
		return None
	p = prog.strip().lower()
	if p.endswith('.rule'):
		p = p[:-5]
	return p

def _normalize_sn(sn : str):
	if sn is None:
		return None
	try:
		return re.sub(r'_(?:SE|E)$', '', sn, flags=re.IGNORECASE)
	except Exception:
		return sn

def VerifyFolder(path : str, program = str) :

	global problems

	if not os.path.isdir(path) :
		Log.Error(f"Le chemin {path} n'est pas correct")
		return False
	
	errorHappened = False
	seen_sns = set()
	
	for thing in os.scandir(path) :

		if not thing.is_file() : continue

		if not thing.name.lower().endswith(".pdf") :
			Log.Warning(f"Le fichier {thing.name} n'est pas un PDF — ignoré")
			continue
		 
		Log.Message(f"Traitement du fichier: {thing.name}")

		sn = VerifPdf.GetSnFromString(thing.name)
		if sn == None :
			Log.Error(f"Pas de SN détecté dans le nom du fichier {thing.name}")
			errorHappened = True
		else :
			sn_key = _normalize_sn(sn)
			if sn_key in seen_sns :
				Log.Warning(f"SN dupliqué détecté (base): {sn_key} dans le fichier {thing.name}")
			else :
				seen_sns.add(sn_key)
			

		text = VerifPdf.GetPdfText(os.path.join(path, thing.name))

		if text == None :
			Log.Error(f"Impossible d'extraire le texte du fichier {thing.name}")
			errorHappened = True
			continue
		
		if not text.strip():
			Log.Warning(f"Aucun texte extrait du fichier {thing.name} (peut-être un scan sans OCR)")
			continue
			

		# EXTRACTION ET LOG DU PROFILE
	

		snInPdf = VerifPdf.GetSnFromString(text)

		# Recherche de secours: si motif introuvable, tenter le SN du nom en recherche simple (insensible à la casse)
		if snInPdf == None and sn != None:
			try:
				if _normalize_sn(sn).lower() in text.lower():
					Log.Message(f"SN: ok")
					snInPdf = sn
			except Exception:
				pass

		if snInPdf == None :
			Log.Error(f"N'a pas pu trouver le SN dans le pdf {thing.name}")
			errorHappened = True
		
		# Vérification d'égalité SN nom vs PDF (OK simple si tout va bien)
		if sn != None and snInPdf != None:
			sn_norm = _normalize_sn(sn)
			sn_pdf_norm = _normalize_sn(snInPdf)
			if sn_norm == sn_pdf_norm:
				Log.Message("SN: ok")
			else:
				Log.Error(f"Le fichier {thing.name} a SN{sn} dans le nom mais SN{snInPdf} à l'intérieur")
				errorHappened = True
		

		progsInPdf = VerifPdf.GetAllProgsFromString(text)
		text_lower = text.lower()
		expected_norm = _normalize_program_name(program) if program else None

		if len(progsInPdf) == 0 :
			if program:
				# Fallback: accepter la présence du nom attendu sans le suffixe .rule
				if expected_norm and (expected_norm in text_lower):
					Log.Message("Programme: ok")
				else:
					Log.Error(f"N'a pas pu trouver le programme dans le pdf {thing.name}")
					errorHappened = True
			else:
				Log.Message(f"Aucun programme .rule détecté dans {thing.name} (aucun programme attendu spécifié)")
		else :
			if len(progsInPdf) > 1 :
				Log.Warning(f"Plusieurs programmes trouvés dans {thing.name}: {progsInPdf}. Utilisation du premier.")
			progInPdf = progsInPdf[0]
			prog_norm = _normalize_program_name(progInPdf)

			if program and (prog_norm != expected_norm):
				# Dernière vérification: le nom attendu apparaît-il dans le texte ?
				if not (expected_norm and expected_norm in text_lower):
					Log.Error(f"Le fichier {thing.name} n'a pas le bon programme (attendu: {program}, trouvé: {progInPdf})")
					errorHappened = True
				else:
					Log.Message("Programme: ok")
			elif program:
				Log.Message("Programme: ok")
			elif not program:
				Log.Message(f"Programme détecté dans {thing.name}: {progInPdf} (aucun programme attendu spécifié)")
		

		FAIL_STR = "FAIL"

		if FAIL_STR in text :
			Log.Error(f"Le fichier {thing.name} n'est pas dans les specs")
			errorHappened = True
		else:
			Log.Message("Conformité: ok")
		

	
	return not errorHappened