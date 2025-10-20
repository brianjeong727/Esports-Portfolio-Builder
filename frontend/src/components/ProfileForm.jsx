import React, { useState } from 'react'
import api from '../api'

export default function ProfileForm() {
  const [form, setForm] = useState({
    display_name: '',
    game: '',
    rank: '',
    hours_played: '',
    country: '',
    bio: '',
  })
  const [status, setStatus] = useState(null)

  const handleChange = (e) => {
    const { name, value } = e.target
    setForm(prev => ({ ...prev, [name]: value }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      const payload = { ...form, hours_played: form.hours_played ? Number(form.hours_played) : null }
      const res = await api.post(`/profiles/`, payload)
      setStatus({ ok: true, message: 'Profile created', data: res.data })
      setForm({ display_name: '', game: '', rank: '', hours_played: '', country: '', bio: '' })
    } catch (err) {
      setStatus({ ok: false, message: err.toString() })
    }
  }

  return (
    <div>
      <form onSubmit={handleSubmit} className="grid gap-3">
        <input name="display_name" value={form.display_name} onChange={handleChange} placeholder="Display name" required className="p-2 border rounded" />
        <input name="game" value={form.game} onChange={handleChange} placeholder="Game (e.g. League of Legends)" className="p-2 border rounded" />
        <input name="rank" value={form.rank} onChange={handleChange} placeholder="Rank (e.g. Diamond)" className="p-2 border rounded" />
        <input name="hours_played" type="number" value={form.hours_played} onChange={handleChange} placeholder="Hours played" className="p-2 border rounded" />
        <input name="country" value={form.country} onChange={handleChange} placeholder="Country" className="p-2 border rounded" />
        <textarea name="bio" value={form.bio} onChange={handleChange} placeholder="Short bio" className="p-2 border rounded" />
        <button type="submit" className="bg-blue-600 text-white py-2 px-4 rounded">Create Profile</button>
      </form>

      {status && (
        <div className={`mt-3 ${status.ok ? 'text-green-600' : 'text-red-600'}`}>
          {status.message}
          {status.data && <pre className="mt-2 p-2 bg-slate-100 rounded">{JSON.stringify(status.data, null, 2)}</pre>}
        </div>
      )}
    </div>
  )
}
