import React, { useState } from 'react'
import api from '../api'

export default function RiotLookup() {
  const [game, setGame] = useState('lol')
  const [region, setRegion] = useState('na1')
  const [query, setQuery] = useState('')
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  const handleLookup = async (e) => {
    e.preventDefault()
    setResult(null)
    setError(null)
    try {
      let res
      if (game === 'lol') {
        res = await api.get(`/riot/lol/${region}/summoner/by-name/${encodeURIComponent(query)}/`)
      } else if (game === 'tft') {
        res = await api.get(`/riot/tft/${region}/summoner/by-name/${encodeURIComponent(query)}/`)
      } else if (game === 'valorant') {
        // for valorant expect PUUID for more reliable lookup
        res = await api.get(`/riot/valorant/${region}/account/by-puuid/${encodeURIComponent(query)}/`)
      }
      setResult(res.data)
    } catch (err) {
      setError(err.response?.data || err.toString())
    }
  }

  return (
    <div className="container">
      <h1 className="text-2xl font-bold mb-4">Riot Lookup</h1>
      <form onSubmit={handleLookup} className="grid gap-2 max-w-md">
        <label className="flex flex-col">
          Game
          <select value={game} onChange={(e) => setGame(e.target.value)} className="p-2 border rounded">
            <option value="lol">League of Legends</option>
            <option value="tft">TFT</option>
            <option value="valorant">Valorant</option>
          </select>
        </label>
        <label className="flex flex-col">
          Region (e.g. na1, euw1, kr)
          <input value={region} onChange={(e) => setRegion(e.target.value)} className="p-2 border rounded" />
        </label>
        <label className="flex flex-col">
          Summoner name or PUUID
          <input value={query} onChange={(e) => setQuery(e.target.value)} className="p-2 border rounded" />
        </label>
        <button className="bg-blue-600 text-white p-2 rounded" type="submit">Lookup</button>
      </form>

      {error && <pre className="mt-4 text-red-600">{JSON.stringify(error, null, 2)}</pre>}
      {result && <pre className="mt-4 bg-slate-100 p-3 rounded">{JSON.stringify(result, null, 2)}</pre>}
    </div>
  )
}
