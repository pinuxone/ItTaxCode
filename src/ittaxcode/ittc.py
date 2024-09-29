from datetime import datetime, date
import re

# riporto in formato standard numerico eventuali omocodie
def omocodie (codfisc):
    caratteri = {
        "L": "0",
        "M": "1",
        "N": "2",
        "P": "3",
        "Q": "4",
        "R": "5",
        "S": "6",
        "T": "7",
        "U": "8",
        "V": "9"
    }

    # Lo porto in maiuscolo
    codfisc = codfisc.upper()

    # Nelle posizioni dove sono le x, qualora si trovi un carattere, va sostituito con il numero per le omocodie
    mask = "cccnnnxxMxx*xxxC"

    codfisco = ""
    lungo = len(codfisc)

    # Spazzolo tutta la stringa e ne creo una "ripulita" dai caratteri
    # eventualmente presenti per la gestione delle omocodie
    for x in range(0, lungo):
        dgt_cod = codfisc[x:x+1]
        dgt_mask = mask[x:x+1]
        if dgt_mask == "x":
            try:
                # dovrei mettere un'altra if
                # ed operare soltanto se dgt_cod fosse stringa
                # ma tanto se non lo è, fallisce la riga sottostante
                # e nulla cambia! ;)
                dgt_cod = caratteri[dgt_cod]
            except:
                # se non trova omocodia lascia il carattere invariato
                pass

        codfisco = codfisco + dgt_cod

    return codfisco


# estraggo giorno e sesso
def birthdate(codfisc):
    codfisco = omocodie(codfisc)

    mesi = {
        "A": "01",
        "B": "02",
        "C": "03",
        "D": "04",
        "E": "05",
        "H": "06",
        "L": "07",
        "M": "08",
        "P": "09",
        "R": "10",
        "S": "11",
        "T": "12"
    }

    # estrazione giorno
    cf_giorno = codfisco[9:11]
    if int(cf_giorno) > 40:
        cf_giorno = f'{int(cf_giorno) - 40:02}'

    # estrazione anno
    cf_mese = mesi[codfisco[8:9]]

    # estrazione anno
    cf_anno = codfisco[6:8]
    anno_attuale = str(datetime.now().year)[2:]
    if int(cf_anno) > int(anno_attuale):
        cf_anno = "19" + cf_anno

    else:
        cf_anno = "20" + cf_anno

    cf_nascita = date(int(cf_anno), int(cf_mese), int(cf_giorno))
    return cf_nascita


# estraggo il sesso
def sex(codfisc):
    codfisco = omocodie(codfisc)
    # estrazione sesso dal giorno
    cf_giorno = codfisco[9:11]
    cf_sesso = "M"
    if int(cf_giorno) > 40:
        cf_sesso = "F"

    return cf_sesso


# estraggo l'età compiuta
def age(codfisc):
    cf_nascita = birthdate(codfisc)
    # d1 = datetime.strptime(cf_nascita, "%Y-%m-%d")
    oggi = datetime.now().date()
    periodo = int(abs((oggi - cf_nascita).days) / 365.2425)
    return periodo


# Controllo il check digit sul codice raw, dunque senza ripulirlo dalle omocodie
def check(codfisc):
    risultato = False
    cf = codfisc.upper()
    cfo = omocodie(codfisc)
    lungo = len(cf)
    if lungo != 16:
        return risultato

    # è lungo 16, testo regexp
    p = re.compile('[A-Z][A-Z][A-Z][A-Z][A-Z][A-Z][0-9][0-9][A-Z][0-9][0-9][A-Z][0-9][0-9][0-9][A-Z]')
    m = p.match(cfo)
    if m is None:
        return risultato

    maxdays = {
        "A": 31,
        "B": 29,
        "C": 31,
        "D": 30,
        "E": 31,
        "H": 30,
        "L": 31,
        "M": 31,
        "P": 30,
        "R": 31,
        "S": 30,
        "T": 31
    }

    # La lettera del mese è conosciuta?
    cod_mese = cf[8:9]
    if not cod_mese in maxdays.keys():
        return risultato

    # Per il mese specificato i giorni sono giusti?
    days = int(cfo[9:11])
    # Se donna...
    if int(days) > 40:
        days = int(f'{int(days) - 40:02}')
    # Se troppi giorni in quel mese...
    if days > maxdays[cod_mese]:
        return risultato

    # Se arrivo sin qui, controllo pure il checkdigit
    pari = {
        "0": 0,
        "1": 1,
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "A": 0,
        "B": 1,
        "C": 2,
        "D": 3,
        "E": 4,
        "F": 5,
        "G": 6,
        "H": 7,
        "I": 8,
        "J": 9,
        "K": 10,
        "L": 11,
        "M": 12,
        "N": 13,
        "O": 14,
        "P": 15,
        "Q": 16,
        "R": 17,
        "S": 18,
        "T": 19,
        "U": 20,
        "V": 21,
        "W": 22,
        "X": 23,
        "Y": 24,
        "Z": 25
    }

    dispari = {
        "0": 1,
        "1": 0,
        "2": 5,
        "3": 7,
        "4": 9,
        "5": 13,
        "6": 15,
        "7": 17,
        "8": 19,
        "9": 21,
        "A": 1,
        "B": 0,
        "C": 5,
        "D": 7,
        "E": 9,
        "F": 13,
        "G": 15,
        "H": 17,
        "I": 19,
        "J": 21,
        "K": 2,
        "L": 4,
        "M": 18,
        "N": 20,
        "O": 11,
        "P": 3,
        "Q": 6,
        "R": 8,
        "S": 12,
        "T": 14,
        "U": 16,
        "V": 10,
        "W": 22,
        "X": 25,
        "Y": 24,
        "Z": 23
    }

    decodifica = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    # posizione pari o dispari?
    flag = False
    somma = 0
    # somma valori corrispondenti
    for t in range(0, lungo-1):
        if flag:
            somma = somma + pari[cf[t:t+1]]

        else:
            somma = somma + dispari[cf[t:t+1]]

        flag = not flag

    resto = somma % 26
    if decodifica[resto:resto+1] == cf[15:16]:
        risultato = True

    return risultato
