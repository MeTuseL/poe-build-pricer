import { useLocation, Link } from "react-router-dom";
import styles from "./styles/PricingBuild.module.css";
import { useI18n } from "../../__core__/i18n/I18nProvider.jsx";

export function PricingBuild() {
    const { t } = useI18n();
    const location = useLocation();
    const pobData = location.state?.pobData;

    if (!pobData) {
        return (
            <div className={styles.page}>
                <h1 className={styles.title}>{t("pricing.title")}</h1>
                <p className={styles.noData}>{t("pricing.noData")}</p>
                <Link to="/" className={styles.backLink}>{t("pricing.back")}</Link>
            </div>
        );
    }

    return (
        <div className={styles.page}>
            <h1 className={styles.title}>{t("pricing.title")}</h1>
            <div className={styles.content}>
        <pre className={styles.jsonBox}>
{JSON.stringify(pobData, null, 2)}
        </pre>
            </div>
            <Link to="/" className={styles.backLink}>{t("pricing.back")}</Link>
        </div>
    );
}
export default PricingBuild;
