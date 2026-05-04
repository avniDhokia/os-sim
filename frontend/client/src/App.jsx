import { useState, useEffect } from 'react'
import './App.css'
import CPU from './components/cpu'
import Scheduler from './components/scheduler'

function App() {

  const [cpu, setCPU] = useState({
    currentProcess: "Idle"
  });

  useEffect(() => {
    fetch("http://127.0.0.1:5000").then((res) => {
      res.json().then((data) => {
        setCPU({
          currentProcess: data.cpu.current_process
        });
      })
    })
  })

  return (
    <>
      <p>hiya :3</p>
      <Scheduler />
      <CPU currentProcess={cpu.currentProcess} />
    </>
  )
}

export default App
