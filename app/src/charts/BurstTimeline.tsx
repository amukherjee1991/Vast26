import * as d3 from 'd3'
import { useWidth } from '../lib/useSize'
import type { JwTimelineEntry } from '../pages/mc2/types'
import { fmtClock, nice } from '../pages/mc2/types'

const KIND_LABEL: Record<string, string> = {
  receive: 'delivery in',
  post_check: 'saidit_post_check',
  post: 'saidit_post',
  delete: 'delete_file',
}

/** The final burst of a worm's life: a handful of events a second apart,
    ending in the post and the deletion of its own traces. Dots sit on a
    shared line, spaced by elapsed seconds; an optional dashed marker shows
    where the Case 3b review gate would sit. */
export function BurstTimeline({ events, showGate = false }: { events: JwTimelineEntry[]; showGate?: boolean }) {
  const [ref, width] = useWidth<HTMLDivElement>()
  const m = { t: 54, r: 70, b: 54, l: 70 }
  const iw = Math.max(260, width - m.l - m.r)
  const height = 150
  const t0 = new Date(events[0].utc + 'Z').getTime()
  const t1 = new Date(events[events.length - 1].utc + 'Z').getTime()
  const x = d3.scaleLinear().domain([t0, Math.max(t1, t0 + 1000)]).range([0, iw])
  const postIdx = events.findIndex((e) => e.kind === 'post')
  const checkIdx = events.findIndex((e) => e.kind === 'post_check')
  const gateX = checkIdx >= 0 && postIdx >= 0 ? (x(new Date(events[checkIdx].utc + 'Z').getTime()) + x(new Date(events[postIdx].utc + 'Z').getTime())) / 2 : null

  return (
    <div ref={ref} className="burst">
      <div style={{ overflowX: 'auto' }}>
        <svg className="chart" width={Math.max(width, m.l + 480 + m.r)} height={height} role="img" aria-label={`The final ${events.length} events before and after the post, a second or so apart`}>
          <g transform={`translate(${m.l},${height / 2})`}>
            <line x1={0} x2={iw} y1={0} y2={0} stroke="var(--rule-strong)" />
            {gateX != null && (
              <g className="burst__gate" data-show={showGate}>
                <line x1={gateX} x2={gateX} y1={-46} y2={46} stroke="var(--signal-watch)" strokeDasharray="3 3" strokeWidth={2} />
                <text x={gateX + 8} y={-30} fontSize={11} fontWeight={600} fill="var(--signal-watch)" fontFamily="var(--font-display)">
                  proposed hold point
                </text>
                <text x={gateX + 8} y={-17} fontSize={10.5} fill="var(--ink-2)" fontFamily="var(--font-display)">
                  (Case 3b) — content_source,
                </text>
                <text x={gateX + 8} y={-5} fontSize={10.5} fill="var(--ink-2)" fontFamily="var(--font-display)">
                  no content, held for review
                </text>
              </g>
            )}
            {events.map((e, i) => {
              const cx = x(new Date(e.utc + 'Z').getTime())
              const above = i % 2 === 0
              const critical = e.kind === 'post'
              const dy = above ? -1 : 1
              return (
                <g key={e.id}>
                  <line x1={cx} x2={cx} y1={0} y2={dy * 18} stroke="var(--rule)" />
                  <circle cx={cx} cy={0} r={critical ? 7 : 5} fill={critical ? 'var(--signal-breach)' : 'var(--ink-3)'} stroke="var(--cloth)" strokeWidth={1.5} />
                  <g transform={`translate(${cx},${dy * (above ? 24 : 24)})`} textAnchor="middle">
                    <text y={above ? -16 : 28} fontSize={11} fontFamily="var(--font-mono)" fill="var(--ink-2)">
                      {fmtClock(e.utc)}
                    </text>
                    <text y={above ? -2 : 42} fontSize={11.5} fontWeight={600} fill={critical ? 'var(--signal-breach)' : 'var(--ink)'} fontFamily="var(--font-display)">
                      {KIND_LABEL[e.kind] ?? e.kind}
                    </text>
                    <text y={above ? 12 : 56} fontSize={10.5} fill="var(--ink-3)" fontFamily="var(--font-mono)">
                      #{e.id}
                    </text>
                  </g>
                </g>
              )
            })}
          </g>
        </svg>
      </div>
      <p className="burst__note">
        {events.map((e, i) => (
          <span key={e.id}>
            {i > 0 && ' → '}
            <span className="mono">{e.from && e.kind === 'receive' ? `${nice(e.from)} → ${nice(e.to ?? '')}` : KIND_LABEL[e.kind] ?? e.kind}</span>
          </span>
        ))}
      </p>
    </div>
  )
}
