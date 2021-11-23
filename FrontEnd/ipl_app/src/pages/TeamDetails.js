import {useParams} from "react-router-dom";
import { useEffect, useState } from "react";
import Axios from 'axios'
import { Link } from "react-router-dom";


function Card(props){
    return (
      
      <Link to='/'  className="teamdetails">
  
        <div className="outrPlayer" >
            <div className="Playercard-body">
                <img src={props.pic} alt={props.name} />
            </div>
            <div style={{marginLeft: "10px", textAlign: 'left'}}>
                <h5>Name : {props.name}</h5>
                <span>Team : {props.team}</span>
                <span>Price : {props.price}</span>
                <span>Roll : {props.role}</span>
                <span>Status : {props.playStatus}</span>
            </div>
        </div>
      </Link>
    )
  }

const TeamDetails = () => {
    const { id } = useParams();
    console.log(id)

    const [Pdatas,setData] = useState([])

    useEffect(() => {
      Axios.get(`http://127.0.0.1:8000/Ipl_Team/${id}/`)
      .then((res) => setData(res.data));              // by using this we capture data whatever comming , and comming  data is Javascript Object
    },[id] );
    
    console.log(Pdatas)
    return (
        <>               
            <div className="TeamProfile">
                <div className="innerProfile">
                    <div class="profile-image">
                        <img src={Pdatas.icon} alt={Pdatas.teamName} />
                    </div>
                    <div className="teaminfo">
                        <div>
                            <h2>Team Name : <b> {Pdatas.teamName}</b></h2>
                        </div>
                        <div>
                            <h3>Chompionship Won : <b> {Pdatas.champ_win}</b></h3>
                        </div>
                        <div>
                            <h4>Total Player : {Pdatas.total_player}</h4>
                        </div>
                    </div>                    
                </div>
                <hr/>

                <div className="profile-image-player">
                    <div className="profileinner-player">
                        <div className="batsmanDiv">
                            <div style={{marginBottom : "40px"}}>
                                <h3>Top Batsman</h3>
                            </div>
                            <div className="teamPlayers">
                                {Pdatas.Batsman?.map((datas) => (
                                    <Card id ={datas.id} key={datas.id} name={datas.playerName} role={datas.description} team={datas.team} pic={datas.picture} price={datas.price} playStatus={datas.isPlaying} />
                                    ))}
                            </div>
                        </div>
                        <div className="bowlerDiv">
                            <div style={{marginBottom : "40px"}}>
                                <h3>Top Bowler</h3>
                            </div>
                            <div className="teamPlayers">
                            {Pdatas.Bowler?.map((datas) => (
                                <Card id ={datas.id} key={datas.id} name={datas.playerName} role={datas.description} team={datas.team} pic={datas.picture} price={datas.price} playStatus={datas.isPlaying} />
                            ))}
                        </div>
                        </div>
                    </div>
                </div>
                
            </div>


        </>
    )

}

export { TeamDetails }
