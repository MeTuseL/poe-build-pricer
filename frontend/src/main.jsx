import React from 'react'
import ReactDOM from 'react-dom/client'
import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import Home from "./pages/Home/index.jsx";
import "./styles/index.css"
import ErrorPage from "./pages/ErrorPage/index.jsx";
import BuildsView from "./pages/BuildsView/index.jsx";
import Layout from "./components/Layout/index.jsx";

/**
 * Main entry point for the Argent Bank application.
 *
 * This script sets up the application's routing and state management
 * using React Router and Redux.
 *
 * @category Router
 */

// Create the application's routing configuration
const router = createBrowserRouter(
    [
        {
            path: '/',
            element: <Layout />,
            errorElement: <ErrorPage />,
            children: [
                {
                    index: true,
                    element: <Home />,
                },
                {
                    path: "builds",
                    element: <BuildsView />,
                }
            ],
        },
    ],
    {
        basename: '/poe-pricer-tools',
    }
)
// Render the application with Redux Provider and Router Provider
ReactDOM.createRoot(document.getElementById('root')).render(
    <React.StrictMode>
            <RouterProvider router={router} />
    </React.StrictMode>
)
