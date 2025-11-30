// get_team.js
// Fonction exposée globalement pour être appelée depuis le HTML
export async function loadTeam(teamId) {
    if (!teamId) {
        console.error("Team ID manquant");
        return;
    }

    try {
        // Appel à ton API PHP qui renvoie les infos JSON depuis Fotmob
        const res = await fetch(`/Generateur/get_team.php?id=${teamId}`);
        if (!res.ok) throw new Error("Erreur API");

        const data = await res.json();

        // Logo
        const img = document.getElementById('clubLogo');
        if (img && data?.info?.imageUrl) img.src = data.info.imageUrl;

        // Joueurs
        const ul = document.getElementById('players');
        ul.innerHTML = '';

        const squad = data?.squad?.squad;
        if (Array.isArray(squad) && squad.length > 0) {
            squad.forEach(p => {
                const li = document.createElement('li');
                li.innerText = `${p.name} - ${p.position ?? ''}`;
                ul.appendChild(li);
            });
        } else {
            ul.innerHTML = '<li>Aucun joueur trouvé.</li>';
        }

    } catch (err) {
        console.error("Erreur lors du chargement de l'équipe:", err);
        const ul = document.getElementById('players');
        if (ul) ul.innerHTML = '<li>Erreur de chargement API</li>';
    }
}
