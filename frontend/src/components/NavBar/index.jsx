import React from "react";
import styles from "./styles/NavBar.module.css";
import logo from "../../assets/logo.png";
import {Link} from "react-router-dom";

export function NavBar({ onSettingsClick, onLoginClick }) {
    return (
        <nav className={styles.navbar}>
            <div className={styles.inner}>
                <Link to="/" className={styles.logo}>
                    <img src={logo} alt="Logo" className={styles.logoIcon} />
                    <span>PoE Pricer</span>
                </Link>
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
export default NavBar;