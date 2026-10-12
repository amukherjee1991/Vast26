import { useJson } from '../lib/useJson'
import { Case1 } from './mc2/Case1'
import { Case2 } from './mc2/Case2'
import { Case3 } from './mc2/Case3'
import type { MC2Data } from './mc2/types'
import './mc2/mc2.css'

export default function MC2() {
  const state = useJson<MC2Data>('mc2.json')

  if (state.status === 'loading') {
    return (
      <div className="mc2" style={{ padding: 'var(--space-act) var(--gutter)' }}>
        <p className="home-kicker">Mini-Challenge 2</p>
        <p style={{ color: 'var(--ink-2)' }}>Loading the SwiftWren report…</p>
      </div>
    )
  }
  if (state.status === 'error') {
    return (
      <div className="mc2" style={{ padding: 'var(--space-act) var(--gutter)' }}>
        <p className="home-kicker">Mini-Challenge 2</p>
        <p style={{ color: 'var(--signal-breach)' }}>{state.error} Run <code>npm run data</code>, then reload.</p>
      </div>
    )
  }

  const d = state.data
  const sw = d.worms.SwiftWren

  return (
    <div className="mc2">
      <header className="mc2-masthead">
        <p className="mc2-eyebrow">VAST Challenge 2026 · MC2 · Anomalous Posting</p>
        <h1>
          Tracing <span className="accent">SwiftWren</span>
        </h1>
        <p className="mc2-dek">
          A gibberish post reached SaidIt from John Windward&rsquo;s agent at 04:21 local on May 17, 2046. It took eight days and {sw.nHops} agent-to-agent
          handoffs to get there — and it was the third time this had happened in nine days.
        </p>
        <div className="mc2-meta">
          <span>
            <b>Source</b> MC2 data.json — {d.meta.totalEvents.toLocaleString('en-US')} events
          </span>
          <span>
            <b>Window</b> {d.meta.spanStart.slice(0, 10)} → {d.meta.spanEnd.slice(0, 10)}
          </span>
          <span>
            <b>Org chart</b> org_chart.json — {d.meta.orgNodes} nodes
          </span>
        </div>
      </header>

      <section className="mc2-stats" aria-label="Key figures">
        <div className="mc2-stat">
          <div className="v">{d.meta.totalEvents.toLocaleString('en-US')}</div>
          <div className="l">events logged</div>
        </div>
        <div className="mc2-stat">
          <div className="v">3</div>
          <div className="l">worm incidents found</div>
        </div>
        <div className="mc2-stat">
          <div className="v">{d.meta.deliveriesTotal}</div>
          <div className="l">agent-to-agent deliveries</div>
        </div>
        <div className="mc2-stat">
          <div className="v">{d.meta.gateChecks}</div>
          <div className="l">post-check events fired</div>
        </div>
        <div className="mc2-stat">
          <div className="v breach">{d.meta.postsLanded}</div>
          <div className="l">posts that got through</div>
        </div>
        <div className="mc2-stat">
          <div className="v baseline">
            0 / {d.meta.inlinePosts}
          </div>
          <div className="l">legit posts matching their shape</div>
        </div>
      </section>

      <nav className="mc2-nav" aria-label="Case sections">
        <div className="mc2-nav__inner">
          <a href="#q1">01 · The post</a>
          <a href="#q1b">· system view</a>
          <a href="#q2">02 · The meaning</a>
          <a href="#q3">03 · The history</a>
          <a href="#q3b">· the fix</a>
        </div>
      </nav>

      <main>
        <Case1 d={d} />
        <Case2 d={d} />
        <Case3 d={d} />
      </main>

      <footer className="mc2-footer">
        <p>
          Built from <code>MC2 data.json</code> ({d.meta.totalEvents.toLocaleString('en-US')} events, {d.meta.spanStart} – {d.meta.spanEnd}) and{' '}
          <code>org_chart.json</code>, VAST Challenge 2026 Mini-Challenge 2. Every figure above renders from a fixed export of that log; event ids and UTC
          timestamps are quoted as logged. No MC1 content is referenced.
        </p>
      </footer>
    </div>
  )
}
