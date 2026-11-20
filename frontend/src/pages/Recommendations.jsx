
import { useEffect, useState } from 'react'
import {
  Lightbulb,
  BookOpen,
  TrendingUp,
  LoaderCircle,
  Clock,
  Target,
  Code,
  CheckCircle
} from 'lucide-react'
import { apiRequest } from '../services/api'

function decodeText(value) {
  if (typeof value !== 'string') return value || ''

  const textarea = document.createElement('textarea')
  textarea.innerHTML = value
  return textarea.value
}

function Recommendations() {
  const [recommendations, setRecommendations] = useState([])
  const [missingSkills, setMissingSkills] = useState([])
  const [targetRole, setTargetRole] = useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    async function loadRecommendations() {
      try {
        setLoading(true)
        setError('')

        const resumesData = await apiRequest('/api/v1/resumes/')

        const resumes = Array.isArray(resumesData)
          ? resumesData
          : resumesData?.resumes || []

        if (resumes.length === 0) {
          setRecommendations([])
          setMissingSkills([])
          setTargetRole('')
          return
        }

        const results = await Promise.all(
          resumes.map(async (resume) => {
            try {
              const analysisData = await apiRequest(
                `/api/v1/resumes/${resume.id}/analyses`
              )

              const analyses = Array.isArray(analysisData)
                ? analysisData
                : analysisData?.analyses || []

              if (analyses.length === 0) return null

              const latestAnalysis = [...analyses].sort(
                (a, b) =>
                  new Date(b.created_at || 0) -
                  new Date(a.created_at || 0)
              )[0]

              const data = await apiRequest(
                `/api/v1/resumes/${resume.id}/analyses/${latestAnalysis.id}/recommendations`
              )

              return {
                data,
                targetRole: latestAnalysis.target_role,
                createdAt: latestAnalysis.created_at
              }
            } catch {
              return null
            }
          })
        )

        const validResults = results
          .filter(Boolean)
          .sort(
            (a, b) =>
              new Date(b.createdAt || 0) -
              new Date(a.createdAt || 0)
          )

        if (validResults.length > 0) {
          const latest = validResults[0]

          setRecommendations(
            latest.data.recommendations || []
          )

          setMissingSkills(
            latest.data.missing_skills || []
          )

          setTargetRole(
            latest.data.target_role || latest.targetRole || ''
          )
        } else {
          setRecommendations([])
          setMissingSkills([])
          setTargetRole('')
        }
      } catch (err) {
        setError(err.message || 'Failed to load recommendations.')
      } finally {
        setLoading(false)
      }
    }

    loadRecommendations()
  }, [])

  const learningActions = recommendations.filter(
    (item) => item.suggestion || item.project
  ).length

  const highPriorityCount = recommendations.filter(
    (item) => item.priority === 'High'
  ).length

  return (
    <div className="page-container">

      <header className="topbar">
        <div>
          <h1>Skill Recommendations</h1>
          <p>Discover which skills you should learn next.</p>
        </div>
      </header>

      <section className="welcome">
        <h2>Your Personalized Learning Path</h2>
        <p>
          Identify skill gaps, understand learning priorities,
          and follow practical steps to improve your career profile.
        </p>

        {targetRole && (
          <span>Target Role: {decodeText(targetRole)}</span>
        )}
      </section>

      {loading ? (
        <div className="dashboard-loading">
          <LoaderCircle size={22} className="loading-icon" />
          <p>Loading recommendations...</p>
        </div>
      ) : (
        <>
          {error && (
            <p className="error-message">{error}</p>
          )}

          <section className="stats">

            <div className="stat-card">
              <Lightbulb size={28} />
              <h3>Suggested Skills</h3>
              <p>{missingSkills.length}</p>
            </div>

            <div className="stat-card">
              <BookOpen size={28} />
              <h3>Learning Actions</h3>
              <p>{learningActions}</p>
            </div>

            <div className="stat-card">
              <TrendingUp size={28} />
              <h3>High Priority Skills</h3>
              <p>{highPriorityCount}</p>
            </div>

          </section>

          <section className="activity">
            <h2>Your Learning Recommendations</h2>

            {recommendations.length > 0 ? (
              recommendations.map((item, index) => (
                <div
                  className="recommendation-card"
                  key={`${item.skill}-${index}`}
                >

                  <h3>{decodeText(item.skill)}</h3>

                  <p>
                    <strong>Priority:</strong>{' '}
                    {item.priority || 'Not specified'}
                  </p>

                  <p>
                    <Clock size={15} />
                    {' '}
                    <strong>Estimated Duration:</strong>{' '}
                    {item.duration || 'Not specified'}
                  </p>

                  <div>
                    <p><strong>Why this skill matters</strong></p>
                    <p>{decodeText(item.reason)}</p>
                  </div>

                  <div>
                    <p><strong>Learning Topics</strong></p>

                    {Array.isArray(item.topics) &&
                    item.topics.length > 0 ? (
                      <ul>
                        {item.topics.map((topic, topicIndex) => (
                          <li key={topicIndex}>
                            <CheckCircle size={15} />
                            {' '}
                            {decodeText(topic)}
                          </li>
                        ))}
                      </ul>
                    ) : (
                      <p>No topics available.</p>
                    )}
                  </div>

                  <div>
                    <p><strong>Recommended Learning Action</strong></p>
                    <p>{decodeText(item.suggestion)}</p>
                  </div>

                  <div>
                    <p>
                      <Code size={16} />
                      {' '}
                      <strong>Practical Project</strong>
                    </p>
                    <p>{decodeText(item.project)}</p>
                  </div>

                </div>
              ))
            ) : (
              <>
                <p>No recommendations available yet.</p>
                <span>
                  Complete a resume analysis to get skill recommendations.
                </span>
              </>
            )}

          </section>
        </>
      )}
    </div>
  )
}

export default Recommendations
