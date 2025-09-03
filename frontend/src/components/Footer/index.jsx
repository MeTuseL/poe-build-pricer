import styles from "./styles/Footer.module.css";

export function Footer() {
    return (
        <footer className={styles.footer}>
            © {new Date().getFullYear()} PoE Pricer — Tous droits réservés.
        </footer>
    );
}
export default Footer