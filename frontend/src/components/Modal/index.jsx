import React, { useEffect } from "react";
import styles from "./styles/Modal.module.css";

export default function Modal({ isOpen, onClose, title, children }) {
    useEffect(() => {
        function onKey(e) { if (e.key === "Escape") onClose?.(); }
        if (isOpen) document.addEventListener("keydown", onKey);
        return () => document.removeEventListener("keydown", onKey);
    }, [isOpen, onClose]);

    if (!isOpen) return null;

    return (
        <div className={styles.overlay} onMouseDown={onClose} role="dialog" aria-modal="true">
            <div className={styles.modal} onMouseDown={(e) => e.stopPropagation()}>
                <div className={styles.header}>
                    <h3 className={styles.title}>{title}</h3>
                    <button className={styles.close} onClick={onClose} aria-label="Fermer">×</button>
                </div>
                <div className={styles.content}>{children}</div>
            </div>
        </div>
    );
}
