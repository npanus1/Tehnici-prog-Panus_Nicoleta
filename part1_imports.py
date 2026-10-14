# Laborator: functii, metode si importuri pe web 
# Student: Panuș Nicoleta

import time
import urllib.request

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10 #secunde

# ex 1
import requests
print("Exercitiul 1:")
print (f"Versiune requests: {requests.__version__}\n")

#ex 2
from requests import get
res_style2=get(BASE_URL, timeout=TIMEOUT)
print("Exercitiul 2:")
print(f"Stilul 2 Status Code: {res_style2.status_code}")
print(f"Stilul 2 Sttus Code: {res_style2.status_code}\n")

#ex 3
import requests as rq
res_alias=rq.get(BASE_URL, timeout=TIMEOUT)
print("Exercitiul 3:")
print(f"Alias Status Code: {res_alias.status_code}\n")

#ex 4
print("Exercitiul 4:")
req = urllib.request.Request(
    BASE_URL, 
    headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
)

with urllib.request.urlopen(req, timeout=TIMEOUT) as response:
    status_code = response.status
    raw_bytes = response.read()
    html_text = raw_bytes.decode("utf-8")

    print(f"Urllib Status Code: {status_code}")
    print("Primele 200 de caractere din corp:")
    print(html_text[:200])
    print("-" * 50 + "\n")

    #ex 5
    print("Exercitiul 5:")
    dir_contents=dir(requests)
    print("Alegem 3 elemente din requests dir(): 'get', 'Response', 'exceptions'")
    print("-"*50+"\n")

    #ex 6
    print("Exercitiul 6:")
    res_timeout=requests.get(BASE_URL, timeout=TIMEOUT)
    print(f"Cerere executata cu parametrul timeout={TIMEOUT}. Status: {res_timeout.status_code}\n")

    #ex 7
    print("Exercitiul 7:")
    t_start=time.perf_counter()
    res_timed=requests.get(BASE_URL, timeout=TIMEOUT)
    t_end=time.perf_counter()
    durata_masurata=t_end-t_start
    durata_elapsed=res_timed.elapsed.total_seconds()
    print(f"Durata masurata cu perf_counter(): {durata_masurata:.4f} secunde")
    print(f"Durata din response.elapsed: {durata_elapsed:.4f} secunde")
    print("-"*50+"\n")

    #ex 8
    print("Exercitiul 8:")
    try:
        import bs4
    except ImportError:
        print("Instalati modulul cu: pip install beautifulsoup4")
        print("\n Verificare cunostine")
