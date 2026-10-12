import { useState } from 'react'
import type { ChainHop } from '../pages/mc2/types'
import { fmtClock, fmtDate, nice } from '../pages/mc2/types'

/** One bar per day of a hop chain, with a scrubber and a list of the real
    events for the selected day. Collapses a long agent-to-agent chain (e.g.
    186 hops over 9 days) to something scannable, without hiding any event —
    every row in the list below is a real logged delivery. */
export function DayStrip({ perDay, chain, color = 'var(--moon)' }: { perDay: Record<string, number>; chain: ChainHop[]; color?: string }) {
  const days = Object.keys(perDay).sort()
  const [idx, setIdx] = useState(days.length - 1)
  const max = Math.max(...Object.values(perDay))
  const day = days[idx]
  const rows = chain.filter((h) => h.utc.slice(0, 10) === day)

  return (
    <div className="daystrip">
      <div className="daystrip__scroll">
        <div className="daystrip__bars">
          {days.map((d, i) => (
            <button
              key={d}
              type="button"
              className="daystrip__col"
              aria-pressed={i === idx}
              onClick={() => setIdx(i)}
              title={`${fmtDate(d)}: ${perDay[d]} deliveries`}
            >
              <span className="daystrip__bar" style={{ height: `${(perDay[d] / max) * 100}%`, background: color }} />
            </button>
          ))}
        </div>
        <div className="daystrip__labels">
          {days.map((d, i) => (
            <div key={d} className="daystrip__label" data-active={i === idx}>
              <span className="d">{fmtDate(d)}</span>
              <span className="c">{perDay[d]}</span>
            </div>
          ))}
        </div>
      </div>
      <div className="daystrip__scrub">
        <input
          type="range"
          min={0}
          max={days.length - 1}
          step={1}
          value={idx}
          onChange={(e) => setIdx(Number(e.target.value))}
          aria-label="Scrub through the propagation days"
        />
        <span className="daystrip__readout">
          <b>{fmtDate(day)}</b> · {rows.length} deliveries
        </span>
      </div>
      <ol className="daystrip__list">
        {rows.map((r) => (
          <li key={r.id}>
            <span className="t">{fmtClock(r.utc)}</span>
            <span className="who">
              <b>{nice(r.from)}</b> → <b>{nice(r.to)}</b>
            </span>
            <span className="id">#{r.id}</span>
          </li>
        ))}
      </ol>
    </div>
  )
}
