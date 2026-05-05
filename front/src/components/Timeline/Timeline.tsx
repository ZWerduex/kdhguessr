import { useRef, useState } from "react"
import { formatTimeFull } from "../../utils/formatTime"
import "./Timeline.css"

type Props = {
  duration: number
  selected: number | null
  onSelect: (value: number) => void
}

function Timeline({ duration, selected, onSelect }: Props) {
  const timelineRef = useRef<HTMLDivElement>(null)
  const isDragging = useRef(false)

  const durationMinutes = duration / 60

  const updateFromClientX = (clientX: number) => {
    if (!timelineRef.current) return

    const rect = timelineRef.current.getBoundingClientRect()
    const x = clientX - rect.left

    const percent = Math.max(0, Math.min(1, x / rect.width))
    const seconds = Math.round(percent * duration)

    onSelect(seconds)
  }

  const handleMouseDown = (e: React.MouseEvent) => {
    isDragging.current = true
    updateFromClientX(e.clientX)
  }

  const handleMouseMove = (e: MouseEvent) => {
    if (!isDragging.current) return
    updateFromClientX(e.clientX)
  }

  const handleMouseUp = () => {
    isDragging.current = false
  }

  // attach global listeners
  useState(() => {
    window.addEventListener("mousemove", handleMouseMove)
    window.addEventListener("mouseup", handleMouseUp)

    return () => {
      window.removeEventListener("mousemove", handleMouseMove)
      window.removeEventListener("mouseup", handleMouseUp)
    }
  })

  const ticks = []

  for (let min = 0; min <= durationMinutes; min += 10) {
    const left = (min / durationMinutes) * 100

    let className = "tick small"
    if (min % 60 === 0) className = "tick large"
    else if (min % 30 === 0) className = "tick medium"

    // Add tick for this minute
    ticks.push(
      <div
        key={min}
        className={className}
        style={{
          left: `${left}%`,
          "--x": `${left}%`,
        } as React.CSSProperties}
      >
        {min % 60 === 0 && (
          <>
            <div className="tick-top" />
            <span className="label">
              {Math.floor(min / 60)}:00:00
            </span>
            <div className="tick-bottom" />
          </>
        )}
      </div>
    )
  }
  const lastLeft = 100

  // Add final tick at the end
  ticks.push(
    <div
      key="end"
      className="tick large"
      style={{
          left: `${lastLeft}%`,
          "--x": `${lastLeft}%`,
        } as React.CSSProperties}
    >
      <>
        <div className="tick-top" />
        <span className="label">
          {formatTimeFull(duration)}
        </span>
        <div className="tick-bottom" />
      </>
    </div>
  )

  return (
    <div className="timeline-wrapper">
      <div className="timeline-container">
        <div
          className="timeline"
          ref={timelineRef}
          onMouseDown={handleMouseDown}
          
        >
          {ticks}

          {selected !== null && (
            <div
              className="marker"
              style={{
                left: `${(selected / duration) * 100}%`,
              }}
            />
          )}
        </div>
      </div>
    </div>
  )
}

export default Timeline