import re
import base64
import hashlib
from urllib.parse import unquote

def ghici_strat(s):
    if "%" in s:
        return "url"
    if re.fullmatch(r"[0-9a-fA-F]+", s) and len(s) % 2 == 0:
        return "hex"
    if re.fullmatch(r"[A-Za-z0-9+/=]+", s):
        return "base64"
    return "necunoscut"

def desfa(s):
    strat = ghici_strat(s)
    if strat == "base64":
        return strat, base64.b64decode(s)
    elif strat == "hex":
        return strat, bytes.fromhex(s)
    elif strat == "url":
        return strat, unquote(s).encode()
    return strat, s.encode()


print(desfa("U2FsdXQ=")) 
print(desfa("48656c6c6f")) 


def citibil(b):
    
    return all(32 <= c < 127 for c in b)

val = "NTM1OTU3NTk="
for _ in range(8):
    strat, b = desfa(val)
    if citibil(b):
        print("Găsit text citibil:", b.decode())
        break
    else:
        val = b.decode("utf-8", errors="ignore")

        
date = open("probe/xor.bin", "rb").read()
for k in range(256):
    clar = bytes(b ^ k for b in date)
    if citibil(clar):
        print("cheie:", k, clar.decode())
        break

    tinta = open("probe/hashuri.txt").readline().strip()
print("Lungime hash tinta:", len(tinta))

with open("probe/wordlist.txt", encoding="latin1") as f:
    for cuv in f:
        cuv = cuv.strip().replace("_", "")
        if hashlib.md5(cuv.encode()).hexdigest() == tinta:
            print("Parola gasita:", cuv)
            break

import os
import re
import base64
import hashlib
import json
import argparse
from urllib.parse import unquote

def citibil(b):
    return all(32 <= c < 127 for c in b)

def ghici_strat(s):
    if "%" in s:
        return "url"
    if re.fullmatch(r"[0-9a-fA-F]+", s) and len(s) % 2 == 0:
        return "hex"
    if re.fullmatch(r"[A-Za-z0-9+/=]+", s):
        return "base64"
    return "necunoscut"

def desfa(s):
    strat = ghici_strat(s)
    if strat == "base64":
        return strat, base64.b64decode(s)
    elif strat == "hex":
        return strat, bytes.fromhex(s)
    elif strat == "url":
        return strat, unquote(s).encode()
    return strat, s.encode()

def decodifica_multiplu(val):
    for _ in range(8):
        strat = ghici_strat(val)
        if strat == "necunoscut":
            break
        strat, b = desfa(val)
        try:
            val_noua = b.decode("utf-8")
            if ghici_strat(val_noua) != "necunoscut":
                val = val_noua
                continue
        except Exception:
            pass
            
        if citibil(b):
            return strat, b
        val = b.decode("utf-8", errors="ignore")
    return "necunoscut", val.encode()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Decoder universal forensics")
    parser.add_argument("intrare", nargs="?", default="probe/mesaj.txt", help="Sir sau cale catre fisier")
    parser.add_argument("--fisier", action="store_true", help="Trateaza intrarea ca fisier")
    args = parser.parse_args()

    if args.fisier or os.path.exists(args.intrare):
        with open(args.intrare, "r", encoding="utf-8", errors="ignore") as f:
            valoare_initiala = f.read().strip()
    else:
        valoare_initiala = args.intrare

    strat, rezultat_bytes = decodifica_multiplu(valoare_initiala)
    rezultat_text = rezultat_bytes.decode("utf-8", errors="ignore")
    
    print(f"[*] Strat final: {strat}")
    print(f"[*] Rezultat decodat: {rezultat_text}")

    
    os.makedirs("arsenal/forensics", exist_ok=True)
    fisa = {
        "strat": strat,
        "rezultat": rezultat_text
    }
    with open("arsenal/forensics/fisa.json", "w", encoding="utf-8") as jf:
        json.dump(fisa, jf, indent=4)
    print("[*] Fisa salvata in arsenal/forensics/fisa.json")