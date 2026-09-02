import os
import re

import VerifPdf
import Log

ACCEPTED_PROGRAMS = [
	"Elio_Muxis_V1",
	"Dichroique_940-1310",
]

DICRO_PROGRAM = "Dichroique_940-1310"
DEFAULT_PROGRAM = "Elio_Muxis_V1"

def _is_dicro_folder(path : str):
	folder_name = os.path.basename(os.path.normpath(path))
	return folder_name.upper().endswith("DICRO")

def _get_expected_program_for_folder(path : str):
	if _is_dicro_folder(path):
		return DICRO_PROGRAM
	return DEFAULT_PROGRAM

def _normalize_program_name(prog : str):
	if prog is None:
		return None
	p = prog.strip().lower()
	if p.endswith('.rule'):
		p = p[:-5]
	return p

def _program_variations(program : str):
	norm = _normalize_program_name(program)
	return [
		program.lower(),
		program.lower().replace('_', ' '),
		f"{program.lower()}.rule",
		f"{program.lower().replace('_', ' ')}.rule",
		norm,
		f"{norm}.rule",
	]

def _get_accepted_programs(program = None):
	accepted = list(ACCEPTED_PROGRAMS)
	if program:
		p = program.strip()
		if p and p not in accepted:
			accepted.append(p)
	return accepted

def _find_accepted_program_in_text(text : str, accepted_programs):
	text_lower = text.lower()
	for prog in accepted_programs:
		for variation in _program_variations(prog):
			if variation in text_lower:
				return prog
	return None

def _match_accepted_program(prog : str, accepted_programs):
	prog_lower = prog.lower()
	prog_norm = _normalize_program_name(prog)
	for expected in accepted_programs:
		expected_norm = _normalize_program_name(expected)
		if prog_norm == expected_norm:
			return expected
		if expected_norm in prog_lower:
			return expected
	return None

def _normalize_sn(sn : str):
	if sn is None:
		return None
	try:
		# Enlever l'extension .pdf si présente
		if sn.endswith('.pdf'):
			sn = sn[:-4]
		# Enlever les suffixes _SE, _E, _RCI à la fin
		sn_normalise = re.sub(r'_(?:SE|E|RCI)$', '', sn, flags=re.IGNORECASE)
		# Certains noms de fichiers embarquent la voie après le SN (ex: 1073_940).
		# Pour la comparaison SN, on ne garde que la partie SN.
		sn_normalise = re.sub(r'^(\d+)_\d{2,4}$', r'\1', sn_normalise)
		# Normaliser les séparateurs : convertir les points en tirets pour comparaison
		# "37.24.05" devient "37-24-05" pour correspondre à "37-24-05"
		sn_normalise = sn_normalise.replace('.', '-')
		return sn_normalise
	except Exception:
		return sn

