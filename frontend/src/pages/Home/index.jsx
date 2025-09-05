import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import styles from "./styles/Home.module.css";
import { pricePoB } from "../../__services__/api-service.js";
import { useI18n } from "../../__core__";
import ErrorMsg from "../../components/ErrorMsg";

export default function Home() {
    const { t } = useI18n();
    const [pobLink, setPobLink] = useState("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null); // erreurs du bloc PoB
    const navigate = useNavigate();

    // TODO: remplacera plus tard par ton vrai état d'auth
    const isAuthenticated = false;

    const handleValidatePoB = async () => {
        if (!pobLink.trim()) {
            setError(t("home.errorInvalidLink"));
            return;
        }
        try {
            setError(null);
            setLoading(true);
            const data = await pricePoB(pobLink);
            navigate("/pricing", { state: { pobData: data } });
        } catch {
            setError(t("home.errorLoading"));
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className={styles.page}>
            <h1 className={styles.heroTitle}>{t("home.title")}</h1>
            <p className={styles.heroSubtitle}>{t("home.subtitle")}</p>

            {/* Bloc PoB */}
            <div className={styles.block}>
                <label className={styles.label}>
                    {t("home.pobLabel")}
                    <a href="#" className={styles.linkHelp}>
                        {t("home.pobHelp")}
                    </a>
                </label>

                <div className={styles.inputRow}>
                    <input
                        type="text"
                        placeholder={t("home.inputPlaceholder")}
                        value={pobLink}
                        onChange={(e) => setPobLink(e.target.value)}
                        className={styles.input}
                        disabled={loading}
                        aria-disabled={loading}
                    />
                    <button
                        onClick={handleValidatePoB}
                        className={styles.validateButton}
                        disabled={loading}
                        type="button"
                    >
                        {loading ? t("home.loading") : t("home.validate")}
                    </button>
                </div>

                {error && <ErrorMsg message={error} />}
            </div>

            {/* Bloc Import profil — désactivé si non connecté */}
            <div className={styles.profileBlock}>
                <label className={styles.label}>
                    {t("home.import")}
                </label>

                <div className={styles.inputRow}>
                    <input
                        type="text"
                        placeholder={t("home.inputPlaceholder")}
                        className={`${styles.input} ${!isAuthenticated ? styles.inputDisabled : ""}`}
                        disabled={!isAuthenticated}
                        aria-disabled={!isAuthenticated}
                        title={!isAuthenticated ? t("home.reserved") : undefined}
                    />
                    <button
                        className={`${!isAuthenticated ? styles.disabledButton : styles.validateButton}`}
                        disabled={!isAuthenticated}
                        aria-disabled={!isAuthenticated}
                        title={!isAuthenticated ? t("home.reserved") : undefined}
                        type="button"
                    >
                        {t("home.validate")}
                    </button>
                </div>

                {!isAuthenticated && <ErrorMsg message={t("home.reserved")} />}
            </div>
        </div>
    );
}
