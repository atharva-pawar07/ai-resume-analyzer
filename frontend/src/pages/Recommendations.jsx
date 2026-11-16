
import { Lightbulb, BookOpen, TrendingUp } from 'lucide-react'

function Recommendations() {
  return (
    <div className="page-container">
      <header className="topbar">
        <div>
          <h1>Skill Recommendations</h1>
          <p>Discover which skills you should learn next.</p>
        </div>
      </header>

      <section className="welcome">
        <h2>Improve Your Career Profile</h2>
        <p>
          Get personalized suggestions based on the missing skills
          identified in your resume analysis.
        </p>
      </section>

      <section className="stats">
        <div className="stat-card">
          <Lightbulb size={28} />
          <h3>Suggested Skills</h3>
          <p>0</p>
        </div>

        <div className="stat-card">
          <BookOpen size={28} />
          <h3>Learning Resources</h3>
          <p>0</p>
        </div>

        <div className="stat-card">
          <TrendingUp size={28} />
          <h3>Career Progress</h3>
          <p>--</p>
        </div>
      </section>

      <section className="activity">
        <h2>Your Recommendations</h2>
        <p>No recommendations available yet.</p>
        <span>Complete a resume analysis to get skill recommendations.</span>
      </section>
    </div>
  )
}

export default Recommendations
