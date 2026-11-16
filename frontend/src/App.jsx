
import {
  LayoutDashboard,
  FileText,
  Brain,
  BriefcaseBusiness,
  Lightbulb,
  UserCircle,
  Bell
} from 'lucide-react'

import {
  NavLink,
  Routes,
  Route,
  Outlet,
  Navigate
} from 'react-router-dom'

import Dashboard from './pages/Dashboard'
import Resumes from './pages/Resumes'
import Analysis from './pages/Analysis'
import JobMatching from './pages/JobMatching'
import Recommendations from './pages/Recommendations'
import Login from './pages/Login'
import Register from './pages/Register'
import ProtectedRoute from './components/ProtectedRoute'
import { LogOut } from 'lucide-react'
import { useAuth } from './context/AuthContext'
import { useNavigate } from 'react-router-dom'

import './App.css'

function LogoutButton() {
  const { logout } = useAuth()
  const navigate = useNavigate()

  function handleLogout() {
    logout()
    navigate('/login')
  }

  return (
    <button onClick={handleLogout} title="Logout">
      <LogOut size={18} />
    </button>
  )
}

function AppLayout() {
  const { user } = useAuth()
  return (
    <div className="app">
      <aside className="sidebar">
        <h2>AI Career Copilot</h2>

        <nav>
          <NavLink to="/" end>
            <LayoutDashboard size={19} />
            Dashboard
          </NavLink>

          <NavLink to="/resumes">
            <FileText size={19} />
            My Resumes
          </NavLink>

          <NavLink to="/analysis">
            <Brain size={19} />
            Resume Analysis
          </NavLink>

          <NavLink to="/job-matching">
            <BriefcaseBusiness size={19} />
            Job Matching
          </NavLink>

          <NavLink to="/recommendations">
            <Lightbulb size={19} />
            Recommendations
          </NavLink>
        </nav>

       <div className="sidebar-footer">
  <UserCircle size={20} />
  <span>{user?.full_name || 'My Account'}</span>
  <LogoutButton />
</div>
      </aside>

      <main className="main-content">
        <header className="topbar">
          <div className="page-heading">
            <h1>AI Career Copilot</h1>
            <p>Your personal career dashboard</p>
          </div>

          <button className="notification-button">
            <Bell size={20} />
          </button>
        </header>

        <Outlet />
      </main>
    </div>
  )
}

function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />

      <Route
        element={
          <ProtectedRoute>
            <AppLayout />
          </ProtectedRoute>
        }
      >
        <Route path="/" element={<Dashboard />} />
        <Route path="/resumes" element={<Resumes />} />
        <Route path="/analysis" element={<Analysis />} />
        <Route path="/job-matching" element={<JobMatching />} />
        <Route path="/recommendations" element={<Recommendations />} />
      </Route>

      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}

export default App
