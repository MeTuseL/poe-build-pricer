import React, { createContext, useContext, useEffect, useMemo, useState } from "react";
import fr from "./translations/fr.json";
import en from "./translations/en.json";

const I18nContext = createContext();
const LANG_KEY = "poe:lang";
const DICT = { fr, en };

export function I18nProvider({ children }) {
    const initial = (() => {
        const saved = typeof window !== "undefined" ? localStorage.getItem(LANG_KEY) : null;
        if (saved) return saved;
        // déduire depuis le navigateur si rien de stocké
        const nav = typeof navigator !== "undefined" ? navigator.language.toLowerCase() : "fr";
        return nav.startsWith("en") ? "en" : "fr";
    })();

    const [lang, setLang] = useState(initial);

    useEffect(() => {
        localStorage.setItem(LANG_KEY, lang);
        if (typeof document !== "undefined") {
            document.documentElement.setAttribute("lang", lang);
        }
    }, [lang]);

    const t = (path) => {
        const parts = path.split(".");
        let cur = DICT[lang] ?? DICT.fr;
        for (const p of parts) cur = cur?.[p];
        return cur ?? path;
    };

    const value = useMemo(() => ({ lang, setLang, t }), [lang]);
    return <I18nContext.Provider value={value}>{children}</I18nContext.Provider>;
}

export function useI18n() {
    const ctx = useContext(I18nContext);
    if (!ctx) throw new Error("useI18n must be used inside I18nProvider");
    return ctx;
}
