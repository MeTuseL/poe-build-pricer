import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import styles from "./styles/Home.module.css";
import {pricePoB} from "../../__services__/api-service.js";

export function Home() {
    const [pobLink, setPobLink] = useState("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const navigate = useNavigate();


    const handleValidatePoB = async () => {
        if (!pobLink.trim()) {
            setError("Veuillez entrer un lien PoB valide.");
            return;
        }

        try {
            setError(null);
            setLoading(true);

            // Call Django API
            const data = await pricePoB(pobLink);

            // Redirect to PricingBuild with data
            navigate("/pricing", { state: { pobData: data } });
        } catch (err) {
            setError("Impossible de charger les données. Vérifiez le lien.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className={styles.page}>
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
                    <button
                        onClick={handleValidatePoB}
                        className={styles.validateButton}
                        disabled={loading}
                    >
                        {loading ? "Chargement..." : "Valider"}
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
                        placeholder="https://pastebin.com/..."
                        value={pobLink}
                        onChange={(e) => setPobLink(e.target.value)}
                        className={styles.input}
                    />
                    <button
                        onClick={handleValidatePoB}
                        className={styles.validateButton}
                        disabled={loading}
                    >
                        {loading ? "Chargement..." : "Valider"}
                    </button>
                </div>

                {error && <p className="text-red-500 mt-2">{error}</p>}
            </div>
        </div>
    );
}
export default Home