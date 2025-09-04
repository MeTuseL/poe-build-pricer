import React from "react";
import styles from "./styles/LoadingOverlay.module.css";

export default function LoadingOverlay({ show, label = "Loading..." }) {
    if (!show) return null;
    return (
        <div className={styles.wrap} role="status" aria-live="polite">
            <div className={styles.spinner} />
            <div className={styles.text}>{label}</div>
        </div>
    );
}
