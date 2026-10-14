# Laborator: Alte module din biblioteca standard 
# Student: <Panuș Nicoleta>

import datetime
import hashlib
import html.parser
import json
import re
import socket
import ssl
import time
import urllib.parse
import requests

BASE_URL = "https://cybercor.org"
TIMEOUT = 10


#ex 35
print("Exercițiul 35")
sample_url = "https://cybercor.org/path?x=1#top"
parsed_url = urllib.parse.urlparse(sample_url)

print(f"Scheme: {parsed_url.scheme}")
print(f"Netloc: {parsed_url.netloc}")
print(f"Path: {parsed_url.path}")
print(f"Query: {parsed_url.query}")
print(f"Fragment: {parsed_url.fragment}")


#ex 36
print("\nExercițiul 36")
relative_links = ["/about", "contact.html", "../index.html"]
for rel in relative_links:
    full_url = urllib.parse.urljoin(BASE_URL, rel)
    print(f"Relativ: {rel:<15} -> Absolut: {full_url}")


#ex 37
def extract_links(html_code: str) -> list:
    """Extrage toate legăturile (href) dintr-un cod HTML și le returnează fără duplicate."""
    raw_links = re.findall(r'href="([^"]+)"', html_code)
    unique_links = list(dict.fromkeys(raw_links)) 
    return unique_links

print("\nExercițiul 37")
html_resp = requests.get(BASE_URL, timeout=TIMEOUT).text
extracted = extract_links(html_resp)
print(f"S-au găsit {len(extracted)} legături unice (primele 5):", extracted[:5])


#ex 28
def split_links(links: list, domain: str) -> tuple[list, list]:
    """Separă o listă de legături în interne și externe pe baza domeniului dat."""
    internal = []
    external = []
    
    for link in links:
        absolute_url = urllib.parse.urljoin(f"https://{domain}", link)
        link_domain = urllib.parse.urlparse(absolute_url).netloc
        
        if link_domain == domain or link_domain == f"www.{domain}":
            internal.append(absolute_url)
        else:
            external.append(absolute_url)
            
    return list(set(internal)), list(set(external))

print("\nExercițiul 38")
base_domain = urllib.parse.urlparse(BASE_URL).netloc
int_links, ext_links = split_links(extracted, base_domain)
print(f"Legături interne: {len(int_links)} | Legături externe: {len(ext_links)}")


#ex 39
class ImageFinder(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.images = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() == "img":
            attrs_dict = dict(attrs)
            src = attrs_dict.get("src")
            if src:
                self.images.append(src)

print("\nExercițiul 39")
test_html = """
<html><body>
  <img src="/logo.png" alt="Logo">
  <IMG SRC="poza.jpg">
  <img alt="imagine fără src">
  <img src="https://cdn.example.com/banner.webp" />
  <a href="/despre">Aceasta nu este o imagine</a>
</body></html>
"""

finder = ImageFinder()
finder.feed(test_html)
print("Imagini găsite în test:", finder.images)

assert finder.images == [
    "/logo.png",                            
    "poza.jpg",                             
    "https://cdn.example.com/banner.webp", 
], "Parserul nu a găsit exact imaginile așteptate"
print("Testul a trecut!")

real_finder = ImageFinder()
real_finder.feed(html_resp)
print(f"{len(real_finder.images)} imagini găsite pe {BASE_URL}")


#ex 40
def page_fingerprint(url: str) -> str:
    """Calculează și returnează amprenta SHA-256 a conținutului paginii."""
    res = requests.get(url, timeout=TIMEOUT)
    return hashlib.sha256(res.content).hexdigest()

print("\nExercițiul 40")
hash1 = page_fingerprint(BASE_URL)
time.sleep(1)
hash2 = page_fingerprint(BASE_URL)

print("Amprenta 1:", hash1)
print("Amprenta 2:", hash2)
print("Amprente egale?:", hash1 == hash2)


#ex 41
print("\nExercițiul 41")
resp_41 = requests.get(BASE_URL, timeout=TIMEOUT)
headers_dict = dict(resp_41.headers)

with open("headers.json", "w", encoding="utf-8") as f:
    json.dump(headers_dict, f, indent=2)
print("Antetele au fost salvate în headers.json")

with open("headers.json", "r", encoding="utf-8") as f:
    loaded_headers = json.load(f)

print("Antet citit din fișier (Content-Type):", loaded_headers.get("Content-Type"))


#42
def resolve(hostname: str) -> str:
    """Află și returnează adresa IP asociată unui nume de gazdă (hostname)."""
    try:
        return socket.gethostbyname(hostname)
    except socket.error as e:
        return f"Eroare DNS: {e}"

print("\nExercițiul 42")
hostname_target = urllib.parse.urlparse(BASE_URL).netloc
ip_address = resolve(hostname_target)
print(f"Adresa IP pentru {hostname_target} este: {ip_address}")


#ex 43
def cert_days_left(hostname: str) -> int:
    """Se conectează prin SSL pe portul 443 și calculează câte zile au rămas până la expirarea certificatului."""
    context = ssl.create_default_context()
    with socket.create_connection((hostname, 443), timeout=TIMEOUT) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            cert = ssock.getpeercert()
            not_after_str = cert["notAfter"]

        
            cert_expires_epoch = ssl.cert_time_to_seconds(not_after_str)
            cert_expires_dt = datetime.datetime.fromtimestamp(cert_expires_epoch, tz=datetime.timezone.utc)
            now_dt = datetime.datetime.now(datetime.timezone.utc)
            
            days_left = (cert_expires_dt - now_dt).days
            return days_left

print("\nExercițiul 43")
try:
    days = cert_days_left(hostname_target)
    print(f"Zile rămase până la expirarea certificatului SSL ({hostname_target}): {days} zile")
except Exception as err:
    print(f"Nu s-a putut citi certificatul: {err}")