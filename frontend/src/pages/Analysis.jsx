
import { useEffect, useState } from 'react'
import {
  Brain,
  FileSearch,
  Target,
  CheckCircle,
  XCircle,
  Lightbulb,
  Code,
  Sparkles,
  RefreshCw
} from 'lucide-react'
import { apiRequest } from '../services/api'

function Analysis() {
  const [reports, setReports] = useState([])
  const [recommendations, setRecommendations] = useState({})
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const [aiAnalysis, setAiAnalysis] = useState({})
  const [aiLoading, setAiLoading] = useState(false)
  const [aiError, setAiError] = useState('')

  useEffect(() => {
    async function loadAnalysisReports() {
      try {
        setError('')

        const resumesData = await apiRequest('/api/v1/resumes/')

        const resumes = Array.isArray(resumesData)
          ? resumesData
          : resumesData?.resumes || []

        const reportGroups = await Promise.all(
          resumes.map(async (resume) => {
            const analysesData = await apiRequest(
              `/api/v1/resumes/${resume.id}/analyses`
            )

            const analyses = Array.isArray(analysesData)
              ? analysesData
              : analysesData?.analyses || []

            return analyses.map((analysis) => ({
              ...analysis,
              resume_name: resume.name,
              resume_id: resume.id,
            }))
          })
        )

        const allReports = reportGroups
          .flat()
          .sort(
            (a, b) =>
              new Date(b.created_at) - new Date(a.created_at)
          )

        setReports(allReports)

        const recommendationResults = await Promise.all(
          allReports.map(async (report) => {
            try {
              const data = await apiRequest(
                `/api/v1/resumes/${report.resume_id}/analyses/${report.id}/recommendations`
              )

              return [report.id, data.recommendations || []]
            } catch {
              return [report.id, []]
            }
          })
        )

        setRecommendations(Object.fromEntries(recommendationResults))
      } catch (err) {
        setError(err.message || 'Failed to load analysis reports.')
      } finally {
        setLoading(false)
      }
    }

    loadAnalysisReports()
  }, [])

  async function generateAIAnalysis(resumeId) {
    setAiLoading(true)
    setAiError('')

    try {
      const data = await apiRequest(
        `/api/v1/resumes/${resumeId}/ai-analysis`,
        { method: 'POST' }
      )

      setAiAnalysis((prev) => ({
        ...prev,
        [resumeId]: data.ai_analysis,
      }))
    } catch (err) {
      setAiError(err.message || 'Failed to generate AI analysis.')
    } finally {
      setAiLoading(false)
    }
  }

  const detectedSkills = [
    ...new Set(
      reports.flatMap((report) => report.detected_skills || [])
    ),
  ]

  const missingSkills = [
    ...new Set(
      reports.flatMap((report) => report.missing_skills || [])
    ),
  ]

  const averageMatch = reports.length
    ? (
        reports.reduce(
          (total, report) =>
            total + (report.skill_match_percentage || 0),
          0
        ) / reports.length
      ).toFixed(2)
    : '0.00'

  const latestReport = reports[0]

  const latestAIAnalysis = latestReport
    ? aiAnalysis[latestReport.resume_id]
    : null

  return (
    <div className="page-container">
      <header className="topbar">
        <div>
          <h1>Resume Analysis</h1>
          <p>Understand your resume and identify skill gaps.</p>
        </div>
      </header>

      <section className="welcome">
        <h2>Your Analysis Overview</h2>
        <p>
          Review your detected skills, compare your skills with your target
          role, and identify areas for improvement.
        </p>
      </section>

      {error && (
        <div className="resume-error">{error}</div>
      )}

      <section className="stats">
        <div className="stat-card">
          <FileSearch size={28} />
          <h3>Skills Detected</h3>
          <p>{loading ? '...' : detectedSkills.length}</p>
        </div>

        <div className="stat-card">
          <Target size={28} />
          <h3>Average Skill Match</h3>
          <p>{loading ? '...' : `${averageMatch}%`}</p>
        </div>

        <div className="stat-card">
          <Brain size={28} />
          <h3>Missing Skills</h3>
          <p>{loading ? '...' : missingSkills.length}</p>
        </div>
      </section>

      <section className="analysis-reports">
        <div className="analysis-heading">
          <div>
            <h2>Analysis Reports</h2>
            <p>{reports.length} report(s) available</p>
          </div>
        </div>

        {loading ? (
          <p>Loading analysis reports...</p>
        ) : reports.length === 0 ? (
          <div className="activity">
            <FileSearch size={36} />
            <h3>No analysis reports available yet.</h3>
            <p>
              Upload a resume and click Analyze Resume to generate your
              first report.
            </p>
          </div>
        ) : (
          <div className="analysis-report-list">
            {reports.map((report) => (
              <article
                className="analysis-report-card"
                key={report.id}
              >
                <div className="analysis-report-header">
                  <div>
                    <h3>{report.resume_name}</h3>
                    <p>{report.target_role}</p>
                    <span>
                      {new Date(report.created_at).toLocaleString()}
                    </span>
                  </div>

                  <div className="analysis-score">
                    <strong>{report.skill_match_percentage}%</strong>
                    <span>Skill Match</span>
                  </div>
                </div>

                <div className="analysis-skills-section">
                  <h4>
                    <CheckCircle size={17} />
                    Matched Skills ({report.matched_skills?.length || 0})
                  </h4>

                  <div className="analysis-skill-list">
                    {report.matched_skills?.length > 0 ? (
                      report.matched_skills.map((skill) => (
                        <span className="matched-skill" key={skill}>
                          {skill}
                        </span>
                      ))
                    ) : (
                      <p>No matching skills detected.</p>
                    )}
                  </div>
                </div>

                <div className="analysis-skills-section">
                  <h4>
                    <XCircle size={17} />
                    Missing Skills ({report.missing_skills?.length || 0})
                  </h4>

                  <div className="analysis-skill-list">
                    {report.missing_skills?.length > 0 ? (
                      report.missing_skills.map((skill) => (
                        <span className="missing-skill" key={skill}>
                          {skill}
                        </span>
                      ))
                    ) : (
                      <p>No missing skills.</p>
                    )}
                  </div>
                </div>

                <div className="analysis-skills-section">
                  <h4>All Detected Skills</h4>

                  <div className="analysis-skill-list">
                    {(report.detected_skills || []).map((skill) => (
                      <span className="detected-skill" key={skill}>
                        {skill}
                      </span>
                    ))}
                  </div>
                </div>

                <div className="analysis-recommendations">
                  <h4>
                    <Lightbulb size={19} />
                    Skill Improvement Recommendations
                  </h4>

                  {recommendations[report.id] === undefined ? (
                    <p>Loading recommendations...</p>
                  ) : recommendations[report.id].length === 0 ? (
                    <p>No recommendations available for this report.</p>
                  ) : (
                    recommendations[report.id].map((item) => (
                      <div className="recommendation-card" key={item.skill}>
                        <h5>{item.skill}</h5>

                        <p>
                          <strong>Why it matters:</strong> {item.reason}
                        </p>

                        <p>
                          <strong>What to learn:</strong> {item.suggestion}
                        </p>

                        <p>
                          <Code size={15} />
                          <strong> Suggested project:</strong> {item.project}
                        </p>
                      </div>
                    ))
                  )}
                </div>

                {report.id === latestReport?.id && (
                  <div className="ai-analysis-section">
                    <div className="analysis-heading">
                      <div>
                        <h3>
                          <Sparkles size={20} />
                          Gemini AI Resume Analysis
                        </h3>
                        <p>
                          Get AI-powered feedback and personalized
                          improvement suggestions for your resume.
                        </p>
                      </div>
                    </div>

                    <button
                      className="primary-button"
                      onClick={() => generateAIAnalysis(report.resume_id)}
                      disabled={aiLoading}
                    >
                      {aiLoading ? (
                        <>
                          <RefreshCw size={17} />
                          Generating AI Analysis...
                        </>
                      ) : latestAIAnalysis ? (
                        <>
                          <RefreshCw size={17} />
                          Regenerate AI Analysis
                        </>
                      ) : (
                        <>
                          <Sparkles size={17} />
                          Generate AI Analysis
                        </>
                      )}
                    </button>

                    {aiError && (
                      <div className="resume-error">{aiError}</div>
                    )}

                    {aiLoading && (
                      <p className="ai-loading-message">
                        Gemini is reviewing your resume. This may take
                        a little time.
                      </p>
                    )}

                    {latestAIAnalysis && (
                      <div className="ai-analysis-results">
                        <div className="ai-result-card">
                          <h4>Overall Assessment</h4>
                          <p>{latestAIAnalysis.overall_assessment}</p>
                        </div>

                        <div className="ai-result-card">
                          <h4>
                            <CheckCircle size={17} />
                            Strengths
                          </h4>
                          <ul>
                            {(latestAIAnalysis.strengths || []).map(
                              (item, index) => (
                                <li key={index}>{item}</li>
                              )
                            )}
                          </ul>
                        </div>

                        <div className="ai-result-card">
                          <h4>
                            <XCircle size={17} />
                            Missing Skills
                          </h4>
                          <ul>
                            {(latestAIAnalysis.missing_skills || []).map(
                              (item, index) => (
                                <li key={index}>{item}</li>
                              )
                            )}
                          </ul>
                        </div>

                        <div className="ai-result-card">
                          <h4>
                            <Lightbulb size={17} />
                            Improvement Suggestions
                          </h4>
                          <ul>
                            {(latestAIAnalysis.improvement_suggestions || []).map(
                              (item, index) => (
                                <li key={index}>{item}</li>
                              )
                            )}
                          </ul>
                        </div>

                        <div className="ai-result-card">
                          <h4>
                            <Code size={17} />
                            Recommended Projects
                          </h4>
                          <ul>
                            {(latestAIAnalysis.recommended_projects || []).map(
                              (item, index) => (
                                <li key={index}>{item}</li>
                              )
                            )}
                          </ul>
                        </div>

                        <div className="ai-result-card ai-summary-card">
                          <h4>Final Summary</h4>
                          <p>{latestAIAnalysis.summary}</p>
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </article>
            ))}
          </div>
        )}
      </section>
    </div>
  )
}

export default Analysis
