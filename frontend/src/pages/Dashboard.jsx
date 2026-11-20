
import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import {
  FileText,
  Brain,
  BriefcaseBusiness,
  Upload,
  LoaderCircle
} from 'lucide-react'
import { apiRequest } from '../services/api'

function Dashboard() {
  const navigate = useNavigate()

  const [stats, setStats] = useState({
    resumes: 0,
    analyses: 0,
    jobMatches: 0
  })

  const [recentActivity, setRecentActivity] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    async function loadDashboard() {
      try {
        setLoading(true)
        setError('')

        const [resumesData, matchesData] = await Promise.all([
          apiRequest('/api/v1/resumes/'),
          apiRequest('/api/v1/job-matches/')
        ])

        const resumes = Array.isArray(resumesData)
          ? resumesData
          : resumesData?.resumes || []

        const matches = Array.isArray(matchesData)
          ? matchesData
          : matchesData?.job_matches || matchesData?.matches || []

        const analysisResults = await Promise.all(
          resumes.map(async (resume) => {
            try {
              const data = await apiRequest(
                `/api/v1/resumes/${resume.id}/analyses`
              )

              return Array.isArray(data)
                ? data
                : data?.analyses || []
            } catch {
              return []
            }
          })
        )

        const analyses = analysisResults.flat()

        setStats({
          resumes: resumes.length,
          analyses: analyses.length,
          jobMatches: matches.length
        })

        const activities = [
          ...resumes.map((resume) => ({
            id: `resume-${resume.id}`,
            title: `Resume added: ${resume.name}`,
            date: resume.created_at,
            type: 'resume'
          })),
          ...analyses.map((analysis) => ({
            id: `analysis-${analysis.id}`,
            title: `Resume analyzed for ${analysis.target_role}`,
            date: analysis.created_at,
            type: 'analysis'
          })),
          ...matches.map((match) => ({
            id: `match-${match.id}`,
            title: 'Job match completed',
            date: match.created_at,
            type: 'match'
          }))
        ]

        activities.sort((a, b) => {
          return new Date(b.date || 0) - new Date(a.date || 0)
        })

        setRecentActivity(activities.slice(0, 5))
      } catch (err) {
        setError(err.message || 'Failed to load dashboard data.')
      } finally {
        setLoading(false)
      }
    }

    loadDashboard()
  }, [])

  return (
    <>
      <header className="topbar">
        <div>
          <h1>Dashboard</h1>
          <p>Welcome back!</p>
        </div>
      </header>

      <section className="welcome">
        <h2>Your career journey starts here.</h2>
        <p>
          Analyze your resume, discover skill gaps and find better job matches.
        </p>

        <button
          className="upload-button"
          onClick={() => navigate('/resumes')}
        >
          <Upload size={18} />
          Upload Resume
        </button>
      </section>

      {loading ? (
        <div className="dashboard-loading">
          <LoaderCircle size={22} className="loading-icon" />
          <p>Loading dashboard...</p>
        </div>
      ) : (
        <>
          {error && (
            <p className="error-message">{error}</p>
          )}

          <section className="stats">
            <div className="stat-card">
              <FileText size={24} />
              <h3>My Resumes</h3>
              <p>{stats.resumes}</p>
            </div>

            <div className="stat-card">
              <Brain size={24} />
              <h3>Resume Analyses</h3>
              <p>{stats.analyses}</p>
            </div>

            <div className="stat-card">
              <BriefcaseBusiness size={24} />
              <h3>Job Matches</h3>
              <p>{stats.jobMatches}</p>
            </div>
          </section>

          <section className="activity">
            <h2>Recent Activity</h2>

            {recentActivity.length > 0 ? (
              recentActivity.map((activity) => (
                <div className="activity-item" key={activity.id}>
                  <p>{activity.title}</p>
                  <span>
                    {activity.date
                      ? new Date(activity.date).toLocaleString()
                      : 'Date unavailable'}
                  </span>
                </div>
              ))
            ) : (
              <>
                <p>No recent activity yet.</p>
                <span>Upload your first resume to get started.</span>
              </>
            )}
          </section>
        </>
      )}
    </>
  )
}

export default Dashboard
