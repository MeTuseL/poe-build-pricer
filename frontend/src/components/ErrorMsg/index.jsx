import styles from "./styles/ErrorMsg.module.css";

/**
 * Message d'erreur réutilisable.
 * variant = "banner" (par défaut) pour le badge rouge,
 *           "subtle" pour un texte discret si besoin.
 */
export default function ErrorMsg({ message, children, className = "", variant = "banner" }) {
    const content = message || children;
    if (!content) return null;

    return (
        <div className={`${styles.msg} ${styles[variant]} ${className}`} role="alert">
            <svg viewBox="0 0 24 24" aria-hidden="true" className={styles.icon}>
                <path
                    d="M12 9v4m0 4h.01M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0Z"
                    fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"
                />
            </svg>
            <span className={styles.text}>{content}</span>
        </div>
    );
}
