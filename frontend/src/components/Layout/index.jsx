import React from "react";
import NavBar from "../NavBar";
import Footer from "../Footer";
import styles from "./styles/Layout.module.css";
import { Outlet } from 'react-router-dom'

export function Layout() {
    return (
        <div className={styles.layout}>
            <NavBar
                onSettingsClick={() => alert("Ouvrir paramètres")}
                onLoginClick={() => alert("Connexion")}
            />
            <div className={styles.container}>
                <main className={styles.main}><Outlet /></main>
                <Footer />
            </div>
        </div>
    );
}
export default Layout
