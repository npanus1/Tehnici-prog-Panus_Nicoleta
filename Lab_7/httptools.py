import requests
BASE = "https://httpbin.org"
PATHS = ["/get", "/redirect/2", "/delay/1", "/status/404", "/delay/5"]
# Partea 1: parametri în URL
def search(params):
    """GET pe /get cu parametri în URL; returnează parametrii primiți de server."""
    r = requests.get(BASE + "/get", params=params, timeout=10)
    return r.json()["args"]


def search_url(params):
    """Returnează adresa completă construită de requests, cu tot cu parametri."""
    r = requests.get(BASE + "/get", params=params, timeout=10)
    return r.url

# Partea 2: anteturi
def fetch_with_agent(agent):
    """GET pe /headers cu User-Agent=agent; returnează User-Agent-ul văzut de server."""
    r = requests.get(BASE + "/headers", headers={"User-Agent": agent}, timeout=10)
    return r.json()["headers"]["User-Agent"]


def default_agent():
    """Returnează User-Agent-ul trimis de requests când nu setezi nimic."""
    r = requests.get(BASE + "/headers", timeout=10)
    return r.json()["headers"]["User-Agent"]

# Partea 3: trimiterea datelor
def post_json(data):
    """POST cu datele ca JSON pe /post; returnează JSON-ul primit de server."""
    r = requests.post(BASE + "/post", json=data, timeout=10)
    return r.json()["json"]


def post_form(data):
    """POST cu datele ca formular pe /post; returnează formularul primit de server."""
    r = requests.post(BASE + "/post", data=data, timeout=10)
    return r.json()["form"]
# Partea 4: coduri de stare
def describe_status(code):
    """GET pe /status/<code>; returnează 'succes', 'eroare client' sau 'eroare server'."""
    try:
        r = requests.get(BASE + f"/status/{code}", timeout=10)
    except requests.RequestException:
        return "eroare server"   # cererea nu a ajuns la server; alegere simplă
    if 200 <= r.status_code < 300:
        return "succes"
    elif 400 <= r.status_code < 500:
        return "eroare client"
    elif 500 <= r.status_code < 600:
        return "eroare server"
    return "necunoscut"          # de ex. 3xx


def is_ok(code):
    """GET pe /status/<code>; returnează True dacă cererea a reușit, altfel False."""
    try:
        r = requests.get(BASE + f"/status/{code}", timeout=10)
        r.raise_for_status()     # ridică HTTPError pentru 4xx și 5xx
        return True
    except requests.RequestException:
        return False
# Partea 5: redirecționări
def count_redirects(n):
    """GET pe /redirect/<n>; returnează câte redirecționări au fost urmate."""
    try:
        r = requests.get(BASE + f"/redirect/{n}", timeout=10)
        return len(r.history)        # un răspuns în history pentru fiecare redirecționare
    except requests.RequestException:
        return None


def final_url(n):
    """GET pe /redirect/<n>; returnează adresa la care ai ajuns."""
    try:
        r = requests.get(BASE + f"/redirect/{n}", timeout=10)
        return r.url                 # adresa finală, după toate redirecționările
    except requests.RequestException:
        return None


def first_hop(n):
    """GET pe /redirect/<n> FĂRĂ a urma redirecționarea; returnează antetul Location."""
    try:
        r = requests.get(BASE + f"/redirect/{n}", allow_redirects=False, timeout=10)
        return r.headers.get("Location")   # None dacă antetul lipsește
    except requests.RequestException:
        return None
# Partea 6: sesiuni și cookie-uri
def cookie_demo(name, value):
    """Setează un cookie, apoi citește cookie-urile înapoi folosind O SINGURĂ sesiune."""
    try:
        s = requests.Session()                     
        s.get(BASE + "/cookies/set", params={name: value}, timeout=10)
        r = s.get(BASE + "/cookies", timeout=10)   
        return r.json()["cookies"]
    except requests.RequestException:
        return None


def no_session_demo(name, value):
    """Același lucru cu apeluri simple requests.get; returnează cookie-urile văzute de server."""
    try:
        requests.get(BASE + "/cookies/set", params={name: value}, timeout=10)
        r = requests.get(BASE + "/cookies", timeout=10)   
        return r.json()["cookies"]                        
    except requests.RequestException:
        return None
# Partea 7: raportul final
def report(path):
    """Returnează un dicționar care descrie pagina de la BASE + path."""
    try:
        r = requests.get(BASE + path, timeout=3)      
        return {
            "status": r.status_code,
            "final_url": r.url,                       
            "redirects": len(r.history),              
            "seconds": round(r.elapsed.total_seconds(), 2),
            "content_type": r.headers.get("Content-Type"),
        }
    except requests.RequestException as e:
        
        return {"status": None, "error": type(e).__name__}
# Bonus: autentificare
def check_login(user, password):
    """Returnează True dacă serverul acceptă datele de autentificare, altfel False."""
    try:
        r = requests.get(BASE + "/basic-auth/admin/secret",
                         auth=(user, password), timeout=10)
        return r.status_code == 200      
    except (requests.RequestException, UnicodeError):
        return False                     


