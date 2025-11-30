// getTeam.js
import express from "express";
import Fotmob from "@max-xoo/fotmob";

const app = express();
const fotmob = new Fotmob();

app.get("/team", async (req, res) => {
  const teamId = req.query.id;
  if (!teamId) return res.status(400).json({ error: "id manquant" });

  try {
    const data = await fotmob.getTeam(teamId, "overview", "team", "Europe/London");

    // Adaptation squadGroups
    let squadGroups = data?.squad || [];
    if (!Array.isArray(squadGroups)) squadGroups = Object.values(squadGroups);

    res.json({ info: data, squad: { squad: squadGroups } });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.listen(3000, () => console.log("API Node FotMob running on port 3000"));
