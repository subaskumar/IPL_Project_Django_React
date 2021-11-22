import './App.css';
// import { Welcome } from './components/Greet';
// import { Form } from './components/Form';
import { Home } from './pages/Home'
import React from "react";
import { Layout } from './Layout/Layout';
import { BrowserRouter as Router, Routes, Route} from "react-router-dom";
import './sass/main.css';
import { TeamForm } from './components/TeamForm';
import { PlayerForm } from './components/PlayerForm';
import { TeamDetails } from './pages/TeamDetails';



function App() {
  
  return (
    <div className="App">
        <Router>
          <Layout>
            <Routes>
            <Route exact path="/" element={<Home/>}/>
            <Route exact path="/addTeam" element={<TeamForm/>}/>
            <Route exact path="/addPlayer" element={<PlayerForm/>}/>
            <Route exact path="/teamDetails/:id" element={<TeamDetails name="subas"/>}/>

            </Routes>

          </Layout> 
        </Router>
    </div>
  );
}

export default App;
