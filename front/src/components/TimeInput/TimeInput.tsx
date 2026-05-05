import { useEffect, useState } from "react"
import "./TimeInput.css"

type Props = {
  selected: number | null
  onSubmit: (value: number) => void
}

// 🔧 convert sec → hh:mm:ss
function formatTime(sec: number) {
  const h = Math.floor(sec / 3600)
  const m = Math.floor((sec % 3600) / 60)
  const s = sec % 60

  return [h, m, s]
    .map((v) => String(v).padStart(2, "0"))
    .join(":")
}

// 🔧 convert hh:mm:ss → sec
function parseTime(str: string) {
  const parts = str.split(":").map(Number)

  if (parts.some(isNaN)) return null

  let h = 0, m = 0, s = 0

  if (parts.length === 3) {
    ;[h, m, s] = parts
  } else if (parts.length === 2) {
    ;[m, s] = parts
  } else if (parts.length === 1) {
    s = parts[0]
  }

  return h * 3600 + m * 60 + s
}

export default function TimeInput({ selected, onSubmit }: Props) {
  const [input, setInput] = useState("")

  // sync avec la timeline
  useEffect(() => {
    if (selected !== null) {
      setInput(formatTime(selected))
    }
  }, [selected])

  const handleSubmit = () => {
    const seconds = parseTime(input)
    if (seconds !== null) {
      onSubmit(seconds)
    }
  }

  return (
    <div className="time-input-container">
      <input
        className="time-input"
        value={input}
        placeholder="00:00:00"
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === "Enter") handleSubmit()
        }}
      />

      <div className="separator" />

      <button className="validate-btn" onClick={handleSubmit}>
        Valider
      </button>
    </div>
  )
}