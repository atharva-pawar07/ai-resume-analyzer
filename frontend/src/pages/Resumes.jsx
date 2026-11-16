
import { FileText, Upload } from 'lucide-react'

function Resumes() {
  return (
    <div className="page-container">
      <header className="topbar">
        <div>
          <h1>My Resumes</h1>
          <p>Manage and upload your resumes.</p>
        </div>
      </header>

      <section className="welcome">
        <h2>Manage Your Resumes</h2>
        <p>
          Upload your resume to analyze your skills and discover job opportunities.
        </p>

        <button className="upload-button">
          <Upload size={18} />
          Upload Resume
        </button>
      </section>

      <section className="activity">
        <FileText size={32} />
        <h2>No Resumes Yet</h2>
        <p>Your uploaded resumes will appear here.</p>
      </section>
    </div>
  )
}

export default Resumes
