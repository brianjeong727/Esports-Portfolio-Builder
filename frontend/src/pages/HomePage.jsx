import React from 'react'
import { Link } from 'react-router-dom'
import ProfileForm from '../components/ProfileForm'

export default function HomePage() {
  return (
    <div className="container">
      <h1 className="text-3xl font-bold mb-4">Esports Portfolio Builder</h1>
      <p className="mb-6 text-slate-700">Enter your gaming profile and preferences to generate an esports portfolio.</p>
      <ProfileForm />
      <div className="mt-6">
        <Link className="text-blue-600" to="/portfolio">View portfolio previews</Link>
      </div>
    </div>
  )
}
