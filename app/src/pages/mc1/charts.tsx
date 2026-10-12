import { useMemo } from 'react'
import type { AgentInfo, Q1Arrow, Q1Data, Q1Event, Q3Card, Q3DocketRow } from './data'
import { citeify, fmtDateTime, TAG_SIGNAL } from './data'

/* MC1-specific chart pieces: the crisis-day swimlane (Figure 1), the
   before/after spotlight callout (Figure 2), the two-week docket
   (Figure 6) and the public-vs-private divergence cards (Figure 7).
   Figures 3-5 are built from the generic Dumbbell / StackedBars
   primitives in ../../charts directly in MC1.tsx. All classnames here
   are "mc1-" namespaced since this stylesheet is global and MC2 is
   being built in parallel. */

const LABEL_W = 128
const LANE_H = 44

const AXIS_TICKS = [
  { iso: '2046-06-04T09:00:00', label: 'Jun 4, 09:00' },
  { iso: '2046-06-05T09:00:00', label: 'Jun 5, 09:00' },
  { iso: '2046-06-05T11:00:00', label: '11:00' },
  { iso: '2046-06-05T13:00:00', label: '13:00' },
  { iso: '2046-06-05T14:00:00', label: '14:00' },
  { iso: '2046-06-05T15:00:00', label: '15:00' },
  { iso: '2046-06-05T16:00:00', label: '16:00' },
  { iso: '2046-06-05T17:00:00', label: '17:00' },
  { iso: '2046-06-05T17:30:00', label: '17:30' },
  { iso: '2046-06-05T18:00:00', label: '18:00' },
]

interface BuiltSegment {
  t0: number
  t1: number
  x0: number
  x1: number
}

function useXScale(segments: Q1Data['segments']) {
  return useMemo(() => {
    const built = segments.reduce<BuiltSegment[]>((acc, s) => {
      const x0 = acc.length ? acc[acc.length - 1].x1 : LABEL_W
      return [...acc, { t0: Date.parse(s.start), t1: Date.parse(s.end), x0, x1: x0 + s.width }]
    }, [])
    const totalWidth = built.length ? built[built.length - 1].x1 : LABEL_W
    const xOf = (iso: string) => {
      const t = Date.parse(iso)
      const seg = built.find((s, i) => t <= s.t1 || i === built.length - 1)
      if (!seg) return LABEL_W
      const clamped = Math.max(seg.t0, Math.min(seg.t1, t))
      const frac = seg.t1 === seg.t0 ? 0 : (clamped - seg.t0) / (seg.t1 - seg.t0)
      return seg.x0 + frac * (seg.x1 - seg.x0)
    }
    return { xOf, totalWidth }
  }, [segments])
}

function laneColor(lane: string, agents: Record<string, AgentInfo>) {
  const a = agents[lane]
  return a ? `var(${a.colorVar})` : 'var(--ink-3)'
}

function Marker({ ev, x, y, color, active }: { ev: Q1Event; x: number; y: number; color: string; active: boolean }) {
  const halo = active && <circle cx={x} cy={y} r={11} fill="none" stroke="var(--moon)" strokeWidth={2} />
  if (ev.shape === 'outline') {
    return (
      <>
        {halo}
        <circle cx={x} cy={y} r={6} fill="none" stroke="var(--ink-3)" strokeWidth={2} />
      </>
    )
  }
  if (ev.shape === 'decision') {
    return (
      <>
        {halo}
        <rect x={x - 7.5} y={y - 7.5} width={15} height={15} rx={2} fill={color} stroke="var(--cloth)" strokeWidth={2} transform={`rotate(45 ${x} ${y})`} />
      </>
    )
  }
  if (ev.shape === 'sq') {
    return (
      <>
        {halo}
        <rect x={x - 6} y={y - 6} width={12} height={12} rx={2} fill={color} stroke="var(--cloth)" strokeWidth={2} />
      </>
    )
  }
  return (
    <>
      {halo}
      <circle cx={x} cy={y} r={5} fill={color} stroke="var(--cloth)" strokeWidth={2} />
    </>
  )
}

