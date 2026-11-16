
import {
  FileText,
  Brain,
  BriefcaseBusiness,
  Upload
} from 'lucide-react'

function Dashboard() {
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

        <button className="upload-button">
          <Upload size={18} />
          Upload Resume
        </button>
      </section>

      <section className="stats">
        <div className="stat-card">
          <FileText size={24} />
          <h3>My Resumes</h3>
          <p>0</p>
        </div>

        <div className="stat-card">
          <Brain size={24} />
          <h3>Resume Analyses</h3>
          <p>0</p>
        </div>

        <div className="stat-card">
          <BriefcaseBusiness size={24} />
          <h3>Job Matches</h3>
          <p>0</p>
        </div>
      </section>

      <section className="activity">
        <h2>Recent Activity</h2>
        <p>No recent activity yet.</p>
        <span>Upload your first resume to get started.</span>
      </section>
    </>
  )
}

export default Dashboard
