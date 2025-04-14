import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { useUser } from '@clerk/clerk-react';
import Layout from './components/Layout';
import ProtectedRoute from './components/ProtectedRoute';
import Dashboard from './pages/Dashboard';
import ScriptManagement from './pages/ScriptManagement';
import AuctionListing from './pages/AuctionListing';
import Statistics from './pages/Statistics';
import './App.css';

function App() {
  const { isSignedIn, isLoaded } = useUser();

  if (!isLoaded) {
    return <div className="loading">Loading...</div>;
  }

  return (
    <Router>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={
            isSignedIn ? <Navigate to="/dashboard" /> : <Navigate to="/login" />
          } />
          <Route path="/login" element={
            isSignedIn ? <Navigate to="/dashboard" /> : <div>Login Page</div>
          } />
          <Route path="/dashboard" element={
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          } />
          <Route path="/scripts" element={
            <ProtectedRoute>
              <ScriptManagement />
            </ProtectedRoute>
          } />
          <Route path="/auctions" element={
            <ProtectedRoute>
              <AuctionListing />
            </ProtectedRoute>
          } />
          <Route path="/statistics" element={
            <ProtectedRoute>
              <Statistics />
            </ProtectedRoute>
          } />
          <Route path="*" element={<div>404 Not Found</div>} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App;