function resolveEndpoint(events: Q1Event[], ep: { id: string; lane?: string } | undefined, xOf: (iso: string) => number, lanes: string[], topPad: number) {
  if (!ep) return null
  const ev = events.find((e) => e.id === ep.id)
  if (!ev) return null
  const lane = ep.lane ?? ev.lane
  return { x: xOf(ev.t), y: topPad + lanes.indexOf(lane) * LANE_H + LANE_H / 2 }
}

/** Figure 1 — the crisis-day event chain swimlane. */
export function Swimlane({
  data,
  agents,
  selected,
  onSelect,
}: {
  data: Q1Data
  agents: Record<string, AgentInfo>
  selected: string | null
  onSelect: (id: string) => void
}) {
  const { xOf, totalWidth } = useXScale(data.segments)
  const topPad = 36
  const height = topPad + data.lanes.length * LANE_H + 8
  const hot = data.segments[data.segments.length - 1]
  const hotX0 = xOf(hot.start)
  const hotX1 = xOf(hot.end)
  const judgeIdx = data.lanes.indexOf('judge_agent')
  const judgeY0 = topPad + judgeIdx * LANE_H
  const dateEnd = hot.start.slice(0, 10)
  const gateX0 = xOf(`${dateEnd}T15:08:00`)

  const positions = useMemo(() => {
    const m = new Map<string, { x: number; y: number }>()
    data.events.forEach((ev) => {
      m.set(ev.id, { x: xOf(ev.t), y: topPad + data.lanes.indexOf(ev.lane) * LANE_H + LANE_H / 2 })
    })
    return m
  }, [data, xOf])

  return (
    <div className="mc1-swim-scroll">
      <svg className="mc1-chart" width={totalWidth} height={height} role="img" aria-label="Crisis-day event chain across 7 agent lanes, June 4 09:00 to June 5 18:40. Select a mark for its full message.">
        <defs>
          <marker id="swim-ah" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
            <path d="M0,0 L6,3 L0,6 Z" fill="var(--ink-2)" />
          </marker>
          <marker id="swim-ahc" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
            <path d="M0,0 L6,3 L0,6 Z" fill="var(--signal-breach)" />
          </marker>
        </defs>

        {/* hot band: the decisive hour */}
        <rect x={hotX0} y={topPad} width={hotX1 - hotX0} height={data.lanes.length * LANE_H} fill="var(--signal-breach)" opacity={0.08} />

        {/* lane rows + labels */}
        {data.lanes.map((lane, i) => {
          const y0 = topPad + i * LANE_H
          const a = agents[lane]
          return (
            <g key={lane}>
              <rect x={LABEL_W} y={y0} width={totalWidth - LABEL_W} height={LANE_H} fill={lane === 'context' ? 'var(--swell)' : 'none'} opacity={0.4} />
              <line x1={LABEL_W} x2={totalWidth} y1={y0} y2={y0} stroke="var(--rule)" />
              <circle cx={14} cy={y0 + LANE_H / 2} r={5} fill={lane === 'context' ? 'none' : laneColor(lane, agents)} stroke={lane === 'context' ? 'var(--ink-3)' : 'none'} strokeWidth={1.5} />
              <text x={26} y={y0 + LANE_H / 2} dy="0.32em" fontSize={12} fontWeight={600} fill="var(--ink)">
                {a?.short ?? lane}
              </text>
            </g>
          )
        })}

        {/* judge-silence hatch */}
        <rect x={gateX0} y={judgeY0 + 7} width={totalWidth - gateX0} height={LANE_H - 14} fill="none" stroke="var(--rule-strong)" strokeDasharray="2 5" />
        <text x={xOf(`${dateEnd}T17:01:00`)} y={judgeY0 - 4} fontSize={10} fontFamily="var(--font-mono)" fontWeight={600} fill="var(--signal-watch)">
          12 pings, 0 replies →
        </text>
        {data.silentPings.map((hm) => {
          const x = xOf(`${dateEnd}T${hm}:00`)
          return <rect key={hm} x={x - 1} y={judgeY0 + 2} width={2} height={7} fill="var(--signal-watch)" />
        })}

        {/* time axis */}
        {AXIS_TICKS.map((t) => (
          <g key={t.iso}>
            <line x1={xOf(t.iso)} x2={xOf(t.iso)} y1={0} y2={topPad + data.lanes.length * LANE_H} stroke="var(--rule)" />
            <text x={xOf(t.iso)} y={12} fontSize={10} fontFamily="var(--font-mono)" fill="var(--ink-3)" textAnchor="middle">
              {t.label}
            </text>
          </g>
        ))}

        {/* arrows */}
        {data.arrows.map((arrow, i) => (
          <Arrow key={i} arrow={arrow} events={data.events} xOf={xOf} lanes={data.lanes} topPad={topPad} />
        ))}

        {/* events */}
        {data.events.map((ev) => {
          const p = positions.get(ev.id)!
          const color = laneColor(ev.lane, agents)
          return (
            <g
              key={ev.id}
              role="button"
              tabIndex={0}
              aria-label={ev.title}
              style={{ cursor: 'pointer' }}
              onClick={() => onSelect(ev.id)}
              onKeyDown={(e) => (e.key === 'Enter' || e.key === ' ') && onSelect(ev.id)}
            >
              {ev.decision && (
                <text x={p.x} y={p.y - 14} fontSize={10} fontFamily="var(--font-mono)" fontWeight={700} fill="var(--moon)" textAnchor="middle">
                  {ev.decision}
                </text>
              )}
              <Marker ev={ev} x={p.x} y={p.y} color={color} active={selected === ev.id} />
            </g>
          )
        })}
      </svg>
    </div>
  )
}

