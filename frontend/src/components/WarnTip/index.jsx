import React, { useEffect, useRef, useState } from "react";
import styles from "./styles/WarnTip.module.css";
import { useI18n } from "../../__core__";

/** Construit un lien PoE Trade de secours à partir de l'item. */
function buildTradeUrl(entry, league = "Standard") {
    const label =
        entry?.name || entry?.itemBase || entry?.subType || entry?.type || "item";
    const q = encodeURIComponent(label);
    return `https://www.pathofexile.com/trade/search/${league}?q=${q}`;
}

/**
 * Icône d'avertissement + tooltip (anti-flicker, délais 60/200ms)
 * Props :
 *  - entry: l’item concerné (obligatoire)
 *  - league: nom de la ligue PoE (défaut "Standard")
 *  - title / message / linkLabel : surcharges optionnelles (sinon i18n)
 */
export default function WarnTip({
                                    entry,
                                    league = "Standard",
                                    title,
                                    message,
                                    linkLabel
                                }) {
    const { t } = useI18n();

    // Textes traduits (surchargés si props fournis)
    const TTL = title ?? t("pricing.warn.title");
    const MSG = message ?? t("pricing.warn.message");
    const LBL = linkLabel ?? t("pricing.warn.link");

    const [open, setOpen] = useState(false);
    const bubbleRef = useRef(null);

    // Timers anti-flicker
    const openTimer = useRef(null);
    const closeTimer = useRef(null);
    const clearTimers = () => {
        if (openTimer.current) clearTimeout(openTimer.current);
        if (closeTimer.current) clearTimeout(closeTimer.current);
        openTimer.current = null;
        closeTimer.current = null;
    };
    const scheduleOpen = () => {
        if (open) return;
        clearTimeout(openTimer.current);
        openTimer.current = setTimeout(() => setOpen(true), 60);
    };
    const scheduleClose = () => {
        clearTimeout(closeTimer.current);
        closeTimer.current = setTimeout(() => setOpen(false), 200);
    };

    useEffect(() => () => clearTimers(), []);

    const url = buildTradeUrl(entry, league);

    return (
        <span
            className={styles.warnWrap}
            onMouseEnter={() => {
                clearTimeout(closeTimer.current);
                scheduleOpen();
            }}
            onMouseLeave={(e) => {
                const to = e.relatedTarget;
                if (bubbleRef.current && to && bubbleRef.current.contains(to)) return;
                scheduleClose();
            }}
        >
      {/* Icône warning (SVG) */}
            <svg
                className={styles.warnIcon}
                viewBox="0 0 24 24"
                aria-hidden="true"
                focusable="false"
            >
        <path d="M12 3l9.196 16H2.804L12 3z" fill="currentColor" opacity="0.2" />
        <path d="M12 8v5m0 3h.01" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
      </svg>

            {open && (
                <div
                    ref={bubbleRef}
                    className={styles.warnBubble}
                    role="tooltip"
                    onMouseEnter={() => {
                        clearTimeout(closeTimer.current);
                        setOpen(true);
                    }}
                    onMouseLeave={() => scheduleClose()}
                >
                    <div className={styles.warnTitle}>{TTL}</div>
                    <div className={styles.warnText}>{MSG}</div>
                    <a href={url} target="_blank" rel="noreferrer" className={styles.warnLink}>
                        {LBL}
                    </a>
                </div>
            )}
    </span>
    );
}
