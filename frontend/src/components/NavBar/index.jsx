import React from "react";
import styles from "./styles/NavBar.module.css";

export function NavBar({ onSettingsClick, onLoginClick }) {
  return (
    <nav className={styles.navbar}>
      <div className={`container ${styles.inner}`}>
        {/* Logo */}
        <div className={styles.logo}>PoE Pricer</div>

        {/* Actions */}
        <div className={styles.actions}>
          <button onClick={onSettingsClick} className={styles.settingsButton}>
            ⚙️ Paramètres
          </button>
          <button onClick={onLoginClick} className={styles.loginButton}>
            🔑 Connexion
          </button>
        </div>
      </div>
    </nav>
  );
}
