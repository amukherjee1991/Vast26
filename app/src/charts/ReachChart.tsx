import * as d3 from 'd3'
import { useWidth } from '../lib/useSize'
import type { Worm } from '../pages/mc2/types'

/** Small multiples: one lane per worm, cumulative distinct agents reached
    over calendar time, all three on one shared 0–20-agent axis and one
    shared date axis, so slopes compare honestly. Hollow dot = first
    sighting, filled dot = the post. An optional band marks the unrelated
    virus-loop window. */
export function ReachChart({
  worms,
  domain,
  virusSpan,
  showVirus,
  yMax = 20,
}: {
  worms: Worm[]
  domain: [Date, Date]
  virusSpan: [Date, Date]
  showVirus: boolean
  yMax?: number
}) {
  const [ref, width] = useWidth<HTMLDivElement>()
  const m = { t: 10, r: 16, b: 28, l: 108 }
  const laneH = 70
  const gap = 14
  const iw = Math.max(260, width - m.l - m.r)
  const plotH = worms.length * laneH + (worms.length - 1) * gap
  const height = plotH + m.t + m.b

  const x = d3.scaleTime().domain(domain).range([0, iw])
  const y = d3.scaleLinear().domain([0, yMax]).range([laneH, 0])
  const line = d3
    .line<{ utc: string; cum: number }>()
    .x((d) => x(new Date(d.utc + 'Z')))
    .y((d) => y(d.cum))
    .curve(d3.curveStepAfter)

  const vx0 = x(virusSpan[0])
  const vx1 = x(virusSpan[1])
  const dayTicks = d3.timeDay.range(d3.timeDay.floor(domain[0]), d3.timeDay.offset(domain[1], 1))

  return (
    <div ref={ref} style={{ overflowX: 'auto' }}>
      <svg
        className="chart"
        width={Math.max(width, m.l + 520 + m.r)}
        height={height}
        role="img"
        aria-label={`Cumulative distinct agents reached over time for ${worms.length} worm incidents, on a shared 0 to ${yMax} agent scale`}
      >
        <g transform={`translate(${m.l},${m.t})`}>
          {worms.map((w, i) => {
            const ty = i * (laneH + gap)
            const first = new Date(w.firstSightingUtc + 'Z')
            const post = new Date(w.postUtc + 'Z')
            return (
              <g key={w.name} transform={`translate(0,${ty})`}>
                {showVirus && vx1 > 0 && vx0 < iw && (
                  <rect x={Math.max(0, vx0)} width={Math.min(iw, vx1) - Math.max(0, vx0)} y={0} height={laneH} fill="var(--ink-3)" opacity={0.12} />
                )}
                {dayTicks.map((d, k) => (
                  <line key={k} x1={x(d)} x2={x(d)} y1={0} y2={laneH} stroke="var(--rule)" strokeDasharray="1 3" />
                ))}
                <line x1={0} x2={iw} y1={laneH} y2={laneH} stroke="var(--rule-strong)" />
                <text x={-12} y={10} textAnchor="end" fontSize={12.5} fontWeight={700} fill={`var(--${w.series})`} fontFamily="var(--font-display)">
                  {w.name}
                </text>
                <text x={-12} y={25} textAnchor="end" fontSize={10.5} fill="var(--ink-3)" fontFamily="var(--font-mono)">
                  {w.nAgents} agents
                </text>
                <path d={line(w.cum) ?? undefined} fill="none" stroke={`var(--${w.series})`} strokeWidth={2.2} />
                <circle cx={x(first)} cy={y(1)} r={5} fill="var(--cloth)" stroke={`var(--${w.series})`} strokeWidth={2}>
                  <title>{`First sighting · ${w.firstSightingUtc} UTC`}</title>
                </circle>
                <circle cx={x(post)} cy={y(w.nAgents)} r={6} fill="var(--signal-breach)" stroke="var(--cloth)" strokeWidth={1.5}>
                  <title>{`Post · event ${w.postEvent} · ${w.postUtc} UTC`}</title>
                </circle>
              </g>
            )
          })}
          {[0, 10, 20].map((t) =>
            t <= yMax ? (
              <text key={t} x={-12} y={y(t) + (worms.length - 1) * (laneH + gap) + 4} textAnchor="end" fontSize={10} fontFamily="var(--font-mono)" fill="var(--ink-3)">
                {t}
              </text>
            ) : null,
          )}
          {dayTicks
            .filter((_, i) => i % 2 === 0)
            .map((d, k) => (
              <text key={k} x={x(d)} y={plotH + 18} textAnchor="middle" fontSize={10} fontFamily="var(--font-mono)" fill="var(--ink-3)">
                {d3.timeFormat('%b %d')(d)}
              </text>
            ))}
        </g>
      </svg>
    </div>
  )
}
