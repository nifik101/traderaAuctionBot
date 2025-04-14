import { NavLink } from 'react-router-dom';
import '../styles/Navbar.css';

const Navbar = () => {
  return (
    <nav className="navbar">
      <ul className="nav-links">
        <li>
          <NavLink to="/" end className={({ isActive }) => isActive ? 'active' : ''}>
            Dashboard
          </NavLink>
        </li>
        <li>
          <NavLink to="/scripts" className={({ isActive }) => isActive ? 'active' : ''}>
            Scripts
          </NavLink>
        </li>
        <li>
          <NavLink to="/auctions" className={({ isActive }) => isActive ? 'active' : ''}>
            Auctions
          </NavLink>
        </li>
        <li>
          <NavLink to="/statistics" className={({ isActive }) => isActive ? 'active' : ''}>
            Statistics
          </NavLink>
        </li>
      </ul>
    </nav>
  );
};

export default Navbar;
