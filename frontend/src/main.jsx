import React from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import HomePage from './pages/HomePage'
import PortfolioPage from './pages/PortfolioPage'
import RiotLookup from './pages/RiotLookup'
import './index.css'

createRoot(document.getElementById('root')).render(
	<React.StrictMode>
		<BrowserRouter>
					<Routes>
						<Route path="/" element={<HomePage />} />
						<Route path="/portfolio" element={<PortfolioPage />} />
						<Route path="/lookup" element={<RiotLookup />} />
					</Routes>
		</BrowserRouter>
	</React.StrictMode>
)
