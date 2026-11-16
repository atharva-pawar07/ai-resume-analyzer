
import { Brain, FileSearch, Target } from 'lucide-react'

function Analysis() {
  return (
    <div className="page-container">
      <header className="topbar">
        <div>
          <h1>Resume Analysis</h1>
          <p>Understand your resume and identify skill gaps.</p>
        </div>
      </header>

      <section className="welcome">
        <h2>Analyze Your Resume</h2>
        <p>
          Get insights into your skills and see how well your resume matches
          your target career role.
        </p>
      </section>

      <section className="stats">
        <div className="stat-card">
          <FileSearch size={28} />
          <h3>Skills Detected</h3>
          <p>--</p>
        </div>

        <div className="stat-card">
          <Target size={28} />
          <h3>Skill Match</h3>
          <p>--%</p>
        </div>

        <div className="stat-card">
          <Brain size={28} />
          <h3>Missing Skills</h3>
          <p>--</p>
        </div>
      </section>

      <section className="activity">
        <h2>Analysis Reports</h2>
        <p>No analysis reports available yet.</p>
        <span>Upload a resume and start your first analysis.</span>
      </section>
    </div>
  )
}

export default Analysis
