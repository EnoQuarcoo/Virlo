import { Fragment, useEffect } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import './LandingPage.css'

function useScrollReveal() {
  useEffect(() => {
    const els = document.querySelectorAll('.reveal')
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('revealed')
          }
        })
      },
      { threshold: 0.12 }
    )
    els.forEach((el) => observer.observe(el))
    return () => observer.disconnect()
  }, [])
}

const FEATURES = [
  {
    num: '01',
    title: 'Referral Tracking',
    desc: 'Every click, signup, and conversion traced back to its source in real time.',
  },
  {
    num: '02',
    title: 'Live Leaderboard',
    desc: 'Gamify your referral program with a real-time ranked leaderboard your users will compete on.',
  },
  {
    num: '03',
    title: 'Campaign Management',
    desc: 'Create and manage multiple referral campaigns from a single dashboard.',
  },
  {
    num: '04',
    title: 'API Integration',
    desc: 'Drop our API into your existing stack. Up and running in minutes, not days.',
  },
]

const STEPS = [
  {
    num: '01',
    title: 'Create a campaign',
    desc: 'Set your reward, craft your message, and launch in minutes.',
  },
  {
    num: '02',
    title: 'Users get a personal link',
    desc: 'When your users sign up they receive a unique shareable referral link.',
  },
  {
    num: '03',
    title: 'The leaderboard tracks who wins',
    desc: 'Watch your top advocates rise and reward them automatically.',
  },
]

export default function LandingPage() {
  useScrollReveal()
  const navigate = useNavigate()

  return (
    <div className="landing">
      {/* ── Nav ── */}
      <nav className="nav">
        <Link to="/" className="nav-logo">Virlo</Link>
        <Link to="/login" className="btn-nav">Login</Link>
      </nav>

      {/* ── Hero ── */}
      <section className="hero">
        <div className="hero-text hero-enter">
          <h1>Turn Every Customer Into a Growth Engine</h1>
          <p>
            Virlo gives your business a referral program in minutes.
            Watch the leaderboard fill up.
          </p>
          <button className="btn-primary" onClick={() => navigate('/signup')}>
            Get Started
          </button>
        </div>

        <div className="hero-contours" aria-hidden="true">
          <div className="contour c1" />
          <div className="contour c2" />
          <div className="contour c3" />
          <div className="contour c4" />
          <div className="contour c5" />
        </div>
      </section>

      {/* ── How It Works ── */}
      <section className="section how-section">
        <h2 className="section-title reveal">How It Works</h2>
        <div className="steps">
          {STEPS.map((step, i) => (
            <Fragment key={step.num}>
              <div className="step reveal" style={{ '--delay': `${i * 120}ms` }}>
                <div className="step-num">{step.num}</div>
                <h3>{step.title}</h3>
                <p>{step.desc}</p>
              </div>
              {i < STEPS.length - 1 && (
                <div className="step-arrow reveal" style={{ '--delay': `${i * 120 + 60}ms` }}>
                  <svg width="28" height="28" viewBox="0 0 28 28" fill="none">
                    <path d="M6 14h16M16 8l6 6-6 6" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
                  </svg>
                </div>
              )}
            </Fragment>
          ))}
        </div>
      </section>

      {/* ── Features ── */}
      <section className="section features-section">
        <h2 className="section-title reveal">Built for Growth</h2>
        <div className="features-grid">
          {FEATURES.map((f) => (
            <div className="feature-card reveal" key={f.num} style={{ '--delay': `${parseInt(f.num) * 80}ms` }}>
              <h3>{f.title}</h3>
              <p>{f.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* ── Footer ── */}
      <footer className="footer">
        <Link to="/" className="footer-logo">Virlo</Link>
        <div className="footer-links">
          <span>Terms</span>
          <span>Privacy</span>
        </div>
      </footer>
    </div>
  )
}