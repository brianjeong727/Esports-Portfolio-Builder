import React, { useEffect, useState } from 'react'
import api from '../api'

export default function PortfolioPage() {
  const [profiles, setProfiles] = useState([])

  useEffect(() => {
    api.get('/profiles/').then(r => setProfiles(r.data)).catch(() => setProfiles([]))
  }, [])

  return (
    <div className="container">
      <h1 className="text-2xl font-bold mb-4">Portfolio Previews</h1>
      {profiles.length === 0 && <p className="text-slate-600">No profiles yet. Create one on the home page.</p>}
      <div className="grid gap-4">
        {profiles.map(p => (
          <div key={p.id} className="p-4 bg-white rounded shadow">
            <h2 className="text-xl font-semibold">{p.display_name}</h2>
            <p className="text-sm text-slate-500">{p.game} • {p.rank}</p>
            <p className="mt-2 text-slate-700">{p.bio}</p>
          </div>
        ))}
      </div>
    </div>
  )
}
