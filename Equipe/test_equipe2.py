import csv
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

LEAGUES_CSV = "footballant_competitions.csv"
TEAMS_CSV = "footballant_teams.csv"

# -------------------------------
# CONFIG SELENIUM
# -------------------------------
options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=options)

print("➡ Ouverture du site principal pour valider Cloudflare...")
driver.get("https://www.footballant.com")
time.sleep(10)   # laisser Cloudflare valider

print("➡ Cloudflare validé.")


# -------------------------------
# LECTURE DES LIGUES
# -------------------------------
leagues = []
with open(LEAGUES_CSV, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        leagues.append({
            "id": row["league_id"],
            "name": row["league_name"]
        })

# -------------------------------
# FICHIER CSV DE SORTIE
# -------------------------------
out = open(TEAMS_CSV, "w", newline="", encoding="utf-8")
writer = csv.writer(out)
writer.writerow(["league_id", "league_name", "team_id", "team_name_en", "team_name_cn", "football_manager_id"])


# -------------------------------
# FONCTION FETCH DANS SELENIUM
# -------------------------------
def fetch_api(url):
    script = f"""
        return fetch("{url}")
            .then(r => r.text())
            .then(t => t)
            .catch(e => "ERROR: " + e);
    """
    return driver.execute_script(script)


# -------------------------------
# TRAITEMENT DES LIGUES
# -------------------------------
for league in leagues:
    lid = league["id"]
    lname = league["name"]
    url = f"https://api.footballant.com/api/v3/get-league-team-list?leagueId={lid}&lang=fr-FR&device=3"

    print(f"\n➡ Récupération des équipes pour {lname} (id={lid})...")

    # ---- Retry automatique ----
    for attempt in range(3):
        response_text = fetch_api(url)

        if response_text.startswith("ERROR"):
            print(f"❌ Erreur fetch() (essai {attempt+1}/3) :", response_text)
            time.sleep(2)
            continue  # retry

        try:
            data = json.loads(response_text)
        except:
            print(f"❌ JSON invalide (essai {attempt+1}/3).")
            time.sleep(2)
            continue  # retry

        if data.get("code") != 0:
            print("❌ API a renvoyé un code d'erreur :", data.get("msg"))
            break

        teams = data.get("data", [])
        print(f"✅ {len(teams)} équipes trouvées.")

        for t in teams:
            writer.writerow([
                lid, lname,
                t.get("TeamID"),
                t.get("TeamNameEn"),
                t.get("TeamNameCn"),
                t.get("footballManagerTeamId")
            ])

        break  # stop retry → succès

    # --- Pause obligatoire pour éviter blocage ---
    time.sleep(1)

# -------------------------------
# FIN
# -------------------------------
out.close()
driver.quit()

print("\n🎉 FINI ! Équipes enregistrées dans :", TEAMS_CSV)
