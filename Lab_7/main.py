from httptools import PATHS, report


def main():
    """Rulează raportul pentru toate adresele din PATHS și afișează rezumatul."""
    results = []
    for path in PATHS:
        info = report(path)
        info["path"] = path              # adăugăm adresa, ca s-o putem afișa
        results.append(info)

    # doar paginile cu status 200, cea mai lentă prima
    ok_pages = [r for r in results if r["status"] == 200]
    ok_pages.sort(key=lambda r: r["seconds"], reverse=True)

    for r in ok_pages:
        print(f"{r['path']} -> {r['status']}, {r['seconds']} secunde")

    failed = len(results) - len(ok_pages)
    print(f"Reușite: {len(ok_pages)} | Eșuate: {failed}")


if __name__ == "__main__":
    main()