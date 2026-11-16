
import { useEffect, useState } from 'react'
import { FileText, Plus, Trash2, Briefcase, Upload } from 'lucide-react'
import { apiRequest } from '../services/api'

function Resumes() {
  const [resumes, setResumes] = useState([])
  const [showForm, setShowForm] = useState(false)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [formData, setFormData] = useState({
    name: '', email: '', phone: '', target_role: '',
    skills: '', experience_years: 0,
  })

  async function loadResumes() {
    try {
      setLoading(true)
      setResumes(await apiRequest('/api/v1/resumes/'))
      setError('')
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadResumes()
  }, [])

  function handleChange(e) {
    setFormData({ ...formData, [e.target.name]: e.target.value })
  }

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')

    try {
      await apiRequest('/api/v1/resumes/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ...formData,
          skills: formData.skills.split(',').map(s => s.trim()).filter(Boolean),
          experience_years: Number(formData.experience_years),
        }),
      })

      setFormData({
        name: '', email: '', phone: '', target_role: '',
        skills: '', experience_years: 0,
      })
      setShowForm(false)
      await loadResumes()
    } catch (err) {
      setError(err.message)
    }
  }

  async function handleDelete(id) {
    if (!window.confirm('Delete this resume?')) return

    try {
      await apiRequest(`/api/v1/resumes/${id}`, { method: 'DELETE' })
      await loadResumes()
    } catch (err) {
      setError(err.message)
    }
  }

  return (
    <div className="page-container resume-page">
      <header className="topbar">
        <div>
          <h1>My Resumes</h1>
          <p>Manage your professional profile and resumes.</p>
        </div>
      </header>

      <section className="resume-hero">
        <div>
          <span className="resume-eyebrow">YOUR CAREER WORKSPACE</span>
          <h2>Build your next career move.</h2>
          <p>Organize your resumes and get ready for intelligent career analysis.</p>
          <button className="resume-primary-btn" onClick={() => setShowForm(!showForm)}>
            <Plus size={18} />
            {showForm ? 'Cancel' : 'Add New Resume'}
          </button>
        </div>
        <div className="resume-hero-icon">
          <FileText size={76} />
        </div>
      </section>

      {error && <div className="resume-error">{error}</div>}

      {showForm && (
        <section className="resume-form-card">
          <h2>Add a New Resume</h2>
          <p>Enter your professional details below.</p>

          <form onSubmit={handleSubmit} className="resume-form">
            <label>Full Name
              <input name="name" placeholder="Your full name" value={formData.name} onChange={handleChange} minLength={2} maxLength={100} required />
            </label>

            <label>Email Address
              <input name="email" type="email" placeholder="you@example.com" value={formData.email} onChange={handleChange} required />
            </label>

            <label>Phone Number
              <input name="phone" placeholder="Optional" value={formData.phone} onChange={handleChange} />
            </label>

            <label>Target Role
              <input name="target_role" placeholder="e.g. Python Developer" value={formData.target_role} onChange={handleChange} required />
            </label>

            <label className="resume-full-width">Skills
              <input name="skills" placeholder="Python, React, SQL..." value={formData.skills} onChange={handleChange} />
            </label>

            <label>Experience (Years)
              <input name="experience_years" type="number" min="0" step="0.1" value={formData.experience_years} onChange={handleChange} required />
            </label>

            <div className="resume-full-width">
              <button className="resume-primary-btn" type="submit">Save Resume</button>
            </div>
          </form>
        </section>
      )}

      <div className="resume-list-heading">
        <div>
          <h2>Your Resumes</h2>
          <p>{resumes.length} resume{resumes.length !== 1 ? 's' : ''} saved</p>
        </div>
      </div>

      {loading ? (
        <div className="resume-empty">Loading resumes...</div>
      ) : resumes.length === 0 ? (
        <div className="resume-empty">
          <FileText size={42} />
          <h3>No resumes yet</h3>
          <p>Add your first resume to get started.</p>
        </div>
      ) : (
        <div className="resume-grid">
          {resumes.map(resume => (
            <article className="resume-card" key={resume.id}>
              <div className="resume-card-top">
                <div className="resume-file-icon"><FileText size={25} /></div>
                <button className="resume-delete-btn" onClick={() => handleDelete(resume.id)} title="Delete resume">
                  <Trash2 size={18} />
                </button>
              </div>
              <h3>{resume.name}</h3>
              <p className="resume-email">{resume.email}</p>
              <div className="resume-role">
                <Briefcase size={16} />
                {resume.target_role}
              </div>
              <p className="resume-experience">Experience: {resume.experience_years} years</p>
              <div className="resume-skills">
                {resume.skills.map((skill, index) => (
                  <span key={index}>{skill}</span>
                ))}
              </div>
            </article>
          ))}
        </div>
      )}
    </div>
  )
}

export default Resumes
