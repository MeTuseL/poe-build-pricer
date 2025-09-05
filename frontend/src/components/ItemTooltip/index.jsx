import React, { useEffect, useLayoutEffect, useRef, useState } from "react";
import { createPortal } from "react-dom";
import styles from "./styles/ItemTooltip.module.css";
import { ItemIcon } from "../Icons";
import { isGem as isGemUtil, getItemTitleVariant } from "../../__utils__/items.js";

/**
 * Tooltip PoE rendu dans un portal (au-dessus de tout).
 * - Anti-flicker : délais d'ouverture/fermeture
 * - Positionnement auto (right/left/bottom) + clamp viewport
 */
export default function ItemTooltip({ item, children, side = "auto" }) {
    const triggerRef = useRef(null);
    const bubbleRef = useRef(null);
    const [open, setOpen] = useState(false);
    const [pos, setPos] = useState({ top: 0, left: 0, placement: "right" });

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

    // Map propriétés à afficher
    const propsToShow = [
        "Item Level",
        "LevelReq",
        "Quality",
        "Sockets",
        "Energy Shield",
        "Armour",
        "Evasion",
        "Radius"
    ];
    const propMap = {};
    (item?.properties || []).forEach((p) => {
        if (p?.name && p?.values != null) propMap[p.name] = String(p.values);
    });

    const isGem = isGemUtil(item);
    const gemLines = isGem
        ? [
            item?.level != null ? `Level: ${item.level}` : null,
            item?.quality != null ? `Quality: ${item.quality}%` : null,
            item?.corrupted || item?.Corrupted ? "Corrupted" : null
        ].filter(Boolean)
        : [];

    const implicitMods = Array.isArray(item?.implicitMods) ? item.implicitMods : [];
    const explicitMods = Array.isArray(item?.explicitMods) ? item.explicitMods : [];

    // Positionnement (viewport/fixed)
    const computePosition = () => {
        const t = triggerRef.current;
        const b = bubbleRef.current;
        if (!t || !b) return;

        const tr = t.getBoundingClientRect();
        const bw = b.offsetWidth;
        const bh = b.offsetHeight;

        const margin = 12;
        const vw = window.innerWidth;
        const vh = window.innerHeight;

        let placement = side === "auto" ? "right" : side;
        let left, top;

        const placeRight = () => { left = tr.right + margin; top = tr.top + tr.height / 2 - bh / 2; };
        const placeLeft  = () => { left = tr.left - margin - bw; top = tr.top + tr.height / 2 - bh / 2; };
        const placeBottom= () => { left = tr.left; top = tr.bottom + margin; };

        if (placement === "right") placeRight();
        else if (placement === "left") placeLeft();
        else if (placement === "bottom") placeBottom();
        else placeRight();

        if (side === "auto") {
            if (left + bw + 8 > vw) { placement = "left"; placeLeft(); }
            if (left < 8)           { placement = "right"; placeRight(); }
            if (top < 8 || top + bh + 8 > vh) { placement = "bottom"; placeBottom(); }
        }

        left = Math.max(8, Math.min(left, vw - bw - 8));
        top  = Math.max(8, Math.min(top,  vh - bh - 8));
        setPos({ top, left, placement });
    };

    useLayoutEffect(() => {
        if (!open) return;
        computePosition();
        const onWin = () => computePosition();
        window.addEventListener("scroll", onWin, true);
        window.addEventListener("resize", onWin, true);
        return () => {
            window.removeEventListener("scroll", onWin, true);
            window.removeEventListener("resize", onWin, true);
        };
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [open, side, item]);

    useEffect(() => () => clearTimers(), []);

    // Couleur du titre
    const variant = getItemTitleVariant(item); // "Gem" | "Unique" | "Rare" | "Magic" | "Normal"
    const titleClass = styles["title" + variant] || styles.titleNormal;

    return (
        <span
            ref={triggerRef}
            className={styles.trigger}
            onMouseEnter={() => {
                clearTimeout(closeTimer.current);
                scheduleOpen();
            }}
            onMouseLeave={(e) => {
                const to = e.relatedTarget;
                if (bubbleRef.current && to && bubbleRef.current.contains(to)) {
                    return; // on entre dans la bulle → ne pas fermer
                }
                scheduleClose();
            }}
        >
      {children}

            {open &&
                createPortal(
                    <div
                        ref={bubbleRef}
                        className={`${styles.bubble} ${styles["place_" + pos.placement]}`}
                        style={{ top: pos.top, left: pos.left }}
                        role="tooltip"
                        onMouseEnter={() => {
                            clearTimeout(closeTimer.current);
                            setOpen(true);
                        }}
                        onMouseLeave={() => scheduleClose()}
                    >
                        {/* Header : titre coloré (pas de badge de rareté) + icône */}
                        <div className={styles.header}>
                            <div className={styles.headerMain}>
                                <div className={`${styles.name} ${titleClass}`}>
                                    {item?.name || item?.itemBase || item?.nameSpec || "Unknown"}
                                </div>
                                {item?.itemBase && item?.name && (
                                    <div className={styles.base}>{item.itemBase}</div>
                                )}
                            </div>
                            <ItemIcon type={item?.subType || item?.type || "Unknown"} className={styles.icon} />
                        </div>

                        {/* Propriétés */}
                        <div className={styles.props}>
                            {isGem && gemLines.length > 0 && (
                                <ul className={styles.propList}>
                                    {gemLines.map((l, i) => <li key={`g-${i}`}>{l}</li>)}
                                </ul>
                            )}
                            {!isGem && (
                                <ul className={styles.propList}>
                                    {propsToShow.map((k) =>
                                        propMap[k] ? (
                                            <li key={k}>
                                                <span className={styles.propKey}>{k}</span> {propMap[k]}
                                            </li>
                                        ) : null
                                    )}
                                </ul>
                            )}
                        </div>

                        {/* Mods */}
                        {implicitMods.length > 0 && (
                            <div className={styles.block}>
                                <div className={styles.blockTitle}>IMPLICIT</div>
                                <ul className={styles.implicitList}>
                                    {implicitMods.map((m, i) => <li key={`imp-${i}`}>{m}</li>)}
                                </ul>
                            </div>
                        )}

                        {explicitMods.length > 0 && (
                            <div className={styles.block}>
                                <div className={styles.blockTitle}>EXPLICIT</div>
                                <ul className={styles.explicitList}>
                                    {explicitMods.map((m, i) => <li key={`exp-${i}`}>{m}</li>)}
                                </ul>
                            </div>
                        )}
                    </div>,
                    document.body
                )}
    </span>
    );
}
