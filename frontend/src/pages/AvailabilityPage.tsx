import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'

interface DayInfo {
  date: string
  booked: number
  capacity: number
  remaining: number
}

interface ApiResponse {
  days: DayInfo[]
  isAvailableForEntireRange: boolean
}

export default function AvailabilityPage() {
  const [start, setStart] = useState('')
  const [end, setEnd] = useState('')

  const { data, refetch } = useQuery<ApiResponse>({
    queryKey: ['availability', start, end],
    queryFn: async () => {
      const res = await fetch(`/api/availability?start=${start}&end=${end}`)
      if (!res.ok) throw new Error('failed')
      return res.json()
    },
    enabled: false
  })

  return (
    <div>
      <h2>Check Availability</h2>
      <input type="date" value={start} onChange={e => setStart(e.target.value)} />
      <input type="date" value={end} onChange={e => setEnd(e.target.value)} />
      <button onClick={() => refetch()}>Check</button>
      {data && (
        <ul>
          {data.days.map(d => (
            <li key={d.date}>{d.date}: {d.booked}/{d.capacity} remaining {d.remaining}</li>
          ))}
        </ul>
      )}
    </div>
  )
}
