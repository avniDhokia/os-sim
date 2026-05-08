import { useState, useEffect } from 'react'
import './App.css'
import CPU from './components/cpu'
import Scheduler from './components/scheduler'

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

  return (
    <>
      <p>hiya :3</p>
      <Scheduler name={scheduler.name} currentProcess={cpu.currentProcess} state={scheduler.state}/>
      <CPU currentProcess={cpu.currentProcess} />
    </>
  )
}

export default App
