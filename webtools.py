# Laborator: Construirea propriului modul
# Student: Panuș Nicoleta

import datetime
import hashlib
import html.parser
import json
import re
import socket
import ssl
import urllib.parse
import requests

#ex 47
DEFAULT_HEADERS = {"User-Agent": "WebLab-Panus Nicoleta"}
TIMEOUT = 10

#ex 44 & 47

def fetch(url: str, timeout: int = TIMEOUT) -> requests.Response:
    """Efectuează o cerere GET către URL folosind antetele implicite ale modulului."""
    return requests.get(url, headers=DEFAULT_HEADERS, timeout=timeout)


def get_status(url: str) -> int:
    """Returnează codul de stare HTTP pentru un URL."""
    try:
        response = fetch(url)
        return response.status_code
    except requests.RequestException:
        return 0


def get_title(html: str) -> str:
    """Extrage și curăță titlul paginii dintr-un șir HTML."""
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


def security_headers(url: str) -> dict:
    """Verifică prezența celor 5 antete de securitate esențiale."""
    headers_to_check = [
        "Strict-Transport-Security",
        "Content-Security-Policy",
        "X-Frame-Options",
        "X-Content-Type-Options",
        "Referrer-Policy"
    ]
    try:
        res = fetch(url)
        return {h: h in res.headers for h in headers_to_check}
    except requests.RequestException:
        return {h: False for h in headers_to_check}


def score_headers(results: dict) -> str:
    """Calculează scorul antetelor de securitate în format 'X/Y'."""
    total = len(results)
    passed = sum(1 for present in results.values() if present)
    return f"{passed}/{total}"


def resolve(hostname: str) -> str:
    """Află adresa IP pentru un nume de gazdă (hostname)."""
    try:
        return socket.gethostbyname(hostname)
    except socket.error:
        return "N/A"


def cert_days_left(hostname: str) -> int | str:
    """Măsoară câte zile au rămas până la expirarea certificatului SSL."""
    try:
        context = ssl.create_default_context()
        with socket.create_connection((hostname, 443), timeout=TIMEOUT) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                not_after_str = cert["notAfter"]
                cert_expires_epoch = ssl.cert_time_to_seconds(not_after_str)
                cert_expires_dt = datetime.datetime.fromtimestamp(cert_expires_epoch, tz=datetime.timezone.utc)
                now_dt = datetime.datetime.now(datetime.timezone.utc)
                return (cert_expires_dt - now_dt).days
    except Exception:
        return "N/A"


def fetch_robots(base: str) -> str | None:
    """Descarcă textul din robots.txt."""
    robots_url = base.rstrip("/") + "/robots.txt"
    try:
        res = fetch(robots_url)
        if res.status_code == 200:
            return res.text
        return None
    except requests.RequestException:
        return None


def disallowed_paths(robots_text: str | None) -> list:
    """Extrage căile interzise din robots.txt."""
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


def extract_links(html_code: str) -> list:
    """Extrage toate legăturile unice din HTML."""
    raw_links = re.findall(r'href="([^"]+)"', html_code)
    return list(dict.fromkeys(raw_links))


def split_links(links: list, domain: str) -> tuple[list, list]:
    """Separă legăturile în interne și externe."""
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


def get_redirect_chain(url: str) -> tuple[str, str]:
    """Măsoară redirecționările de la o adresă HTTP la HTTPS."""
    try:
        res = requests.get(url, headers=DEFAULT_HEADERS, timeout=TIMEOUT)
        if res.history:
            chain = " -> ".join(f"{r.status_code}" for r in res.history) + f" -> {res.url}"
        else:
            chain = f"Fără redirecționare ({res.status_code})"
        return chain, res.url
    except requests.RequestException:
        return "Eroare la conectare", url


#ex 50
def site_report(url: str) -> dict:
    """Generează un raport complet despre un site web, îl afișează și îl salvează în report.json."""
    parsed = urllib.parse.urlparse(url)
    hostname = parsed.netloc or parsed.path

    target_url = url if url.startswith("http") else f"https://{hostname}"
    http_url = f"http://{hostname}"

    print(f"=== Raport site: {target_url} ===")

    redirect_info, final_url = get_redirect_chain(http_url)
    res = fetch(target_url)
    status_code = res.status_code
    print(f"Cod de stare:      {status_code}")

    title = get_title(res.text)
    print(f"Titlu:             {title}")

    ip_addr = resolve(hostname)
    print(f"Adresă IP:         {ip_addr}")

    print(f"Redirecționări:    {redirect_info}")

    sec_dict = security_headers(target_url)
    sec_score = score_headers(sec_dict)
    print(f"Scor securitate:   {sec_score}")

    days_left = cert_days_left(hostname)
    print(f"Certificat:        {days_left} de zile rămase")

    all_links = extract_links(res.text)
    int_links, ext_links = split_links(all_links, hostname)
    print(f"Legături:          {len(int_links)} interne, {len(ext_links)} externe")

    robots_txt = fetch_robots(target_url)
    forbidden_paths = disallowed_paths(robots_txt)
    print(f"Căi interzise:     {', '.join(forbidden_paths) if forbidden_paths else 'Niciuna'}")

    report_data = {
        "target_url": target_url,
        "status_code": status_code,
        "title": title,
        "ip_address": ip_addr,
        "redirect_chain": redirect_info,
        "security_score": sec_score,
        "ssl_days_left": days_left,
        "internal_links_count": len(int_links),
        "external_links_count": len(ext_links),
        "disallowed_paths": forbidden_paths
    }

    with open("report.json", "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=2, ensure_ascii=False)

    print("Salvat în report.json")
    return report_data


#ex 46
if __name__ == "__main__":
    print("Autotest:", get_status("https://cybercor.org"))