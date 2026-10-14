# Laborator: Scrierea propriilor funcții 
# Student: <Panus Nicoleta>

import time
import requests

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde


#ex 21
def fetch(url: str, timeout: int = TIMEOUT) -> requests.Response:
    """Efectuează o cerere GET către URL-ul specificat și returnează obiectul Response."""
    return requests.get(url, timeout=timeout)

print("Exercitiul 21")
resp_21 = fetch(BASE_URL)
print(f"Fetch BASE_URL status code: {resp_21.status_code}")


#ex 22
def get_status(url: str) -> int:
    """Returnează codul de stare HTTP pentru adresa url."""
    response = requests.get(url, timeout=TIMEOUT)
    return response.status_code

print("\nExercițiul 22")
paths = ["/", "/robots.txt", "/sitemap.xml"]
for p in paths:
    full_url = BASE_URL + p
    status = get_status(full_url)
    print(f"URL: {full_url} | Status: {status}")
    time.sleep(1)


#ex 23
def fetch(url: str, timeout: int = 10) -> requests.Response:
    """Efectuează o cerere GET cu un parametru timeout configurabil (implicit 10s)."""
    return requests.get(url, timeout=timeout)

print("\nExercițiul 23")
resp_default = fetch(BASE_URL)
print(f"Apel cu timeout implicit: {resp_default.status_code}")

resp_custom = fetch(BASE_URL, timeout=3)
print(f"Apel cu timeout=3: {resp_custom.status_code}")


#ex 24
def get_title(html: str) -> str:
    """Extrage și curăță titlul dintr-un șir de caractere HTML."""
    start_tag = "<title>"
    end_tag = "</title>"
    start_pos = html.lower().find(start_tag)
    if start_pos == -1:
        return "Fără titlu"
    start_pos += len(start_tag)
    end_pos = html.lower().find(end_tag, start_pos)
    if end_pos == -1:
        return "Fără titlu"
    return html[start_pos:end_pos].strip()

print("\nExercițiul 24")
page_html = fetch(BASE_URL).text
print("Titlu extras cu get_title():", get_title(page_html))


#ex 25
print("\nExercițiul 25")
help(get_title)

#ex 26
print("\nExercițiul 26")
try:
    print("Se apelează get_status(123)...")
    get_status(123)
except Exception as e:
    print(f"Eroare la runtime: {e}")
    print("Explicație: Adnotările de tip în Python sunt doar informative și nu blochează executarea.")


#ex 27
def page_exists(url: str) -> bool:
    """Verifică dacă o pagină există și returnează True/False fără a arunca excepții."""
    try:
        response = requests.get(url, timeout=TIMEOUT)
        return response.status_code < 400
    except requests.RequestException:
        return False

print("\nExercițiul 27")
invalid_url = "https://this-domain-does-not-exist.invalid"
print(f"Pagina {BASE_URL} există?: {page_exists(BASE_URL)}")
print(f"Pagina {invalid_url} există?: {page_exists(invalid_url)}")


#ex 28
def check_paths(base: str, paths: list) -> dict:
    """Verifică o listă de căi relative și returnează un dicționar {path: status_code}."""
    results = {}
    for path in paths:
        full_url = base.rstrip("/") + "/" + path.lstrip("/")
        try:
            res = requests.get(full_url, timeout=TIMEOUT)
            results[path] = res.status_code
        except requests.RequestException:
            results[path] = 0
        time.sleep(1)
    return results

print("\nExercițiul 28")
test_paths = ["/", "/robots.txt", "/sitemap.xml"]
print("Rezultat check_paths:", check_paths(BASE_URL, test_paths))


#ex 29
def get_header(url: str, name: str, default: str = "lipsește") -> str:
    """Returnează valoarea unui antet HTTP specificat sau valoarea implicită dacă lipsește."""
    try:
        res = requests.get(url, timeout=TIMEOUT)
        return res.headers.get(name, default)
    except requests.RequestException:
        return default

print("\nExercițiul 29")
server_val = get_header(BASE_URL, name="Server")
print(f"Antetul 'Server' pentru {BASE_URL}: {server_val}")


#ex 30
def security_headers(url: str) -> dict:
    """Verifică prezența a 5 antete de securitate esențiale."""
    headers_to_check = [
        "Strict-Transport-Security",
        "Content-Security-Policy",
        "X-Frame-Options",
        "X-Content-Type-Options",
        "Referrer-Policy"
    ]
    try:
        res = requests.get(url, timeout=TIMEOUT)
        return {h: h in res.headers for h in headers_to_check}
    except requests.RequestException:
        return {h: False for h in headers_to_check}

print("\nExercițiul 30")
sec_res = security_headers(BASE_URL)
print("Antete de securitate:", sec_res)


#ex 31
def score_headers(results: dict) -> str:
    """Calculează scorul antetelor prezente în formatul 'X/Y'."""
    total = len(results)
    passed = sum(1 for present in results.values() if present)
    return f"{passed}/{total}"

print("\nExercițiul 31")
score = score_headers(security_headers(BASE_URL))
print(f"Scor securitate antete: {score}")


#ex 32
def fetch_robots(base: str) -> str | None:
    """Returnează conținutul fișierului /robots.txt sau None dacă nu există/eșuează."""
    robots_url = base.rstrip("/") + "/robots.txt"
    try:
        res = requests.get(robots_url, timeout=TIMEOUT)
        if res.status_code == 200:
            return res.text
        return None
    except requests.RequestException:
        return None

def disallowed_paths(robots_text: str | None) -> list:
    """Returnează o listă cu toate căile specificate prin Disallow: din robots.txt."""
    if not robots_text:
        return []
    
    paths = []
    for line in robots_text.splitlines():
        line = line.strip()
        if line.lower().startswith("disallow:"):
            parts = line.split(":", 1)
            if len(parts) > 1:
                path = parts[1].strip()
                if path:
                    paths.append(path)
    return paths

print("\n--- Exercițiul 32 ---")
robots_content = fetch_robots(BASE_URL)
disallowed = disallowed_paths(robots_content)
print("Căi interzise în robots.txt:", disallowed)


#ex 34
def response_times(*urls) -> dict:
    """Măsoară timpul de răspuns în secunde pentru un număr variabil de URL-uri."""
    times = {}
    for idx, url in enumerate(urls):
        if idx > 0:
            time.sleep(1)
        try:
            start = time.perf_counter()
            requests.get(url, timeout=TIMEOUT)
            elapsed = time.perf_counter() - start
            times[url] = round(elapsed, 4)
        except requests.RequestException:
            times[url] = -1.0
    return times

print("\nExercițiul 33")
times_dict = response_times(BASE_URL, ECHO_URL + "/get")
print("Timpi de răspuns:", times_dict)


#ex 34
def log(message: str, **details) -> None:
    """Afișează un mesaj urmat de perechile cheie=valoare transmise prin kwargs."""
    details_str = " | ".join(f"{key}={val}" for key, val in details.items())
    if details_str:
        print(f"{message} | {details_str}")
    else:
        print(message)

print("\nExercițiul 34")
log("verificat", url=BASE_URL, status=200)