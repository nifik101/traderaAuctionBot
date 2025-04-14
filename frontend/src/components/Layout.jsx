import { Outlet } from 'react-router-dom';
import Navbar from './Navbar';
import Sidebar from './Sidebar';
import { UserButton } from '@clerk/clerk-react';
import '../styles/Layout.css';

const Layout = () => {
  return (
    <div className="layout">
      <header className="header">
        <div className="logo">Tradera Assistant</div>
        <Navbar />
        <div className="user-profile">
          <UserButton />
        </div>
      </header>
      <div className="main-container">
        <Sidebar />
        <main className="content">
          <Outlet />
        </main>
      </div>
    </div>
  );
};

export default Layout;
