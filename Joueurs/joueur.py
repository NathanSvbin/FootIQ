import requests
from bs4 import BeautifulSoup
import csv
import time

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


# ------------------------------------------------------------
# FONCTIONS DE SCRAPING
# ------------------------------------------------------------

def extract_people_from_table(url, id_club):
    """
    Récupère nom, prénom depuis un tableau Transfermarkt (joueurs ou staff)
    """
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        print(f"❌ Erreur {response.status_code} pour {url}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", class_="items")
    if not table:
        print(f"⚠️ Aucun tableau trouvé pour {url}")
        return []

    result = []

    rows = table.find("tbody").find_all("tr", recursive=False)
    for row in rows:
        a = row.find("a", href=True)
        if not a:
            continue

        full_name = a.get_text(strip=True)

        parts = full_name.split(" ", 1)
        prenom = parts[0]
        nom = parts[1] if len(parts) > 1 else ""

        result.append((nom, prenom, id_club))

    return result


# ------------------------------------------------------------
# LECTURE CLUBS
# ------------------------------------------------------------

def lire_equipes(fichier_csv):
    """
    Lecture du fichier equipe.csv
    Format attendu :
    Championnat, Club, Lien
    id_club = ligne index + 1
    """
    equipes = []
    with open(fichier_csv, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)
        for idx, row in enumerate(reader, start=1):
            championnat = row[0].strip()
            club = row[1].strip()
            lien = row[2].strip()
            id_club = idx  # ID = numéro de ligne
            equipes.append((id_club, championnat, club, lien))

    return equipes


# ------------------------------------------------------------
# PROGRAMME PRINCIPAL
# ------------------------------------------------------------

def main():
    fichier_equipe = "../equipe/Equipe/equipe.csv"
    sortie = "joueurs_staff.csv"

    equipes = lire_equipes(fichier_equipe)

    all_people = []

    for id_club, championnat, club, lien_club in equipes:
        print(f"🔎 Traitement club : {club} (ID {id_club})")

        # URL joueurs (kader)
        joueurs_url = lien_club.replace("starseite/verein/", "/kader/verein/")

        # URL staff (mitarbeiter)
        staff_url = lien_club.replace("starseite/verein/", "/mitarbeiter/verein/")

        print("  👥 Joueurs…")
        joueurs = extract_people_from_table(joueurs_url, id_club)
        all_people.extend(joueurs)
        print(f"  ✔️ {len(joueurs)} joueurs trouvés")

        print("  🧑‍🏫 Staff…")
        staff = extract_people_from_table(staff_url, id_club)
        all_people.extend(staff)
        print(f"  ✔️ {len(staff)} staff trouvés")

        time.sleep(1.5)

    # Sauvegarde CSV final
    with open(sortie, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["nom", "prenom", "id_club"])
        writer.writerows(all_people)

    print(f"\n💾 Sauvegardé dans {sortie}")
    print("🏁 Terminé.")


if __name__ == "__main__":
    main()
