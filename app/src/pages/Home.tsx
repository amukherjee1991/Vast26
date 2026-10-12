import { Link } from 'react-router-dom'
import './Home.css'

export default function Home() {
  return (
    <div className="home">
      <section className="home-hero">
        <p className="home-kicker">VAST Challenge 2026</p>
        <h1 className="home-title">Forensic Ledger</h1>
        <p className="home-dek">
          Two incident reports on an agentic-AI system at TenantThread, each
          reconstructed from a raw event log and traced back to its cause.
        </p>
      </section>
      <section className="home-reports">
        <Link to="/mc1" className="report-card">
          <span className="report-eyebrow">Mini-Challenge 1</span>
          <h2>The HarborCrest Leak</h2>
          <p>
            An embargoed merger surfaces 35 minutes early, from an AI legal
            agent&rsquo;s own account. Deliberate sabotage, or a system that
            broke under pressure?
          </p>
        </Link>
        <Link to="/mc2" className="report-card">
          <span className="report-eyebrow">Mini-Challenge 2</span>
          <h2>SwiftWren</h2>
          <p>
            A gibberish post lands on a public forum at 4:21am. Underneath it:
            an agent-to-agent worm that moved through 18 agents over 8 days.
          </p>
        </Link>
      </section>
    </div>
  )
}