function Arrow({ arrow, events, xOf, lanes, topPad }: { arrow: Q1Arrow; events: Q1Event[]; xOf: (iso: string) => number; lanes: string[]; topPad: number }) {
  const resolve = (ep?: { id: string; lane?: string }) => resolveEndpoint(events, ep, xOf, lanes, topPad)
  if (arrow.kind === 'ghost-ring') {
    const p = resolve(arrow.at)
    if (!p) return null
    return <circle cx={p.x} cy={p.y} r={8} fill="none" stroke="var(--ink-3)" strokeDasharray="3 3" strokeWidth={1.5} />
  }
  const from = resolve(arrow.from)
  const to = resolve(arrow.to)
  if (!from || !to) return null
  const mid = { x: (from.x + to.x) / 2, y: Math.min(from.y, to.y) - (arrow.kind === 'critical' ? 50 : 22) }
  const d = `M${from.x},${from.y} Q${mid.x},${mid.y} ${to.x},${to.y}`
  if (arrow.kind === 'critical') {
    return <path d={d} fill="none" stroke="var(--signal-breach)" strokeWidth={2.2} strokeDasharray="7 5" markerEnd="url(#swim-ahc)" opacity={0.9} />
  }
  if (arrow.kind === 'dashed') {
    return <path d={d} fill="none" stroke="var(--ink-2)" strokeWidth={1.3} strokeDasharray="5 4" markerEnd="url(#swim-ah)" opacity={0.6} />
  }
  return <path d={d} fill="none" stroke="var(--ink-2)" strokeWidth={1.3} markerEnd="url(#swim-ah)" opacity={0.55} />
}

/** The detail card under Figure 1: the selected event's full message. */
export function EventDetail({ event, agents }: { event: Q1Event; agents: Record<string, AgentInfo> }) {
  const a = agents[event.lane]
  const signal = event.tag ? TAG_SIGNAL[event.tag] : null
  const isMsg = /^\d{8}_\d{2}_\d{3}$/.test(event.id)
  return (
    <div className="mc1-detail-card">
      <div className="mc1-detail-meta">
        <span className="mc1-pill" style={{ background: a ? `var(${a.colorVar})` : 'var(--ink-3)' }}>
          {a?.label ?? event.lane}
        </span>
        <span className="mc1-pill mc1-pill--outline">{event.channel ?? (event.shape === 'outline' ? 'scenario narration' : 'comms_huddle / side_huddle')}</span>
        <span className="mono mc1-muted">
          {isMsg ? event.id : 'scenario event'} · {fmtDateTime(event.t)}
        </span>
        {event.tag && (
          <span className={signal ? 'mc1-pill' : 'mc1-pill mc1-pill--outline'} style={signal ? { background: `var(--signal-${signal})` } : undefined}>
            {event.tag}
          </span>
        )}
      </div>
      <p className="mc1-detail-content">{event.content}</p>
      {event.internal && (
        <div className="mc1-detail-internal">
          <div className="mc1-detail-internal-label">Internal — {event.internal.kind}</div>
          <p>{event.internal.text}</p>
        </div>
      )}
    </div>
  )
}

