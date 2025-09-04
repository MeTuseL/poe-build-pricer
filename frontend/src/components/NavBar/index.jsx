import React from "react";
import { Link } from "react-router-dom";
import styles from "./styles/NavBar.module.css";
import logo from "../../assets/logo.png";
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
                    <button
                        onClick={onSettingsClick}
                        className={styles.settingsButton}
                        aria-label={t("navbar.settings")}
                        title={t("navbar.settings")}
                        type="button"
                    >
                        {/* Icône Paramètres (engrenage) */}
                        <svg
                            className={styles.btnIcon}
                            viewBox="0 0 24 24"
                            aria-hidden="true"
                            focusable="false"
                        >
                            <path d="M12 15a3 3 0 1 0 0-6 3 3 0 0 0 0 6Z" fill="currentColor" />
                            <path
                                d="M19.4 15a1 1 0 0 1 .2 1.1l-1 1.8a1 1 0 0 1-1.1.5l-2-.5a7.5 7.5 0 0 1-1.7 1l-.3 2a1 1 0 0 1-1 .9h-2a1 1 0 0 1-1-.9l-.3-2a7.5 7.5 0 0 1-1.7-1l-2 .5a1 1 0 0 1-1.1-.5l-1-1.8a1 1 0 0 1 .2-1.1l1.7-1.4a7.8 7.8 0 0 1 0-2.1L4.3 10a1 1 0 0 1-.2-1.1l1-1.8a1 1 0 0 1 1.1-.5l2 .5a7.5 7.5 0 0 1 1.7-1l.3-2a1 1 0 0 1 1-.9h2a1 1 0 0 1 1 .9l.3 2a7.5 7.5 0 0 1 1.7 1l2-.5a1 1 0 0 1 1.1.5l1 1.8a1 1 0 0 1-.2 1.1l-1.7 1.4a7.8 7.8 0 0 1 0 2.1L19.4 15Z"
                                fill="currentColor"
                            />
                        </svg>
                        <span>{t("navbar.settings")}</span>
                    </button>

                    <button
                        onClick={onLoginClick}
                        className={styles.loginButton}
                        aria-label={t("navbar.login")}
                        title={t("navbar.login")}
                        type="button"
                    >
                        {/* Icône Connexion (porte + flèche) */}
                        <svg
                            className={styles.btnIcon}
                            viewBox="0 0 24 24"
                            aria-hidden="true"
                            focusable="false"
                        >
                            <path
                                d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"
                                fill="none"
                                stroke="currentColor"
                                strokeWidth="2"
                                strokeLinecap="round"
                            />
                            <path
                                d="M10 17l-5-5 5-5"
                                fill="none"
                                stroke="currentColor"
                                strokeWidth="2"
                                strokeLinecap="round"
                                strokeLinejoin="round"
                            />
                            <path
                                d="M15 12H5"
                                fill="none"
                                stroke="currentColor"
                                strokeWidth="2"
                                strokeLinecap="round"
                            />
                        </svg>
                        <span>{t("navbar.login")}</span>
                    </button>
                </div>
            </div>
        </nav>
    );
}
export default NavBar;
