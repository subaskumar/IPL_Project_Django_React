//import ReactDOM from "react-dom";
import { Link, NavLink } from "react-router-dom";
import { MdSportsCricket } from "react-icons/md";
import { useState} from "react"
import { FcSearch } from "react-icons/fc";
import Axios from 'axios'
import {useNavigate} from 'react-router-dom';

const NavBar = () => {
    const [search,setSearchplayer] = useState("")
    const [searchData,setSearchData] = useState({})
    const navigate = useNavigate()
    const handleSubmit = (e) =>{
        e.preventDefault();         // meaning that the default action that belongs to the event will not occur.
        const inputs = new FormData()
        inputs.append('teamName',search);

        Axios.post("http://127.0.0.1:8000/search/", inputs)
            .then((res) => {setSearchData(res.data) 
                navigate('/search')
                console.log(searchData)

            })
            .catch(function(error){
                    if(error.response){
                        console.log(error.message);
                        console.log(error.response);
            }
        })

    }
return (
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
       <div className=''>
            <form className='' onSubmit={handleSubmit} style={{display: "flex"}}>
                <input id='formPName' className='' name='teamName' type='text' placeholder='Search Team player' onChange={(e)=> setSearchplayer(e.target.value)} value={search} />
                <button type="submit" style={{fontSize: '25px', cursor: 'pointer', paddingTop: '10x'}}><FcSearch /></button>
            </form>
            
        </div
        
    </nav>
);
//GiCricketBat, MdSportsCricket,MdOutlineSportsCricket
export { NavBar }
