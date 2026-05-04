import { useState, useEffect } from 'react'
import './App.css'
import CPU from './components/cpu'
import Scheduler from './components/scheduler'

function App() {

  const [data, setData] = useState({
    n: "empty"
  });

  const [two, detTwo] = useState({
    num: "2"
  })

  useEffect(() => {
    fetch("http://127.0.0.1:5000").then((res) => {
      console.log(res)
      res.json().then((data) => {
        console.log(res)
        setData({
          n: data.Name
        });
      })
    })
  })

  return (
    <>
      <p>hiya :3</p>
      <Scheduler />
      <CPU />

      <p>{data.n}</p>
      <p>{two.num}</p>
    </>
  )
}

export default App
