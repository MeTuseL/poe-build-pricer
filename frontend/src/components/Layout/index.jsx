import React, { useState } from "react";
import { Outlet, useLocation } from "react-router-dom";

import NavBar from "../NavBar";
import Footer from "../Footer";
import SettingsModal from "../SettingsModal";

import styles from "./styles/Layout.module.css";

export function Layout() {
    const [openSettings, setOpenSettings] = useState(false);
    const location = useLocation();

    const isPricing =
        location.pathname.endsWith("/pricing") ||
        location.pathname.includes("/pricing");

    const containerClass = `${styles.container} ${isPricing ? styles.containerWide : ""}`;

    return (
        <div className={styles.layout}>
            <NavBar
                onSettingsClick={() => setOpenSettings(true)}
                onLoginClick={() => console.log("Connexion")}
            />

            <div className={containerClass}>
                <main className={styles.main}>
                    <Outlet />
                </main>
            </div>

            <Footer />

            <SettingsModal
                open={openSettings}
                onClose={() => setOpenSettings(false)}
            />
        </div>
    );
}
export default Layout;
