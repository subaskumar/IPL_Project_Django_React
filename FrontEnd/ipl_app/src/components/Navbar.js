//import ReactDOM from "react-dom";
import { Link, NavLink } from "react-router-dom";
//import { GiCricketBat } from "react-icons/gi";
import { MdSportsCricket } from "react-icons/md";

const NavBar = () => (
    <nav className='navbar'>
        <div className='navbar__title'>
            
            <Link to="/" className="logoName"><MdSportsCricket className="logo1"/> IPL Buzz</Link>
        </div>
        <div className='navbar__item'>
            <NavLink to="/addPlayer">Add Player</NavLink>
        </div>
        <div className='navbar__item'>
            <NavLink to="/addTeam">Add Team</NavLink>
        </div>
        
    </nav>
);
//GiCricketBat, MdSportsCricket,MdOutlineSportsCricket
export { NavBar }