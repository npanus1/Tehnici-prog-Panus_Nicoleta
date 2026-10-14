
# Student: Panuș Nicoleta

import argparse
import csv
from datetime import datetime

#ex 44, 45 & 47
import webtools
from webtools import DEFAULT_HEADERS, get_title, site_report


#ex 49
def generate_csv_report(base_url: str):
    """Verifică o listă de căi și le salvează în report.csv."""
    paths_to_check = ["/", "/robots.txt", "/sitemap.xml"]
    
    with open("report.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["path", "status", "checked_at"])
        
        for path in paths_to_check:
            full_url = base_url.rstrip("/") + path
            status = webtools.get_status(full_url)
            checked_at = datetime.now().isoformat()
            writer.writerow([path, status, checked_at])
            
    print("Raportul CSV a fost salvat în report.csv")


def main():
    #ex 48
    parser = argparse.ArgumentParser(description="Generează un raport despre un site web.")
    parser.add_argument("url", nargs="?", default="https://cybercor.org", help="URL-ul țintă pentru raport")
    args = parser.parse_args()

    target_url = args.url

    print(f"User-Agent implicit: {DEFAULT_HEADERS['User-Agent']}\n")

    # Generare CSV (ex 49)
    generate_csv_report(target_url)
    print()

    # Raportul complet (ex 50)
    site_report(target_url)


if __name__ == "__main__":
    main()