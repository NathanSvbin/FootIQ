from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import csv
import time

def parse_value_euro(valeur_str):
    """Convertit la valeur en euros entiers"""
    if not valeur_str:
        return 0
    valeur_str = valeur_str.replace("€", "").strip()
    valeur_str = valeur_str.replace(".", "").replace(",", ".")
    try:
        number = float(valeur_str.split()[0])
        if "mrd" in valeur_str:
            return int(number * 1_000_000_000)
        elif "mio" in valeur_str:
            return int(number * 1_000_000)
        else:
            return int(number)
    except:
        return 0

# --- Configuration Selenium ---
chrome_options = Options()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--window-size=1920x1080")

driver_path = r"C:\Users\nathan.sabin\.wdm\drivers\chromedriver-win64\chromedriver.exe"
driver = webdriver.Chrome(service=Service(driver_path), options=chrome_options)

URL = "https://www.transfermarkt.fr/wettbewerbe/europa/wettbewerbe?plus=1"
driver.get(URL)
time.sleep(10)

championnats = []
id_counter = 1
seen = set()  # pour éviter les doublons

while len(championnats) < 500:
    rows = driver.find_elements(By.CSS_SELECTOR, "table.items tbody tr")
    for row in rows:
        if len(championnats) >= 500:
            break

        links = row.find_elements(By.CSS_SELECTOR, "td.hauptlink a")
        if len(links) >= 2:
            link = links[1]
            nom = link.text.strip()
            href = link.get_attribute("href")
        else:
            continue

        if (nom, href) in seen:
            continue
        seen.add((nom, href))

        try:
            valeur_td = row.find_element(By.CSS_SELECTOR, "td.rechts.hauptlink")
            valeur_str = valeur_td.text.strip()
        except:
            valeur_str = ""
        valeur = parse_value_euro(valeur_str)

        championnats.append((id_counter, nom, href, valeur))
        print(id_counter, nom, href, valeur)
        id_counter += 1

    # Pagination : page suivante
    try:
        next_btn = driver.find_element(By.CSS_SELECTOR, "a.tm-pagination__link[title='Allez à la page suivante']")
        next_btn.click()
        time.sleep(10)
    except:
        break

driver.quit()

# Sauvegarder dans CSV
with open("championnats_europe.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["ID", "Championnat", "Lien", "Valeur (€)"])
    for row in championnats:
        writer.writerow(row)

print(f"{len(championnats)} championnats récupérés et sauvegardés dans championnats_europe.csv")
