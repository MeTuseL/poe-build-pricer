import React, { useState } from "react";
import { Outlet } from "react-router-dom";

import NavBar from "../NavBar";
import Footer from "../Footer";
import SettingsModal from "../SettingsModal"; // ⬅️ ouvert par le bouton "Paramètres"

import styles from "./styles/Layout.module.css";

export function Layout() {
    const [openSettings, setOpenSettings] = useState(false);

    return (
        <div className={styles.layout}>
            <NavBar
                onSettingsClick={() => setOpenSettings(true)}
                onLoginClick={() => console.log("Connexion")}
            />

            <div className={styles.container}>
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
