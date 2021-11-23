import {useParams} from "react-router-dom";
import { useEffect, useState } from "react";
import Axios from 'axios'

const PlayerDetails = () => {
    const { id } = useParams(); //Here we destructing value from useParams
    console.log(id)

    const [Pdatas,setData] = useState([])

    useEffect(() => {
      Axios.get(`http://127.0.0.1:8000/player/${id}/`)
      .then((res) => setData(res.data));              // by using this we capture data whatever comming , and comming  data is Javascript Object
    },[id] );
    
    console.log(Pdatas)
    return (
        <>               

        <div class="wrapper">
            <div class="Pprofile-card">
                <div class="profile-card__img">
                    <img src={Pdatas.picture} alt="profile card" />
                </div>
                <div>
                    <h1>{Pdatas.playerName}</h1>
                </div>
                <div style={{width: '40%', float: 'left', textAlign: 'left', marginLeft : '70px', fontWeight: '700'}}>
                    <div style={{ left : "20px"}}>
                        <span>Team Name : {Pdatas.team}</span>
                    </div>
                    <div style={{left : "20px"}}>
                        <span>description : {Pdatas.description}</span>
                    </div>
                </div>
                <div style={{width: '40%', float: 'right',textAlign: 'left',fontWeight: '700'}}>
                    <div style={{ left : "10px"}}>
                        <span>Price : {Pdatas.price}</span>
                    </div>
                    <div style={{left : "10px"}}>
                        <span> isPlaying : {Pdatas.isPlaying}</span>
                    </div>
                </div>
            </div>
            
        </div>


        </>
    )

}

export { PlayerDetails }