import requests

SITES = [
    "https://httpbin.org/html",
    "https://httpbin.org/json",
    "https://example.com",
    "https://httpbin.org/status/200",
    "https://httpbin.org/status/404",
    "https://httpbin.org/status/500",
    "http://this-site-does-not-exist.invalid",
]

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
]

def build_url(host, path):
    if not path.startswith("/"):
        path = "/" + path
    return f"https://{host}{path}"

def is_https(url):
    return url.lower().startswith("https://")

def show_response(url):
    try:
        response = requests.get(url)
        print(f"Status: {response.status_code}")
        print(f"Content-Type: {response.headers.get('Content-Type')}")
    except Exception as e:
        print(f"Erore: {e}")

def check_site(url):
    try:
        response = requests.get(url, timeout=5)
        content_type = response.headers.get("Content-Type", "").split(";")[0].strip()
        server = response.headers.get("Server", "unknown")
        return {
            "status": response.status_code,
            "content_type": content_type,
            "length": len(response.content),
            "server": server
        }
    except requests.RequestException as e:
        return {"status": None, "error": str(e)}

def scan_sites():
    results = []
    for url in SITES:
        res = check_site(url)
        if res["status"] == 200:
            results.append((url, res))
    
    results.sort(key=lambda x: x[1]["length"], reverse=True)
    
    for url, res in results:
        print(f"{url} -> 200, {res['length']} octeți")
        
    successful = 0
    failed = 0
    for url in SITES:
        res = check_site(url)
        if res["status"] == 200:
            successful += 1
        else:
            failed += 1
            
    print(f"Reuşite: {successful} Eşuate: {failed}")

def check_headers(url):
    try:
        response = requests.get(url, timeout=5)
        headers_lower = {k.lower(): v for k, v in response.headers.items()}
        present = []
        missing = []
        
        for header in SECURITY_HEADERS:
            if header.lower() in headers_lower:
                present.append(header)
            else:
                missing.append(header)
                
        score = int((len(present) / len(SECURITY_HEADERS)) * 100)
        return {
            "present": present,
            "missing": missing,
            "score": score,
        }
    except requests.RequestException as e:
        return {"status": None, "error": str(e)}

def retry_check(url, attempts=3):
    last_status = None
    last_error = None
    
    for i in range(1, attempts + 1):
        try:
            response = requests.get(url, timeout=5)
            last_status = response.status_code
            if last_status < 500:
                return {"status": last_status, "attempts": i}
        except requests.RequestException as e:
            last_error = str(e)
            
    result = {"status": last_status, "attempts": attempts}
    if last_status is None and last_error:
        result["error"] = last_error
    return result