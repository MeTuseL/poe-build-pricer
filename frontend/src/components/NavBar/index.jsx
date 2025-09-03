import React from "react";
import styles from "./styles/NavBar.module.css";
import logo from "../../assets/logo.png";
import { Link } from "react-router-dom";
import { useI18n } from "../../__core__";

export function NavBar({ onSettingsClick, onLoginClick }) {
    const { t } = useI18n();

    return (
        <nav className={styles.navbar}>
            <div className={styles.inner}>
                <Link to="/" className={styles.logo} aria-label="PoE Pricer Home">
                    <img src={logo} alt="" className={styles.logoIcon} />
                    <span>PoE Pricer</span>
                </Link>

                <div className={styles.actions}>
                    <button onClick={onSettingsClick} className={styles.settingsButton}>
                        ⚙️ {t("navbar.settings")}
                    </button>
                    <button onClick={onLoginClick} className={styles.loginButton}>
                        🔑 {t("navbar.login")}
                    </button>
                </div>
            </div>
        </nav>
    );
}
export default NavBar;
