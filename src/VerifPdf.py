import re
import pypdf


# Amélioration du regex pour capturer SN/SN variantes (SN, S/N) suivies d'un séparateur optionnel et de l'identifiant
# La capture exige au moins un chiffre pour éviter des faux positifs (ex: 'Device')
# Supporte les points et tirets comme séparateurs : SN.37.24.05 ou SN37-24-05
SN_REGEX = re.compile(r"(?:S/?N)\s*[:\-°\.]*\s*((?=[\w\-\.]*\d)[\w\-\.]+)", re.IGNORECASE)

PROG_REGEX = re.compile(r"[\w\s,-]+\.rule")

"""
Attempt to read the pdf and extract all the text in it, in all pages.
Returns a string on success, and None otherwise
"""
def GetPdfText(path : str) :

    try :

        reader = pypdf.PdfReader(path)
        
        pages = reader.pages

        result = ""
        for page in pages :
            try:
                page_text = page.extract_text()
                if page_text:
                    result += page_text
            except Exception as e:
                print(e)

        return result
    
    except Exception as e :
        print(e)
        return None


"""
Finds the SN number in a string
"""
def GetSnFromString(string : str) :
    match = SN_REGEX.search(string)
    if match is not None:
        sn = match.group(1).strip()
        # Enlever l'extension .pdf si présente (pour les noms de fichiers)
        if sn.endswith('.pdf'):
            sn = sn[:-4]
        # On ignore les cas où le SN est vide ou égal à 'SN'
        if sn and sn.upper() != 'SN':
            return sn
        else:
            return None
    else:
        return None


def GetAllSnsFromString(string : str) :
    """Trouve tous les SN dans une chaîne"""
    if string is None:
        return []
    try:
        matches = SN_REGEX.findall(string)
        sns = []
        for sn in matches:
            sn_clean = sn.strip()
            if sn_clean and sn_clean.upper() != 'SN':
                sns.append(sn_clean)
        return sns
    except Exception:
        return []



def GetProgFromString(string : str) :
    match = PROG_REGEX.search(string)

    if match != None :
        res = match.group(0)
        return res
    else : return None


def GetAllProgsFromString(string : str) :
    if string is None:
        return []
    try:
        return PROG_REGEX.findall(string)
    except Exception:
        return []

