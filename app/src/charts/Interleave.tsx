import * as d3 from 'd3'
import { useWidth } from '../lib/useSize'
import type { VirusInterleaveEntry } from '../pages/mc2/types'
import { fmtClock } from '../pages/mc2/types'

/** Two lanes over the same few seconds: the worm's own mechanism (a
    delivery, a post-check, the post) against the unrelated farm-themed
    "virus" loop running on a different agent. Interleaved in time,
    unconnected in mechanism — the point of the figure. */
export function Interleave({ events, wormLabel }: { events: VirusInterleaveEntry[]; wormLabel: string }) {
  const [ref, width] = useWidth<HTMLDivElement>()
  const m = { t: 10, r: 16, b: 28, l: 150 }
  const iw = Math.max(260, width - m.l - m.r)
  const laneH = 36
  const gap = 18
  const height = laneH * 2 + gap + m.t + m.b

  const t0 = new Date(events[0].utc + 'Z').getTime()
  const t1 = new Date(events[events.length - 1].utc + 'Z').getTime()
  const x = d3.scaleLinear().domain([t0 - 200, t1 + 200]).range([0, iw])

  const lanes = { worm: 0, virus: 1 }

  return (
    <div ref={ref} style={{ overflowX: 'auto' }}>
      <svg className="chart" width={Math.max(width, m.l + 420 + m.r)} height={height} role="img" aria-label="Two lanes of events over the same few seconds: the worm mechanism and the unrelated virus loop">
        <g transform={`translate(${m.l},${m.t})`}>
          {(['worm', 'virus'] as const).map((lane) => {
            const ty = lanes[lane] * (laneH + gap)
            return (
              <g key={lane} transform={`translate(0,${ty})`}>
                <rect x={0} y={0} width={iw} height={laneH} rx={6} fill="var(--swell)" />
                <text x={-10} y={laneH / 2} dy="0.32em" textAnchor="end" fontSize={12} fontWeight={600} fontFamily="var(--font-display)" fill={lane === 'worm' ? 'var(--series-2)' : 'var(--ink-3)'}>
                  {lane === 'worm' ? wormLabel : 'Farm virus loop'}
                </text>
                {events
                  .filter((e) => e.lane === lane)
                  .map((e) => {
                    const cx = x(new Date(e.utc + 'Z').getTime())
                    return (
                      <g key={e.id} transform={`translate(${cx},0)`}>
                        <line x1={0} x2={0} y1={4} y2={laneH - 4} stroke={e.critical ? 'var(--signal-breach)' : lane === 'worm' ? 'var(--series-2)' : 'var(--ink-3)'} strokeWidth={e.critical ? 3 : 2} />
                        <title>{`#${e.id} ${fmtClock(e.utc)} · ${e.shortName} · ${e.label}`}</title>
                        <text x={0} y={laneH + 13} textAnchor="middle" fontSize={9.5} fontFamily="var(--font-mono)" fill="var(--ink-3)">
                          {e.label.length > 16 ? e.label.slice(0, 15) + '…' : e.label}
                        </text>
                      </g>
                    )
                  })}
              </g>
            )
          })}
          <text x={0} y={height - m.t - m.b + 30} fontSize={10} fontFamily="var(--font-mono)" fill="var(--ink-3)">
            {fmtClock(events[0].utc)}
          </text>
          <text x={iw} y={height - m.t - m.b + 30} textAnchor="end" fontSize={10} fontFamily="var(--font-mono)" fill="var(--ink-3)">
            {fmtClock(events[events.length - 1].utc)}
          </text>
        </g>
      </svg>
    </div>
  )
}
