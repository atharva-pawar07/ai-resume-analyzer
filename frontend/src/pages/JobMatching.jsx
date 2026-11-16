
import { BriefcaseBusiness, Search, Target } from 'lucide-react'

function JobMatching() {
  return (
    <div className="page-container">
      <header className="topbar">
        <div>
          <h1>Job Matching</h1>
          <p>Discover jobs that match your skills.</p>
        </div>
      </header>

      <section className="welcome">
        <h2>Find Your Best Job Matches</h2>
        <p>
          Compare your resume skills with job descriptions and discover
          opportunities that suit your profile.
        </p>
      </section>

      <section className="stats">
        <div className="stat-card">
          <BriefcaseBusiness size={28} />
          <h3>Available Jobs</h3>
          <p>0</p>
        </div>

        <div className="stat-card">
          <Target size={28} />
          <h3>Job Matches</h3>
          <p>0</p>
        </div>
      </section>

      <section className="activity">
        <Search size={32} />
        <h2>No Job Matches Yet</h2>
        <p>Your job matching reports will appear here.</p>
        <span>Add a job description and compare it with your resume.</span>
      </section>
    </div>
  )
}

export default JobMatching
