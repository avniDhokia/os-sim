import { useState, useEffect } from 'react'
import './App.css'
import CPU from './components/cpu'
import Scheduler from './components/scheduler'
import Terminal from './components/terminal'

function App() {

  const [cpu, setCPU] = useState({
    currentProcess: "Idle",
    events: "No Events"
  });

  const [scheduler, setScheduler] = useState({
    name: "No Scheduler Selected",
    state: "No Scheduler",
    processes: "No Processes",
    events: "No Events"
  })


  useEffect(() => {
    fetch("http://127.0.0.1:5000").then((res) => {
      res.json().then((data) => {
        console.log(data)
        setCPU({
          currentProcess: data.cpu.current_process.process,
          events: data.cpu.events
        });
        setScheduler({
          name: data.scheduler.name,
          state: data.scheduler.state,
          events: data.scheduler.events
        })
      })
    })
  })


  // data for making new processes
  const [newProcessName, setNewProcessName] = useState("User Process");

  // add a new process
  function addProcess(e){
    e.preventDefault();

    fetch("http://127.0.0.1:5000/addProcess", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name: newProcessName })
    })
    .catch(console.error);
  }

  return (
    <div id="app">


      <div>

        <div id="user-panel">

          {/* form to add new processes */}
          <form id="gui" onSubmit={addProcess} action="http://localhost:5173/" method="post">

            {/* choose name of new process */}
            <input type="text" value={newProcessName} onChange={e => setNewProcessName(e.target.value)} />

            {/* submit */}
            <button type="submit" name="addProcessButton">Add Process</button>

          </form>
          
          <Terminal />

        </div>

        <CPU currentProcess={cpu.currentProcess} events={cpu.events}/>

      </div>


      <Scheduler name={scheduler.name} currentProcess={cpu.currentProcess} state={scheduler.state} events={scheduler.events}/>
      
    </div>
  )
}

export default App
