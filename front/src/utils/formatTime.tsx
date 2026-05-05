


export function formatTime(minutes: number): string {
    const hours = Math.floor(minutes / 60)
    const mins = minutes % 60

    if (hours === 0) return `${mins} min`

    return `${hours}h${mins.toString().padStart(2, "0")}`
  }

export function formatTimeFull(seconds: number): string {
  const hrs = Math.floor(seconds / 3600)
  const mins = Math.floor((seconds % 3600) / 60)
  const secs = seconds % 60

  return `${hrs}:${mins.toString().padStart(2, "0")}:${secs
    .toString()
    .padStart(2, "0")}`
}