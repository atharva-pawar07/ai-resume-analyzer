
import { useEffect, useState } from 'react'
import { FileText, Plus, Trash2, Briefcase, Upload } from 'lucide-react'
import { apiRequest } from '../services/api'

function Resumes() {
  const [resumes, setResumes] = useState([])
  const [showForm, setShowForm] = useState(false)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [uploadingId, setUploadingId] = useState(null)

  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    target_role: '',
    skills: '',
    experience_years: 0,
  })

  async function loadResumes() {
    try {
      setError('')
      const data = await apiRequest('/api/v1/resumes/')
      setResumes(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadResumes()
  }, [])

  function handleChange(event) {
    const { name, value } = event.target

    setFormData((previous) => ({
      ...previous,
      [name]: value,
    }))
  }

  async function handleSubmit(event) {
    event.preventDefault()

    try {
      setError('')
      setSuccess('')

      const resumeData = {
        ...formData,
        skills: formData.skills
          .split(',')
          .map((skill) => skill.trim())
          .filter(Boolean),
        experience_years: Number(formData.experience_years),
      }

      await apiRequest('/api/v1/resumes/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(resumeData),
      })

      setFormData({
        name: '',
        email: '',
        phone: '',
        target_role: '',
        skills: '',
        experience_years: 0,
      })

      setShowForm(false)
      setSuccess('Resume added successfully!')
      await loadResumes()
    } catch (err) {
      setError(err.message)
    }
  }

  async function handleDelete(id) {
    const confirmed = window.confirm(
      'Are you sure you want to delete this resume?'
    )

    if (!confirmed) return

    try {
      setError('')
      setSuccess('')

      await apiRequest(`/api/v1/resumes/${id}`, {
        method: 'DELETE',
      })

      setSuccess('Resume deleted successfully!')
      await loadResumes()
    } catch (err) {
      setError(err.message)
    }
  }

  async function handlePdfUpload(resumeId, file) {
    if (!file) return

    if (file.type !== 'application/pdf') {
      setError('Only PDF files are allowed.')
      return
    }

    if (file.size > 5 * 1024 * 1024) {
      setError('PDF must be smaller than 5 MB.')
      return
    }

    const formData = new FormData()
    formData.append('file', file)

    try {
      setError('')
      setSuccess('')
      setUploadingId(resumeId)

      await apiRequest(`/api/v1/resumes/${resumeId}/upload-pdf`, {
        method: 'POST',
        body: formData,
      })

      setSuccess('Resume PDF uploaded successfully!')
      await loadResumes()
    } catch (err) {
      setError(err.message)
    } finally {
      setUploadingId(null)
    }
  }

  return (
    <div className="page-container">
      <div className="resume-hero">
        <div>
          <p className="resume-eyebrow">YOUR CAREER DOCUMENTS</p>
          <h2>My Resumes</h2>
          <p>
            Manage your resumes and upload PDF files to start your career
            analysis.
          </p>
        </div>

        <button
          className="resume-primary-btn"
          onClick={() => {
            setShowForm(!showForm)
            setError('')
            setSuccess('')
          }}
        >
          <Plus size={18} />
          {showForm ? 'Close Form' : 'Add New Resume'}
        </button>
      </div>

      {error && <div className="resume-error">{error}</div>}
      {success && <div className="resume-success">{success}</div>}

      {showForm && (
        <div className="resume-form-card">
          <h2>Add New Resume</h2>

          <form onSubmit={handleSubmit} className="resume-form">
            <div>
              <label>Full Name</label>
              <input
                type="text"
                name="name"
                value={formData.name}
                onChange={handleChange}
                placeholder="Enter your full name"
                minLength={2}
                maxLength={100}
                required
              />
            </div>

            <div>
              <label>Email Address</label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                placeholder="Enter your email"
                required
              />
            </div>

            <div>
              <label>Phone Number</label>
              <input
                type="text"
                name="phone"
                value={formData.phone}
                onChange={handleChange}
                placeholder="Enter your phone number"
              />
            </div>

            <div>
              <label>Target Job Role</label>
              <input
                type="text"
                name="target_role"
                value={formData.target_role}
                onChange={handleChange}
                placeholder="e.g. Python Developer"
                required
              />
            </div>

            <div>
              <label>Skills</label>
              <input
                type="text"
                name="skills"
                value={formData.skills}
                onChange={handleChange}
                placeholder="Python, React, SQL"
              />
            </div>

            <div>
              <label>Experience (Years)</label>
              <input
                type="number"
                name="experience_years"
                value={formData.experience_years}
                onChange={handleChange}
                min="0"
                step="0.5"
              />
            </div>

            <button type="submit" className="resume-primary-btn">
              Save Resume
            </button>
          </form>
        </div>
      )}

      <div className="resume-list-heading">
        <div>
          <h2>Your Saved Resumes</h2>
          <p>{resumes.length} resume(s) saved</p>
        </div>
      </div>

      {loading ? (
        <p>Loading resumes...</p>
      ) : resumes.length === 0 ? (
        <div className="resume-empty">
          <FileText size={42} />
          <h3>No resumes yet</h3>
          <p>Add your first resume to get started.</p>
        </div>
      ) : (
        <div className="resume-grid">
          {resumes.map((resume) => (
            <div className="resume-card" key={resume.id}>
              <div className="resume-card-header">
                <div className="resume-icon">
                  <FileText size={22} />
                </div>

                <button
                  className="resume-delete-btn"
                  onClick={() => handleDelete(resume.id)}
                  title="Delete resume"
                >
                  <Trash2 size={18} />
                </button>
              </div>

              <h3>{resume.name}</h3>
              <p className="resume-email">{resume.email}</p>

              <div className="resume-role">
                <Briefcase size={16} />
                <span>{resume.target_role}</span>
              </div>

              <p className="resume-experience">
                Experience: {resume.experience_years} year(s)
              </p>

              <div className="resume-skills">
                {resume.skills?.length > 0 ? (
                  resume.skills.map((skill, index) => (
                    <span key={`${skill}-${index}`}>{skill}</span>
                  ))
                ) : (
                  <span>No skills added</span>
                )}
              </div>

              <div className="resume-upload-section">
                <p className="resume-upload-status">
                  {resume.resume_text
                    ? 'PDF uploaded'
                    : 'No PDF uploaded'}
                </p>

                <label className="resume-upload-btn">
                  <Upload size={16} />
                  {uploadingId === resume.id
                    ? 'Uploading...'
                    : 'Upload PDF'}

                  <input
                    type="file"
                    accept=".pdf,application/pdf"
                    hidden
                    disabled={uploadingId !== null}
                    onChange={(event) => {
                      const file = event.target.files?.[0]
                      handlePdfUpload(resume.id, file)
                      event.target.value = ''
                    }}
                  />
                </label>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default Resumes
