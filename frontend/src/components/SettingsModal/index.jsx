import React from "react";
import Modal from "../Modal";
import Card from "../Card";
import styles from "./styles/SettingsModal.module.css";
import { useTheme, useI18n } from "../../__core__"

export default function SettingsModal({ open, onClose }) {
    const { theme, setTheme, systemPref } = useTheme();
    const { lang, setLang, t } = useI18n();

    return (
        <Modal isOpen={open} onClose={onClose} title={t("settings.title")}>
            <div className={styles.gridLayout}>
                <Card
                    title={t("settings.theme")}
                    description={t("settings.themeDesc")}
                    rightSlot={
                        <select
                            value={theme}
                            onChange={(e) => setTheme(e.target.value)}
                            className={styles.select}
                            aria-label={t("settings.theme")}
                        >
                            <option value="system">{t("settings.system")} ({systemPref})</option>
                            <option value="dark">{t("settings.dark")}</option>
                            <option value="light">{t("settings.light")}</option>
                        </select>
                    }
                />

                <Card
                    title={t("settings.textSize")}
                    description={t("settings.textSizeDesc")}
                    rightSlot={
                        <select
                            className={styles.select}
                            onChange={(e) => {
                                document.documentElement.style.setProperty("--poe-font", e.target.value);
                                localStorage.setItem("poe:font", e.target.value);
                            }}
                            defaultValue={localStorage.getItem("poe:font") || "16px"}
                        >
                            <option value="14px">{t("settings.small")}</option>
                            <option value="16px">{t("settings.normal")}</option>
                            <option value="18px">{t("settings.large")}</option>
                        </select>
                    }
                />

                <Card
                    title={t("settings.anim")}
                    description={t("settings.animDesc")}
                    rightSlot={
                        <label className={styles.switch}>
                            <input
                                type="checkbox"
                                defaultChecked={localStorage.getItem("poe:anim") !== "off"}
                                onChange={(e) => localStorage.setItem("poe:anim", e.target.checked ? "on" : "off")}
                            />
                            <span />
                        </label>
                    }
                />

                <Card
                    title={t("settings.lang")}
                    description={t("settings.langDesc")}
                    rightSlot={
                        <select
                            className={styles.select}
                            value={lang}
                            onChange={(e) => setLang(e.target.value)}
                            aria-label={t("settings.lang")}
                        >
                            <option value="fr">{t("settings.french")}</option>
                            <option value="en">{t("settings.english")}</option>
                        </select>
                    }
                />
            </div>

            <div className={styles.footer}>
                <button className={styles.primary} onClick={onClose}>{t("settings.close")}</button>
            </div>
        </Modal>
    );
}
