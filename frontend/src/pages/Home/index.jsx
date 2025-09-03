import React, { useState } from "react";
import {NavBar} from "../../components/NavBar/index.jsx";
import styles from "./styles/Home.module.css"

export function Home() {
  const [pobLink, setPobLink] = useState("");
  const [profile, setProfile] = useState("");
  const [result, setResult] = useState(null);

  const handleValidatePoB = () => {
    if (pobLink.trim()) {
      setResult(`Lien PoB détecté : ${pobLink}`);
    } else {
      setResult("Veuillez entrer un lien PoB valide.");
    }
  };

  const handleValidateProfile = () => {
    if (profile.trim()) {
      setResult(`Profil détecté : ${profile}`);
    } else {
      setResult("Veuillez entrer un pseudo de profil valide.");
    }
  };

  return (
    <div className={styles.page}>
      <NavBar
        onSettingsClick={() => alert("Ouvrir paramètres")}
        onLoginClick={() => alert("Connexion")}
      />

      <main className={styles.main}>
        <h1 className={styles.heroTitle}>PoE Pricer Tools</h1>
        <p className={styles.heroSubtitle}>
          Estime le coût total d’un build Path of Exile à partir d’un lien PoB.
          Connecte-toi pour accéder aux paramètres et sauvegarder des builds.
        </p>

        {/* Bloc PoB */}
        <div className={styles.block}>
          <label className={styles.label}>
            Code PoB
            <a href="#" className={styles.linkHelp}>
              Comment obtenir un lien PoB ?
            </a>
          </label>
          <div className={styles.inputRow}>
            <input
              type="text"
              placeholder="https://pastebin.com/..."
              value={pobLink}
              onChange={(e) => setPobLink(e.target.value)}
              className={styles.input}
            />
            <button onClick={handleValidatePoB} className={styles.validateButton}>
              Valider
            </button>
          </div>
        </div>

        {/* Bloc Profil */}
        <div className={styles.profileBlock}>
          <label className={styles.label}>
            Import Profil
            <span className={styles.reservedTag}>
              Réservé aux utilisateurs connectés
            </span>
          </label>
          <div className={styles.inputRow}>
            <input
              type="text"
              placeholder="Insérer le pseudo du profil PoE"
              value={profile}
              onChange={(e) => setProfile(e.target.value)}
              className={styles.input}
            />
            <button
              onClick={handleValidateProfile}
              disabled
              className={styles.disabledButton}
            >
              Valider
            </button>
          </div>
        </div>

        {/* Bloc Résultat */}
        <div className={styles.resultBox}>
          <h2 className={styles.resultTitle}>Résultat</h2>
          <p className={styles.resultText}>
            {result || "Aucun calcul encore. Entre un lien PoB valide puis clique sur Valider."}
          </p>
        </div>
      </main>
    </div>
  );
}
