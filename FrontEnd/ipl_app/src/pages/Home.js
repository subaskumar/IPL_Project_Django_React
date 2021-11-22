import { useEffect, useState } from "react";
import Axios from 'axios'
import { Link } from "react-router-dom";

function Card(props){
  return (
    
    <Link to={`/teamDetails/${props.id}`}  className="teamdetails">

      <div className="card-body" >
          <div className="icon-wrapper section">
              <img src={props.pic} alt={props.name} />
          </div>
          <div className="text-wrapper section1">
              <div className="title"><span >Team Name : <b style={{fontWeight : 500, color: "pink" }}> {props.name}</b></span></div>
              <div className="details"><span>Championship Won : {props.win}</span></div>
              <div className="details"><span style={{color: "white"}}>Total Player : {props.players}</span></div>

          </div>
      </div>
    </Link>
  )
}

const Home = () => {
    const [datas,setData] = useState([])

    useEffect(() => {
      Axios.get("http://127.0.0.1:8000/Ipl_Team/")
      .then((res) => setData(res.data));              // by using this we capture data whatever comming , and comming  data is Javascript Object
    },[] );

    return (
      <>
        <div className="card-grid-view">
            {datas.map((data) => (

                <Card id ={data.id} key={data.teamName} name={data.teamName} win={data.champ_win} pic={data.icon} players={data.total_player} />
            ))}

        </div>
      </>
    )
  };
  
  export {Home };