import {useEffect, useState} from "react"
import Axios from 'axios'
import {useNavigate} from 'react-router-dom';


 function  ReactFormLabel(props) {
     return(
      <label htmlFor={props.htmlFor}>{props.title}</label>
     )
}
function PlayerForm() {

    const navigate = useNavigate();

    const [teamDatas,setTeamData] = useState([])

    useEffect(() => {
      Axios.get("http://127.0.0.1:8000/Ipl_Team/")
      .then((res) => setTeamData(res.data));              // by using this we capture data whatever comming , and comming  data is Javascript Object
    },[] );


    // const [inputsPlayer, setInputPlayer] = useState({});

    const [playerName, setplayerName] = useState("")
    const [team, setTeam] = useState("RCB")
    const [price, setPrice] = useState("")
    const [description, setDescription] = useState("bowler")
    const [isPlaying, setIsPlaying] = useState(false)
    const [picture, setPicture] = useState()
    

    const handleSubmit = (e) => {
            e.preventDefault();
            const inputsPlayer = new FormData()
            inputsPlayer.append('playerName',playerName);
            inputsPlayer.append('team',team);
            inputsPlayer.append('price',price);
            inputsPlayer.append('description',description);
            inputsPlayer.append('isPlaying',isPlaying);
            inputsPlayer.append('picture',picture,picture.name);
            console.log(inputsPlayer)

            Axios.post("http://127.0.0.1:8000/addPlayer/", inputsPlayer)
            .then((res) => navigate('/'))
            .catch(function(error){
                    if(error.response){
                        console.log(error.message);
                        console.log(error.response);
        
            }
        })
    }

  return (
        <form className='react-form' onSubmit={handleSubmit}>
            <h1>Add Players</h1>
            <fieldset className='form-group'>
                <ReactFormLabel htmlFor='formPName' title='Enter Player Name :' />
                <input id='formPName' className='form-input' name='playerName' type='text' required onChange={(e)=> setplayerName(e.target.value)} value={playerName} />
            </fieldset>

            <fieldset className='form-group'>
                <ReactFormLabel htmlFor='formPrice' title='Price :' />
                <input id='formPrice' className='form-input' name='price' type='number' required onChange={(e)=> setPrice(e.target.value)} value={price} />
            </fieldset>
            <fieldset className='form-group'>
                <ReactFormLabel htmlFor='formPic' title='Picture :' />
                <input id="formPic" type="file" name='icon' onChange={(e)=> setPicture(e.target.files[0])} required/>
            </fieldset>
            <fieldset className='form-group'>
                <ReactFormLabel htmlFor='formTaem' title='Team :' />
                <select name="team" id="formTeam"  onChange={(e)=> setTeam(e.target.value)} value={team}>
                {teamDatas.map((data) => (
                    <option key={data.teamName} value={data.teamName}>{data.teamName}</option>

                ))}
                </select>
            </fieldset>
            <fieldset className='form-group'>
                <ReactFormLabel htmlFor='formDescription' title='Description :' />
                <select name="description" id="formDescription" onChange={(e)=> setDescription(e.target.value)} value={description}>
                    <option value="batsman">Batsman</option>
                    <option value="bowler">Bowler</option>
                    <option value="Allrounder">Allrounder</option>
                </select>
            </fieldset>
            <fieldset className='form-group'>
                <input id='formPlayStatus' className='form-input' name='isPlaying' type='checkbox' onChange={(e)=> setIsPlaying(e.target.value)} value={true} />
                <ReactFormLabel htmlFor='formPlayStatus' title='IsPlaying :' />
            </fieldset>

            <div className='form-group'>
                <input id='formButton' className='btn' type='submit' placeholder='Send message' />
            </div>
        </form>
        )
}

export { PlayerForm }