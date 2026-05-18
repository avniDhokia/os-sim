import { useState, useEffect } from 'react'
import './App.css'
import CPU from './components/cpu'
import Scheduler from './components/scheduler'
import Terminal from './components/terminal'

function App() {

  const [cpu, setCPU] = useState({
    currentProcess: "Idle"
  });

  const [scheduler, setScheduler] = useState({
    name: "No Scheduler Selected",
    state: "No Scheduler",
    processes: "No Processes"
  })


  useEffect(() => {
    fetch("http://127.0.0.1:5000").then((res) => {
      res.json().then((data) => {
        console.log(data)
        setCPU({
          currentProcess: data.cpu.current_process.process
        });
        setScheduler({
          name: data.scheduler.name,
          state: data.scheduler.state
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
    <>

      {/* form to add new processes */}
      <form onSubmit={addProcess} action="http://localhost:5173/" method="post">

        {/* choose name of new process */}
        <input type="text" value={newProcessName} onChange={e => setNewProcessName(e.target.value)} />

        {/* submit */}
        <button type="submit" name="addProcessButton">Add Process</button>

      </form>
      
      <Terminal />
      <Scheduler name={scheduler.name} currentProcess={cpu.currentProcess} state={scheduler.state}/>
      <CPU currentProcess={cpu.currentProcess} />
    </>
  )
}

export default App
