import React, { useState } from "react";
import { useRouteError } from "react-router-dom";
import NavBar from "../NavBar";
import Footer from "../Footer";
import SettingsModal from "../SettingsModal";
import Status from "../Status";

export function ErrorLayout() {
    const err = useRouteError?.() || {};
    const status = err?.status ?? err?.statusCode ?? "";
    const message = err?.statusText ?? err?.message ?? "";
    const [open, setOpen] = useState(false);

    return (
        <>
            <NavBar onSettingsClick={() => setOpen(true)} onLoginClick={() => {}} />
            <Status status={status} message={message} />
            <Footer />
            <SettingsModal open={open} onClose={() => setOpen(false)} />
        </>
    );
}
export default ErrorLayout;
