import { useLocation, Link } from "react-router-dom";
import styles from "./styles/PricingBuild.module.css";

export function PricingBuild() {
    const location = useLocation();
    const pobData = location.state?.pobData;

    if (!pobData) {
        return (
            <div className={styles.page}>
                <h1 className={styles.title}>Résultats du build</h1>
                <p>Aucune donnée reçue. Retournez à l'accueil.</p>
                <Link to="/" className={styles.backLink}>
                    ← Retour à l'accueil
                </Link>
            </div>
        );
    }

    return (
        <div className={styles.page}>
            <h1 className={styles.title}>Résultats du build</h1>
            <div className={styles.content}>
        <pre className={styles.jsonBox}>
          {JSON.stringify(pobData, null, 2)}
        </pre>
            </div>
            <Link to="/" className={styles.backLink}>
                ← Retour à l'accueil
            </Link>
        </div>
    );
}
export default PricingBuild;