import React, { useEffect, useMemo, useState } from "react";
import { useLocation, Link } from "react-router-dom";
import styles from "./styles/PricingBuild.module.css";
import { useI18n } from "../../__core__";

import { formatBuild } from "../../__services__/build-formatter.js";
import {
    loadOverrides,
    setOverrideDivine,
    getDivinePrice,
    sumDivine,
} from "../../__services__/price-overrides.js";

import LoadingOverlay from "../../components/LoadingOverlay";
import { ItemIcon } from "../../components/Icons";
import ItemTooltip from "../../components/ItemTooltip";
import WarnTip from "../../components/WarnTip";
import ErrorMsg from "../../components/ErrorMsg";
import divineIcon from "../../assets/currency/divine.png";

export default function PricingBuild() {
    const { t } = useI18n();
    const backLabel = t("pricing.back").replace(/^←\s*/i, "").trim();
    const location = useLocation();
    const pobData = location.state?.pobData;

    const [overrides, setOverrides] = useState(loadOverrides());
    const [loading, setLoading] = useState(true);

    // TODO: remplacer par ton vrai état d'auth plus tard (context/Redux)
    const isAuthenticated = false;

    const summary = useMemo(() => (pobData ? formatBuild(pobData) : null), [pobData]);

    useEffect(() => {
        const id = setTimeout(() => setLoading(false), 300);
        return () => clearTimeout(id);
    }, []);

    if (!pobData) {
        return (
            <div className={styles.page}>
                <h1 className={styles.title}>{t("pricing.title")}</h1>
                <p className={styles.noData}>{t("pricing.noData")}</p>
                <Link to="/" className={styles.backLink}>{t("pricing.back")}</Link>
            </div>
        );
    }

    if (!summary) {
        return (
            <div className={styles.page}>
                <LoadingOverlay show />
            </div>
        );
    }

    const DivineTag = () => (
        <img src={divineIcon} alt="Divine" className={styles.currencyIcon} />
    );

    const row = (entry, labelType) => {
        if (!entry) return null;
        const v = getDivinePrice(entry, overrides);
        const hasValue = v != null;
        const display = hasValue ? String(Math.round(v * 100) / 100) : "";
        const rarity = (entry.rarity || "").toLowerCase();

        return (
            <div key={entry._key} className={styles.itemRow}>
                <ItemIcon type={labelType || entry.subType || entry.type} className={styles.icon} />

                <div className={styles.itemMain}>
                    <ItemTooltip item={entry}>
                        <div className={styles.itemName}>{entry.name || entry.itemBase}</div>
                    </ItemTooltip>
                    <div className={`${styles.badge} ${styles[`rar_${rarity}`]}`}>{entry.rarity}</div>
                </div>

                <div className={styles.priceBox}>
                    <input
                        className={`${styles.priceInput} ${!hasValue ? styles.priceInputError : ""}`}
                        type="text"
                        inputMode="decimal"
                        placeholder="N/A"
                        value={display}
                        onChange={(e) => {
                            const raw = e.target.value.trim();
                            const normalized = raw.replace(",", ".");
                            const next = setOverrideDivine(
                                { ...overrides },
                                entry._key,
                                normalized === "" ? "" : normalized
                            );
                            setOverrides({ ...next });
                        }}
                        aria-label="Prix (Divine)"
                    />
                    <DivineTag />
                    {!hasValue && <WarnTip entry={entry} />}
                </div>
            </div>
        );
    };

    const equipment = summary.equipment || [];
    const jewels = [
        ...summary.jewels.base,
        ...summary.jewels.abyss,
        ...summary.jewels.timeless,
        ...summary.jewels.cluster.large,
        ...summary.jewels.cluster.medium,
        ...summary.jewels.cluster.small
    ];
    const gemsBySlot = summary.gemsBySlot;
    const flasks = summary.flasks;

    const totals = {
        equipment: sumDivine(equipment, overrides),
        jewels: sumDivine(jewels, overrides),
        gems: sumDivine(Object.values(gemsBySlot).flat(), overrides),
        flasks: sumDivine(flasks, overrides)
    };
    const totalAll = totals.equipment + totals.jewels + totals.gems + totals.flasks;

    const klass = summary.classes?.characterClass || "-";
    const ascend = summary.classes?.ascendancy || "-";

    return (
        <div className={styles.page}>
            <LoadingOverlay show={loading} />

            <div className={styles.headerRow}>
                <div className={styles.backTop}>
                    <Link to="/" className={styles.backBtn} aria-label={t("pricing.back")}>
                        <svg viewBox="0 0 24 24" className={styles.backBtnIcon} aria-hidden="true">
                            <path d="M15 18l-6-6 6-6" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                        </svg>
                        <span>{backLabel}</span>
                    </Link>
                </div>

                <h1 className={styles.title}>
                    {t("pricing.title")} — {klass} ({ascend})
                </h1>

                <div style={{ width: 1 }} />
            </div>

            <div className={styles.grid}>
                {/* 1. Équipements */}
                <section className={`${styles.card} ${styles.cardTall}`}>
                    <h2 className={styles.cardTitle}>{t("pricing.sections.equipment")}</h2>
                    {equipment.map((it) => row(it))}
                </section>

                {/* 2. Joyaux */}
                <section className={styles.card}>
                    <h2 className={styles.cardTitle}>{t("pricing.sections.jewels")}</h2>
                    {jewels.map((j) => row(j, "Jewel"))}
                </section>

                {/* 3. Gemmes */}
                <section className={styles.card}>
                    <h2 className={styles.cardTitle}>{t("pricing.sections.gems")}</h2>
                    {Object.entries(gemsBySlot).map(([slot, list]) => (
                        <div key={slot} className={styles.slotBlock}>
                            <div className={styles.slotTitle}>{slot}</div>
                            {list.map((g) => {
                                const gv = getDivinePrice(g, overrides);
                                const gHasValue = gv != null;
                                const gDisplay = gHasValue ? String(Math.round(gv * 100) / 100) : "";

                                return (
                                    <div key={g._key} className={styles.itemRow}>
                                        <ItemIcon type="Gem" className={styles.icon} />
                                        <div className={styles.itemMain}>
                                            <ItemTooltip item={{ ...g, type: "Gem", _gem: true }}>
                                                <div className={styles.itemName}>{g.name}</div>
                                            </ItemTooltip>
                                            <div className={styles.gemMeta}>
                                                Lv {g.level} • Q{g.quality}{g.corrupted ? " • Corrupted" : ""}
                                            </div>
                                        </div>
                                        <div className={styles.priceBox}>
                                            <input
                                                className={`${styles.priceInput} ${!gHasValue ? styles.priceInputError : ""}`}
                                                type="text"
                                                inputMode="decimal"
                                                placeholder="N/A"
                                                value={gDisplay}
                                                onChange={(e) => {
                                                    const raw = e.target.value.trim();
                                                    const normalized = raw.replace(",", ".");
                                                    const next = setOverrideDivine(
                                                        { ...overrides },
                                                        g._key,
                                                        normalized === "" ? "" : normalized
                                                    );
                                                    setOverrides({ ...next });
                                                }}
                                                aria-label="Prix (Divine)"
                                            />
                                            <DivineTag />
                                            {!gHasValue && <WarnTip entry={g} />}
                                        </div>
                                    </div>
                                );
                            })}
                        </div>
                    ))}
                </section>

                {/* 4. Flacons + Total */}
                <aside className={styles.sideCol}>
                    <section className={styles.card}>
                        <h2 className={styles.cardTitle}>{t("pricing.sections.flasks")}</h2>
                        {flasks.map((f) => row(f, "Flask"))}
                    </section>

                    <section className={styles.totalCard}>
                        <div className={styles.totalLabel}>{t("pricing.total")}</div>
                        <div className={styles.totalValue}>
                            {Math.round(totalAll * 100) / 100}{" "}
                            <img src={divineIcon} alt="Divine" className={styles.currencyIcon} />
                        </div>
                        <div className={styles.totalBreak}>
                            {t("pricing.breakdown.equipment")}: {Math.round(totals.equipment * 100) / 100} •{" "}
                            {t("pricing.breakdown.jewels")}: {Math.round(totals.jewels * 100) / 100} •{" "}
                            {t("pricing.breakdown.gems")}: {Math.round(totals.gems * 100) / 100} •{" "}
                            {t("pricing.breakdown.flasks")}: {Math.round(totals.flasks * 100) / 100}
                        </div>

                        {/* Save désactivé si non connecté + message */}
                        <button
                            className={isAuthenticated ? styles.saveBtnBottom : styles.saveBtnDisabled}
                            type="button"
                            disabled={!isAuthenticated}
                            aria-disabled={!isAuthenticated}
                            title={!isAuthenticated ? t("home.reserved") : undefined}
                        >
                            {t("pricing.save")}
                        </button>

                        {!isAuthenticated && (
                            <ErrorMsg message={t("home.reserved")} />
                        )}
                    </section>
                </aside>
            </div>

            <div className={styles.backBottom}>
                <Link to="/" className={styles.backBtn} aria-label={t("pricing.back")}>
                    <svg viewBox="0 0 24 24" className={styles.backBtnIcon} aria-hidden="true">
                        <path d="M15 18l-6-6 6-6" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                    </svg>
                    <span>{backLabel}</span>
                </Link>
            </div>
        </div>
    );
}
