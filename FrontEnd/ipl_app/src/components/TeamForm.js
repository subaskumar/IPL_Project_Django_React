import {useState} from "react"
import Axios from 'axios'
import {useNavigate} from 'react-router-dom';
function  ReactFormLabel(props) {
     return(
      <label htmlFor={props.htmlFor}>{props.title}</label>
     )
}
function TeamForm() {
    const navigate = useNavigate();
    const [teamName, setTeamName] = useState("")
    const [champ_win, setChamp_win] = useState("")
    const [icon, setIcon] = useState()


    const handleSubmit = (e) => {
            e.preventDefault();
            const inputs = new FormData()
            inputs.append('teamName',teamName);
            inputs.append('champ_win',champ_win);
            inputs.append('icon',icon,icon.name);
            console.log(inputs)

            Axios.post("http://127.0.0.1:8000/Ipl_Team/", inputs)
            .then((res) => navigate('/'))
            .catch(function(error){
                    if(error.response){
                        console.log(error.message);
                        console.log(error.response);
                        console.log(error.response);
                        // console.log(error.response.status);
                        // setError(error.response.teamName)
                        // console.log(Errors.icon)
                    }
            })
    }

  return (
        <form className='react-form' onSubmit={handleSubmit}>
            <h1>Add New Team</h1>
            <fieldset className='form-group'>
                <ReactFormLabel htmlFor='formTeamName' title='New Team Name :' />
                <input id='formTeamName' className='form-input' name='teamName' type='text' required onChange={(e)=> setTeamName(e.target.value)} value={teamName} />
            </fieldset>
            <fieldset className='form-group'>
                <ReactFormLabel htmlFor='formChampWin' title='Championship Won :' />
                <input id='formChampWin' className='form-input' name='champ_win' type='number' required onChange={(e)=> setChamp_win(e.target.value)} value={champ_win} />
            </fieldset>

            <fieldset className='form-group'>
                <ReactFormLabel  htmlFor='formIcon' title='Team Icon :' />
                <input id='formIcon' type="file" name='icon' onChange={(e)=> setIcon(e.target.files[0])} />
            </fieldset>

            <div className='form-group'>
                <input id='formButton' className='btn' type='submit' placeholder='Send message' />
            </div>
        </form>
        )
}

export { TeamForm }