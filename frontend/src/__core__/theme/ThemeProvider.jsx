import React, { createContext, useContext, useEffect, useMemo, useState } from "react";

const ThemeContext = createContext(null);
const THEME_KEY = "poe:theme"; // 'system' | 'light' | 'dark'

export function ThemeProvider({ children }) {
    const [theme, setTheme] = useState(() => {
        const saved = typeof window !== "undefined" ? localStorage.getItem(THEME_KEY) : null;
        return saved || "dark";
    });

    useEffect(() => {
        if (typeof document === "undefined") return;
        localStorage.setItem(THEME_KEY, theme);

        const root = document.documentElement;
        const apply = () => {
            if (theme === "system") {
                const prefersLight = window.matchMedia("(prefers-color-scheme: light)").matches;
                root.classList.toggle("dark", !prefersLight);
            } else {
                root.classList.toggle("dark", theme === "dark");
            }
            root.dataset.theme = theme;
        };

        apply();

        // suivre l’OS si "system"
        let mq;
        const onChange = () => apply();
        if (theme === "system") {
            mq = window.matchMedia("(prefers-color-scheme: light)");
            mq.addEventListener?.("change", onChange);
            return () => mq.removeEventListener?.("change", onChange);
        }
    }, [theme]);

    const systemPref = useMemo(() => {
        if (typeof window === "undefined") return "dark";
        return window.matchMedia("(prefers-color-scheme: light)").matches ? "light" : "dark";
    }, []);

    const value = useMemo(() => ({ theme, setTheme, systemPref }), [theme, systemPref]);
    return <ThemeContext.Provider value={value}>{children}</ThemeContext.Provider>;
}

export function useTheme() {
    const ctx = useContext(ThemeContext);
    if (!ctx) throw new Error("useTheme must be used within ThemeProvider");
    return ctx;
}
