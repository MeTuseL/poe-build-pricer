import React from 'react'
import ReactDOM from 'react-dom/client'
import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import {Home} from "./pages/Home/index.jsx";
import "./styles/index.css"
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
            element: <Home />,
            /*errorElement: <ErrorPage />, */
            children: [
                {
                    index: true,
                    element: <Home />,
                },
            ],
        },
    ],
    {
        basename: '/',
    }
)
// Render the application with Redux Provider and Router Provider
ReactDOM.createRoot(document.getElementById('root')).render(
    <React.StrictMode>
            <RouterProvider router={router} />
    </React.StrictMode>
)
