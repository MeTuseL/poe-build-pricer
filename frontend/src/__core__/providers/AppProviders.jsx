import React, { useEffect } from "react";
import { ThemeProvider, I18nProvider } from "../index.js";

export default function AppProviders({ children }) {
    useEffect(() => {
        const saved = localStorage.getItem("poe:font");
        if (saved) document.documentElement.style.setProperty("--poe-font", saved);
    }, []);

    return (
        <ThemeProvider>
            <I18nProvider>{children}</I18nProvider>
        </ThemeProvider>
    );
}
