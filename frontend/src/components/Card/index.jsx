import React from "react";
import styles from "./styles/Card.module.css";

export default function Card({ title, description, rightSlot, children }) {
    return (
        <div className={styles.card}>
            <div className={styles.row}>
                <div>
                    {title && <div className={styles.title}>{title}</div>}
                    {description && <div className={styles.desc}>{description}</div>}
                </div>
                {rightSlot ? <div className={styles.right}>{rightSlot}</div> : null}
            </div>
            {children ? <div className={styles.body}>{children}</div> : null}
        </div>
    );
}
