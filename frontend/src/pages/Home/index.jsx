import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import styles from "./styles/Home.module.css";
import { pricePoB } from "../../__services__/api-service.js";
import { useI18n } from "../../__core__/i18n/I18nProvider.jsx";

export function Home() {
    const { t } = useI18n();
    const [pobLink, setPobLink] = useState("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const navigate = useNavigate();

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
                    />
                    <button
                        onClick={handleValidatePoB}
                        className={styles.validateButton}
                        disabled={loading}
                    >
                        {loading ? t("home.loading") : t("home.validate")}
                    </button>
                </div>
            </div>

            {/* Bloc Profil */}
            <div className={styles.profileBlock}>
                <label className={styles.label}>
                    {t("home.import")}
                    <span className={styles.reservedTag}>{t("home.reserved")}</span>
                </label>

                <div className={styles.inputRow}>
                    <input
                        type="text"
                        placeholder={t("home.inputPlaceholder")}
                        className={styles.input}
                    />
                    <button className={styles.validateButton}>
                        {t("home.validate")}
                    </button>
                </div>

                {error && <p className={styles.errorText}>{error}</p>}
            </div>
        </div>
    );
}
export default Home;