def VerifyFolder(path : str, program = None) :

	global problems

	if not os.path.isdir(path) :
		Log.Error(f"Le chemin {path} n'est pas correct")
		return False
	
	errorHappened = False
	seen_sns = set()

	expected_program = _get_expected_program_for_folder(path)
	if program:
		expected_program = program.strip()
	accepted_programs = [expected_program]

	if _is_dicro_folder(path):
		Log.Message(f"Dossier DICRO détecté — profil attendu: {DICRO_PROGRAM}")
	else:
		Log.Message(f"Dossier standard — profil attendu: {DEFAULT_PROGRAM}")
	
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
			

		# Recherche intelligente du SN dans le PDF
		snInPdf = None
		
		if sn != None:
			sn_norm_attendu = _normalize_sn(sn)
			text_lower = text.lower()
			
			# 1. Recherche directe : chercher le SN attendu dans le texte (avec variations)
			sn_variations = [
				sn_norm_attendu,
				sn_norm_attendu.replace('-', '.'),
				sn_norm_attendu.replace('.', '-'),
				f"SN{sn_norm_attendu}",
				f"SN.{sn_norm_attendu.replace('-', '.')}",
				f"S/N {sn_norm_attendu}",
			]
			
			for variation in sn_variations:
				if variation.lower() in text_lower:
					allSnsInPdf = VerifPdf.GetAllSnsFromString(text)
					for sn_candidat in allSnsInPdf:
						sn_candidat_norm = _normalize_sn(sn_candidat)
						if sn_candidat_norm == sn_norm_attendu:
							snInPdf = sn_candidat
							break
					if snInPdf:
						break
			
			# 2. Si pas trouvé directement, chercher parmi tous les SN trouvés
			if snInPdf == None:
				allSnsInPdf = VerifPdf.GetAllSnsFromString(text)
				if len(allSnsInPdf) > 0:
					# Chercher celui qui correspond après normalisation
					for sn_candidat in allSnsInPdf:
						sn_candidat_norm = _normalize_sn(sn_candidat)
						if sn_candidat_norm == sn_norm_attendu:
							snInPdf = sn_candidat
							break
					
					# Si aucun ne correspond exactement, chercher celui qui contient le SN attendu
					if snInPdf == None:
						for sn_candidat in allSnsInPdf:
							sn_candidat_norm = _normalize_sn(sn_candidat)
							if sn_norm_attendu in sn_candidat_norm or sn_candidat_norm in sn_norm_attendu:
								snInPdf = sn_candidat
								break
					
					# Si toujours rien et plusieurs SN trouvés, préférer le plus court
					if snInPdf == None and len(allSnsInPdf) > 1:
						sns_courts = [s for s in allSnsInPdf if len(s) < 20]
						if sns_courts:
							snInPdf = min(sns_courts, key=len)
							Log.Warning(f"Plusieurs SN trouvés dans {thing.name}: {allSnsInPdf}. Utilisation du plus court: {snInPdf}")
						else:
							snInPdf = allSnsInPdf[0]
					elif snInPdf == None:
						snInPdf = allSnsInPdf[0]
		else:
			snInPdf = VerifPdf.GetSnFromString(text)

		if snInPdf == None :
			Log.Error(f"N'a pas pu trouver le SN dans le pdf {thing.name}")
			errorHappened = True
		
		# Vérification d'égalité SN nom vs PDF
		if sn != None and snInPdf != None:
			sn_norm = _normalize_sn(sn)
			sn_pdf_norm = _normalize_sn(snInPdf)
			if sn_norm == sn_pdf_norm:
				Log.Message("SN: ok")
			else:
				Log.Error(f"Le fichier {thing.name} a SN{sn} dans le nom mais SN{snInPdf} à l'intérieur")
				errorHappened = True
		

		progsInPdf = VerifPdf.GetAllProgsFromString(text)
		accepted_label = expected_program

		prog_trouve = _find_accepted_program_in_text(text, accepted_programs)

		if not prog_trouve and progsInPdf:
			for prog in progsInPdf:
				match = _match_accepted_program(prog, accepted_programs)
				if match:
					prog_trouve = match
					break

			if not prog_trouve:
				progs_filtres = [p for p in progsInPdf if len(p) >= 8]
				if progs_filtres:
					prog_complet = max(progs_filtres, key=len)
					match = _match_accepted_program(prog_complet, accepted_programs)
					if match:
						prog_trouve = match
						if len(progsInPdf) > 1:
							Log.Warning(f"Plusieurs programmes trouvés dans {thing.name}: {progsInPdf}. Utilisation du programme complet: {prog_complet}")

		if prog_trouve:
			Log.Message(f"Profil: ok ({prog_trouve})")
		elif len(progsInPdf) == 0:
			if _is_dicro_folder(path):
				Log.Error(f"PDF égaré ? Dossier DICRO mais profil {DICRO_PROGRAM} absent dans {thing.name}")
			else:
				Log.Error(f"N'a pas pu trouver le profil dans le pdf {thing.name} (attendu: {accepted_label})")
			errorHappened = True
		else:
			prog_detecte = max(progsInPdf, key=len) if len(progsInPdf) > 1 else progsInPdf[0]
			if _is_dicro_folder(path):
				Log.Error(f"PDF égaré ? Dossier DICRO, profil attendu {DICRO_PROGRAM} mais trouvé {prog_detecte} dans {thing.name}")
			elif _match_accepted_program(prog_detecte, [DICRO_PROGRAM]):
				Log.Error(f"PDF égaré ? Profil {DICRO_PROGRAM} trouvé dans un dossier non-DICRO ({thing.name})")
			else:
				Log.Error(f"Le fichier {thing.name} n'a pas le bon profil (attendu: {accepted_label}, trouvé: {prog_detecte})")
			errorHappened = True
		

		FAIL_STR = "FAIL"

		if FAIL_STR in text :
			Log.Error(f"Le fichier {thing.name} n'est pas dans les specs")
			errorHappened = True
		else:
			Log.Message("Conformité: ok")
		

	
	return not errorHappened