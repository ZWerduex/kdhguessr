import { useState } from "react"
import Timeline from "./components/Timeline/Timeline"
import FrameImage from "./components/FrameImage/FrameImage"
import TimeInput from "./components/TimeInput/TimeInput"

import BackgroundShader from "./components/BackgroundShader/BackgroundShader"

import { formatTime, formatTimeFull } from "./utils/formatTime"

import './App.css'

function App() {
  const [selected, setSelected] = useState<number | null>(null)


  const validate = () => {
    if (selected !== null) {
      alert(`Tu as choisi ${formatTimeFull(selected)}`)
    }
  }

  return (
    <>
      <BackgroundShader />
      <div className="container">
        <FrameImage />
        <Timeline
          duration={4783}
          selected={selected}
          onSelect={setSelected}
        />
        <TimeInput
          selected={selected}
          onSubmit={validate}
        />

      </div>
    </>
  )
}

export default App
