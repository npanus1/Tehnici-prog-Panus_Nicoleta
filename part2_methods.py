# Laborator: Metode și atribute ale obiectelor web 
# Student: <Panuș Nicoleta>

import time
import requests

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10 

#ex 9
print("Exercițiul 9")
response = requests.get(BASE_URL, timeout=TIMEOUT)

print("Status code:", response.status_code)  
print("Is OK?:", response.ok)                
print("URL:", response.url)                  
print("Encoding:", response.encoding)       


#ex 10
print("\nExercițiul 10")
try:
    response.raise_for_status()  
    print("Pagina principală s-a încărcat cu succes")
except requests.HTTPError as e:
    print(f"Eroare pe pagina principală: {e}")

time.sleep(1)

bad_url = BASE_URL + "/this-page-does-not-exist"
try:
    bad_response = requests.get(bad_url, timeout=TIMEOUT)
    bad_response.raise_for_status()
except requests.HTTPError as err:
    print(f"Mesaj prietenos: Pagina căutată nu a fost găsită ({err.response.status_code}).")


#ex 11
print("\nExercițiul 11")
print("Antetele răspunsului:")
for header_name, header_value in response.headers.items():
    print(f"{header_name}: {header_value}")


#ex 12
print("\nExercițiul 12")
server_header = response.headers.get("Server", "lipsește")
content_type_header = response.headers.get("Content-Type", "lipsește")
print(f"Server: {server_header}")
print(f"Content-Type: {content_type_header}")

# Încercare cu litere mici:
lowercase_content_type = response.headers.get("content-type", "lipsește")
print(f"content-type (cu litere mici): {lowercase_content_type}")


#ex 13
print("\nExercițiul 13")
cyber_count = response.text.lower().count("cyber")
print(f"Cuvântul 'cyber' apare de {cyber_count} ori pe pagina principală.")


#ex 14
print("\nExercițiul 14")
html_content = response.text
start_tag = "<title>"
end_tag = "</title>"

start_pos = html_content.lower().find(start_tag)
if start_pos != -1:
    start_pos += len(start_tag)
    end_pos = html_content.lower().find(end_tag, start_pos)
    title = html_content[start_pos:end_pos].strip()
    print("Titlul paginii:", title)
else:
    print("Eticheta <title> nu a fost găsită.")


#ex 15
print("\nExercițiul 15")
lines = html_content.splitlines()
print(f"Număr total de linii: {len(lines)}")
if lines:
    longest_line = max(lines, key=len)
    print(f"Lungimea celei mai lungi linii: {len(longest_line)} caractere")


#ex 16
print("\nExercițiul 16")
if response.url.startswith("https://"):
    print("Conexiune securizată")
else:
    print("Conexiune nesecurizată")


#ex 17
print("\nExercițiul 17")
time.sleep(1)
http_url = "http://cybercor.org"
redirect_response = requests.get(http_url, timeout=TIMEOUT)

if redirect_response.history:
    print("Lanț de redirecționări:")
    for resp in redirect_response.history:
        print(f"  {resp.status_code} -> {resp.url}")
    print(f"URL final: {redirect_response.url}")
else:
    print(f"Nu au existat redirecționări. URL final: {redirect_response.url}")


#ex 18
print("\nExercițiul 18")
time.sleep(1)
head_response = requests.head(BASE_URL, timeout=TIMEOUT)
get_response = requests.get(BASE_URL, timeout=TIMEOUT)

print(f"Lungime corp răspuns HEAD: {len(head_response.content)} octeți")
print(f"Lungime corp răspuns GET:  {len(get_response.content)} octeți")


#ex  19
print("\nExercițiul 19")
if len(response.cookies) > 0:
    for cookie in response.cookies:
        print(f"Cookie: {cookie.name} | Securizat: {cookie.secure}")
else:
    print("Niciun cookie setat")


#ex 20
print("\nExercițiul 20")
time.sleep(1)
session = requests.Session()
custom_user_agent = "WebLab-Panus Nicoleta"
session.headers.update({"User-Agent": custom_user_agent})

session_response = session.get(ECHO_URL + "/headers", timeout=TIMEOUT)
data = session_response.json()

sent_user_agent = data.get("headers", {}).get("User-Agent")
print(f"User-Agent trimis confirmat de server: {sent_user_agent}")

session.close()