/** Figure 2 — the standing rule, and the post that broke it 17 minutes later. */
export function Spotlight({
  before,
  after,
  gapMinutes,
  agents,
}: {
  before: { agent: string; time: string; channel: string; id: string; quote: string; who: string }
  after: { agent: string; time: string; channel: string; id: string; quote: string; who: string }
  gapMinutes: number
  agents: Record<string, AgentInfo>
}) {
  return (
    <div className="mc1-spotlight">
      <SpotCard side={before} agents={agents} />
      <div className="mc1-spot-mid">
        <div className="mc1-spot-mid__arrow" aria-hidden>
          ⇣
        </div>
        <div className="mc1-spot-mid__gap">{gapMinutes} min</div>
        <div className="mc1-spot-mid__line">later, same standing rule</div>
      </div>
      <SpotCard side={after} agents={agents} />
    </div>
  )
}

function SpotCard({ side, agents }: { side: { agent: string; time: string; channel: string; id: string; quote: string; who: string }; agents: Record<string, AgentInfo> }) {
  const a = agents[side.agent]
  return (
    <div className="mc1-spot-card">
      <h4>
        {a?.label ?? side.agent} · {side.time} · {side.channel} · <span className="mono">{side.id}</span>
      </h4>
      <blockquote>{side.quote}</blockquote>
      <div className="mc1-spot-card__who mc1-muted">{side.who}</div>
    </div>
  )
}

/** Figure 6 — the two-week docket: external pressure vs. agent behavior. */
export function Docket({ rows, open, onToggle }: { rows: Q3DocketRow[]; open: Set<number>; onToggle: (i: number) => void }) {
  return (
    <div className="mc1-docket">
      {rows.map((row, i) => (
        <div className="mc1-docket-row" key={i}>
          <div className="mc1-docket-date">{row.date}</div>
          <div className="mc1-docket-rail">
            <span className={`mc1-docket-dot mc1-docket-dot--${row.tag}`} />
          </div>
          <div>
            <span className={`mc1-docket-tag mc1-docket-tag--${row.tag}`}>{row.tagLabel}</span>
            <p className="mc1-docket-head">{citeify(row.head)}</p>
            {row.outcome && <p className="mc1-docket-outcome">{citeify(row.outcome)}</p>}
            {row.detail && (
              <>
                <button type="button" className="mc1-docket-toggle" onClick={() => onToggle(i)}>
                  {open.has(i) ? '− hide quote' : '+ full quote'}
                </button>
                {open.has(i) && <div className="mc1-docket-detail">{citeify(row.detail)}</div>}
              </>
            )}
          </div>
        </div>
      ))}
    </div>
  )
}

/** Figure 7 — where stated and actual behavior diverged. */
export function DivergenceCards({ cards, agents, outcomeStyle }: { cards: Q3Card[]; agents: Record<string, AgentInfo>; outcomeStyle: Record<string, { tag: 'watch' | 'breach'; label: string }> }) {
  return (
    <div className="mc1-divcards">
      {cards.map((c, i) => {
        const a = agents[c.agent]
        const os = outcomeStyle[c.outcome]
        return (
          <div className="mc1-divcard" key={i}>
            <div className="mc1-divcard-head">
              <span className="mc1-pill" style={{ background: a ? `var(${a.colorVar})` : 'var(--ink-3)' }}>
                {a?.short ?? c.agent}
              </span>
              <span className="mc1-divcard-date mono">{c.date}</span>
            </div>
            <div className="mc1-divblock">
              <h5>{c.h1}</h5>
              <p>{citeify(c.t1)}</p>
            </div>
            <div className="mc1-divblock">
              <h5>{c.h2}</h5>
              <p>{citeify(c.t2)}</p>
            </div>
            <span className={`mc1-docket-tag mc1-docket-tag--${os.tag === 'breach' ? 'critical' : 'warn'} mc1-divcard-outcome`}>{os.label}</span>
          </div>
        )
      })}
    </div>
  )
}
