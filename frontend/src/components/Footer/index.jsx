import React from "react";
import styles from "./styles/Footer.module.css";

export default function Footer() {
    const year = new Date().getFullYear();
    return (
        <footer className={styles.footer}>
            <div className={styles.inner}>
                <p className={styles.copy}>
                    © {year} <span className={styles.brand}>PoE Pricer</span> — Tous droits réservés.
                </p>
            </div>
        </footer>
    );
}
