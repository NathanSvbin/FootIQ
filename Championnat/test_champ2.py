import csv
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

API_URL = "https://api.footballant.com/api/v2/area-league-list?areaId=1&lang=fr-FR&device=3"
CSV_FILE = "footballant_competitions.csv"

options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=options)

print("➡ Ouverture du site principal pour valider Cloudflare...")
driver.get("https://www.footballant.com")

time.sleep(10)

print("➡ Cloudflare validé. Appel de l’API avec fetch()...")

script = f"""
return fetch("{API_URL}")
    .then(r => r.text())
    .then(t => t)
    .catch(e => "ERROR: " + e);
"""

response_text = driver.execute_script(script)
driver.quit()

print("➡ Réponse reçue :")
print(response_text[:200] + "...\n")

try:
    data = json.loads(response_text)
except:
    print("❌ ERREUR : la réponse n'est pas du JSON valide.")
    exit()

print("➡ JSON OK. Extraction des compétitions...")

rows = []

for country in data.get("data", []):
    country_id = country.get("countryId")
    country_name = country.get("countryEn")

    # ⚠️ ici la bonne clé est leagueList
    for league in country.get("leagueList", []):
        league_id = league.get("sclassId")
        league_name = league.get("NameEn")

        rows.append([league_id, league_name, country_id, country_name])

# écriture csv
with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["league_id", "league_name", "country_id", "country_name"])
    writer.writerows(rows)

print(f"✅ CSV créé : {CSV_FILE}")
print(f"📌 Compétitions trouvées : {len(rows)}")
