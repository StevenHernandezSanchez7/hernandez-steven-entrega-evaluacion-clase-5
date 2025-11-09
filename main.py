import concurrent.futures, requests, time, json, random

URLS = [
    "https://example.com",
    "https://httpbin.org/get",
    "https://httpbin.org/status/404",
    "https://api.github.com"
]
MAX_WORKERS, TIMEOUT, RETRIES = 5, 5, 3

def fetch(url):
    for intento in range(1, RETRIES + 1):
        try:
            r = requests.get(url, timeout=TIMEOUT)
            return {"url": url, "status": r.status_code, "ok": r.ok, "intentos": intento}
        except requests.RequestException as e:
            if intento < RETRIES:
                time.sleep(0.5 * (2 ** (intento - 1)) + random.uniform(0, 0.3))
            else:
                return {"url": url, "ok": False, "error": str(e), "intentos": intento}

def main():
    resultados = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futuros = [executor.submit(fetch, url) for url in URLS]
        for futuro in concurrent.futures.as_completed(futuros):
            r = futuro.result()
            resultados.append(r)
            print(f"{r['url']} → {r.get('status', 'error')}")

    with open("resultados.json", "w", encoding="utf-8") as f:
        json.dump(resultados, f, indent=2, ensure_ascii=False)

    print("\nResultados guardados en resultados.json")

if __name__ == "__main__":
    main()
