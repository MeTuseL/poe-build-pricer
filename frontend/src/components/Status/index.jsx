import React from "react";
import { Link } from "react-router-dom";
import styles from "./styles/Status.module.css";
import { useI18n } from "../../__core__";

export default function Status({ status, message }) {
    const { t } = useI18n();

    return (
        <div className={styles.wrapper}>
            <div className={styles.card}>
                <div className={styles.icon} aria-hidden>⚠️</div>
                <h1 className={styles.title}>{t("errorPage.title")}</h1>
                <p className={styles.subtitle}>{t("errorPage.subtitle")}</p>

                {(status || message) && (
                    <div className={styles.detailBox}>
                        <div className={styles.detailTitle}>{t("errorPage.details")}</div>
                        <div className={styles.detailContent}>
                            {status && <span className={styles.badge}>#{status}</span>}
                            {message && <span>{message}</span>}
                        </div>
                    </div>
                )}

                <Link to="/" className={styles.back}>{t("errorPage.backHome")}</Link>
            </div>
        </div>
    );
}
