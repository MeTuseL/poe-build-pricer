import React from 'react';
import ReactDOM from 'react-dom/client';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';

import Home from "./pages/Home/index.jsx";
import "./styles/index.css";
import BuildsView from "./pages/BuildsView/index.jsx";
import Layout from "./components/Layout/index.jsx";
import PricingBuild from "./pages/PricingBuild/index.jsx";

import AppProviders from "./__core__/providers/AppProviders.jsx";
import StatusPage from "./pages/StatusPage/index.jsx";
import ErrorLayout from "./components/ErrorLayout/index.jsx";

// Routing configuration
const router = createBrowserRouter(
    [
        {
            path: '/',
            element: <Layout />,
            errorElement: <ErrorLayout />,
            children: [
                { index: true, element: <Home /> },
                { path: 'builds', element: <BuildsView /> },
                { path: 'pricing', element: <PricingBuild /> },
                { path: '*', element: <StatusPage /> },
            ],
        },
    ],
    {
        basename: '/poe-pricer-tools',
    }
);

ReactDOM.createRoot(document.getElementById('root')).render(
    <React.StrictMode>
        <AppProviders>
            <RouterProvider router={router} />
        </AppProviders>
    </React.StrictMode>
);
