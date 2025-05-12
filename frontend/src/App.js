import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import NavBar from './components/layout/NavBar';
import Footer from './components/layout/Footer';
import Home from './pages/Home';
import DocumentList from './pages/DocumentList';
import DocumentDetail from './pages/DocumentDetails.js';

export default function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50">
        <NavBar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/documents" element={<DocumentList />} />
          <Route path="/documents/:id" element={<DocumentDetail />} />
        </Routes>
        <Footer />
      </div>
    </Router>
  );
}