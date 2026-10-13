from checker import (
    build_url,
    is_https,
    show_response,
    check_site,
    scan_sites,
    check_headers,
    retry_check
)

# Partea 1 - apeluri pentru build_url și is_https[cite: 5]
print("Partea 1")
print("build_url:", build_url("example.com", "login"))
print("build_url cu /:", build_url("example.com", "/login"))
print("is_https (True):", is_https("https://example.com"))
print("is_https (False):", is_https("http://example.com"))

# Partea 2 - apeluri pentru show_response[cite: 5]
print("\nPartea 2")
show_response("https://example.com")

# Partea 3 - apeluri pentru check_site[cite: 5]
print("\nPartea 3")
print("check_site (succes):", check_site("https://example.com"))
print("check_site (eroare):", check_site("http://this-site-does-not-exist.invalid"))

# Partea 4 -  apelul scan_sites()[cite: 5]
print("\nPartea 4")
scan_sites()

# Partea 5 - apeluri pentru check_headers[cite: 5]
print("\nPartea 5")
print("check_headers:", check_headers("https://example.com"))

# Partea 6 -apeluri pentru retry_check[cite: 5]
print("\nPartea 6")
print("retry_check 200:", retry_check("https://httpbin.org/status/200"))
print("retry_check 404:", retry_check("https://httpbin.org/status/404"))
print("retry_check 500:", retry_check("https://httpbin.org/status/500", attempts=2))
print("retry_check invalid:", retry_check("http://this-site-does-not-exist.invalid"))