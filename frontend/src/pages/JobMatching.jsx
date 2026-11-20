
import { useEffect, useState } from 'react'
import {
  BriefcaseBusiness,
  Target,
  Plus,
  Trash2,
  Search,
  RefreshCw,
  CheckCircle,
  AlertCircle,
} from 'lucide-react'
import { apiRequest } from '../services/api'

function JobMatching() {
  const [jobs, setJobs] = useState([])
  const [resumes, setResumes] = useState([])
  const [matches, setMatches] = useState([])

  const [title, setTitle] = useState('')
  const [companyName, setCompanyName] = useState('')
  const [description, setDescription] = useState('')

  const [selectedJob, setSelectedJob] = useState('')
  const [selectedResume, setSelectedResume] = useState('')

  const [latestMatch, setLatestMatch] = useState(null)
  const [loading, setLoading] = useState(true)
  const [submitting, setSubmitting] = useState(false)
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')

  useEffect(() => {
    loadData()
  }, [])

  async function loadData() {
    setLoading(true)
    setError('')

    try {
      const [jobsData, resumesData, matchesData] = await Promise.all([
        apiRequest('/api/v1/jobs/'),
        apiRequest('/api/v1/resumes/'),
        apiRequest('/api/v1/job-matches/'),
      ])

      setJobs(jobsData)
      setResumes(resumesData)
      setMatches(matchesData)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  async function handleAddJob(e) {
    e.preventDefault()
    setError('')
    setMessage('')
    setSubmitting(true)

    try {
      const newJob = await apiRequest('/api/v1/jobs/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          title,
          company_name: companyName || null,
          description,
        }),
      })

      setJobs((previous) => [newJob, ...previous])
      setTitle('')
      setCompanyName('')
      setDescription('')
      setMessage('Job description added successfully.')
    } catch (err) {
      setError(err.message)
    } finally {
      setSubmitting(false)
    }
  }

  async function handleDeleteJob(jobId) {
    const confirmed = window.confirm(
      'Are you sure you want to delete this job?'
    )

    if (!confirmed) return

    setError('')
    setMessage('')

    try {
      await apiRequest(`/api/v1/jobs/${jobId}`, {
        method: 'DELETE',
      })

      setJobs((previous) => previous.filter((job) => job.id !== jobId))
      setMatches((previous) =>
        previous.filter((match) => match.job_id !== jobId)
      )

      if (Number(selectedJob) === jobId) {
        setSelectedJob('')
      }

      setMessage('Job deleted successfully.')
    } catch (err) {
      setError(err.message)
    }
  }

  async function handleMatch(e) {
    e.preventDefault()
    setError('')
    setMessage('')
    setLatestMatch(null)

    if (!selectedResume || !selectedJob) {
      setError('Please select both a resume and a job.')
      return
    }

    setSubmitting(true)

    try {
      const result = await apiRequest('/api/v1/job-matches/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          resume_id: Number(selectedResume),
          job_id: Number(selectedJob),
        }),
      })

      setLatestMatch(result)
      setMatches((previous) => [result, ...previous])
      setMessage('Resume and job matched successfully.')
    } catch (err) {
      setError(err.message)
    } finally {
      setSubmitting(false)
    }
  }

  function getJobTitle(jobId) {
    return jobs.find((job) => job.id === jobId)?.title || `Job #${jobId}`
  }

  function getResumeName(resumeId) {
    return resumes.find((resume) => resume.id === resumeId)?.name ||
      `Resume #${resumeId}`
  }

  if (loading) {
    return (
      <div className="page-container">
        <p>Loading job matching data...</p>
      </div>
    )
  }

  return (
    <div className="page-container">
      <header className="topbar">
        <div>
          <h1>Job Matching</h1>
          <p>Discover jobs that match your skills.</p>
        </div>

        <button className="secondary-btn" onClick={loadData}>
          <RefreshCw size={16} />
          Refresh
        </button>
      </header>

      <section className="welcome">
        <h2>Find Your Best Job Matches</h2>
        <p>
          Compare your resume skills with job descriptions and discover
          opportunities that suit your profile.
        </p>
      </section>

      {error && (
        <div className="job-message error-message">
          <AlertCircle size={18} />
          {error}
        </div>
      )}

      {message && (
        <div className="job-message success-message">
          <CheckCircle size={18} />
          {message}
        </div>
      )}

      <section className="stats">
        <div className="stat-card">
          <BriefcaseBusiness size={28} />
          <h3>Available Jobs</h3>
          <p>{jobs.length}</p>
        </div>

        <div className="stat-card">
          <Target size={28} />
          <h3>Job Matches</h3>
          <p>{matches.length}</p>
        </div>
      </section>

      <section className="job-section">
        <div className="section-heading">
          <div>
            <h2>Add Job Description</h2>
            <p>Save a job opportunity to compare it with your resume.</p>
          </div>
          <Plus size={24} />
        </div>

        <form onSubmit={handleAddJob} className="job-form">
          <label>Job Title</label>
          <input
            type="text"
            placeholder="e.g. Python Developer"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            minLength={2}
            maxLength={150}
            required
          />

          <label>Company Name</label>
          <input
            type="text"
            placeholder="e.g. Google"
            value={companyName}
            onChange={(e) => setCompanyName(e.target.value)}
            maxLength={150}
          />

          <label>Job Description</label>
          <textarea
            placeholder="Paste the complete job description here (minimum 50 characters)..."
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            minLength={50}
            rows={6}
            required
          />

          <button type="submit" disabled={submitting}>
            <Plus size={17} />
            {submitting ? 'Adding...' : 'Add Job'}
          </button>
        </form>
      </section>

      <section className="job-section">
        <div className="section-heading">
          <div>
            <h2>Compare Resume with Job</h2>
            <p>Select a resume and job description to calculate compatibility.</p>
          </div>
          <Search size={24} />
        </div>

        <form onSubmit={handleMatch} className="job-form">
          <label>Select Resume</label>
          <select
            value={selectedResume}
            onChange={(e) => setSelectedResume(e.target.value)}
            required
          >
            <option value="">Choose a resume</option>
            {resumes.map((resume) => (
              <option
                key={resume.id}
                value={resume.id}
                disabled={!resume.resume_text}
              >
                {resume.name} - {resume.target_role}
                {!resume.resume_text ? ' (PDF not uploaded)' : ''}
              </option>
            ))}
          </select>

          <label>Select Job</label>
          <select
            value={selectedJob}
            onChange={(e) => setSelectedJob(e.target.value)}
            required
          >
            <option value="">Choose a job</option>
            {jobs.map((job) => (
              <option key={job.id} value={job.id}>
                {job.title} {job.company_name ? `- ${job.company_name}` : ''}
              </option>
            ))}
          </select>

          <button
            type="submit"
            disabled={submitting || !jobs.length || !resumes.length}
          >
            <Target size={17} />
            {submitting ? 'Matching...' : 'Compare Resume'}
          </button>
        </form>
      </section>

      {latestMatch && (
        <section className="job-section">
          <h2>Latest Matching Result</h2>

          <div className="match-score">
            <span>Skill Match Percentage</span>
            <h2>{latestMatch.skill_match_percentage.toFixed(2)}%</h2>
          </div>

          <p>
            <strong>Resume:</strong> {getResumeName(latestMatch.resume_id)}
          </p>
          <p>
            <strong>Job:</strong> {getJobTitle(latestMatch.job_id)}
          </p>

          <div className="skills-result">
            <div>
              <h3>Matched Skills ({latestMatch.matched_skills.length})</h3>
              {latestMatch.matched_skills.length ? (
                latestMatch.matched_skills.map((skill) => (
                  <span className="skill-tag matched" key={skill}>
                    {skill}
                  </span>
                ))
              ) : (
                <p>No matched skills found.</p>
              )}
            </div>

            <div>
              <h3>Missing Skills ({latestMatch.missing_skills.length})</h3>
              {latestMatch.missing_skills.length ? (
                latestMatch.missing_skills.map((skill) => (
                  <span className="skill-tag missing" key={skill}>
                    {skill}
                  </span>
                ))
              ) : (
                <p>No missing skills found.</p>
              )}
            </div>
          </div>
        </section>
      )}

      <section className="job-section">
        <h2>Saved Job Descriptions ({jobs.length})</h2>

        {jobs.length === 0 ? (
          <p>No jobs added yet. Add your first job description above.</p>
        ) : (
          <div className="job-list">
            {jobs.map((job) => (
              <div className="job-card" key={job.id}>
                <div>
                  <h3>{job.title}</h3>
                  <p>{job.company_name || 'Company not specified'}</p>
                  <span>
                    {job.description.length > 150
                      ? `${job.description.slice(0, 150)}...`
                      : job.description}
                  </span>
                </div>

                <button
                  className="delete-job-btn"
                  onClick={() => handleDeleteJob(job.id)}
                  aria-label={`Delete ${job.title}`}
                >
                  <Trash2 size={18} />
                </button>
              </div>
            ))}
          </div>
        )}
      </section>

      <section className="job-section">
        <h2>Matching History ({matches.length})</h2>

        {matches.length === 0 ? (
          <p>Your matching reports will appear here.</p>
        ) : (
          <div className="job-list">
            {matches.map((match) => (
              <div className="job-card" key={match.id}>
                <div>
                  <h3>{getJobTitle(match.job_id)}</h3>
                  <p>{getResumeName(match.resume_id)}</p>
                  <span>
                    {match.matched_skills.length} matched skills ·{' '}
                    {match.missing_skills.length} missing skills
                  </span>
                </div>

                <strong className="history-score">
                  {match.skill_match_percentage.toFixed(2)}%
                </strong>
              </div>
            ))}
          </div>
        )}
      </section>
    </div>
  )
}

export default JobMatching
