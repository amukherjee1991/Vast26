import * as d3 from 'd3'
import { useWidth } from '../lib/useSize'

export interface DumbbellRow {
  key: string
  label: string
  lo: number
  hi: number
}

/** A row per label, two dots (lo/hi) joined by a line on a shared linear
    scale, with the raw values printed next to each dot. Used to compare a
    "before" value against an "after" value across several rows — e.g.
    pre-crisis vs. crisis-day channel volume, or per-agent metrics. */
export function Dumbbell({
  rows,
  max,
  gridStep,
  loColor = 'var(--ink-3)',
  hiColor = 'var(--moon)',
  format = (n: number) => n.toLocaleString('en-US'),
  unit,
}: {
  rows: DumbbellRow[]
  max: number
  gridStep: number
  loColor?: string
  hiColor?: string
  format?: (n: number) => string
  unit?: string
}) {
  const [ref, width] = useWidth<HTMLDivElement>()
  const lw = Math.min(160, width * 0.32)
  const rowH = 38
  const m = { t: 20, r: 16, b: 26 }
  const iw = Math.max(80, width - lw - m.r)
  const height = rows.length * rowH + m.t + m.b
  const x = d3.scaleLinear().domain([0, max]).range([0, iw])
  const ticks: number[] = []
  for (let v = 0; v <= max; v += gridStep) ticks.push(v)

  return (
    <div ref={ref}>
      <svg className="chart" width={width} height={height} role="img" aria-label={`Comparison of ${rows.length} rows, before and after values on a 0 to ${max}${unit ?? ''} scale`}>
        <g transform={`translate(${lw},${m.t})`}>
          {ticks.map((t) => (
            <g key={t}>
              <line x1={x(t)} x2={x(t)} y1={0} y2={rows.length * rowH} stroke="var(--rule)" strokeDasharray="2 3" />
              <text x={x(t)} y={rows.length * rowH + 18} textAnchor="middle" fontSize={11} fill="var(--ink-3)" fontFamily="var(--font-mono)">
                {t}
              </text>
            </g>
          ))}
          {rows.map((r, i) => {
            const loX = x(r.lo)
            const hiX = x(r.hi)
            const left = Math.min(loX, hiX)
            const w = Math.abs(hiX - loX)
            return (
              <g key={r.key} transform={`translate(0,${i * rowH + rowH / 2})`}>
                <title>{`${r.label}: ${format(r.lo)} → ${format(r.hi)}`}</title>
                <text x={-10} dy="0.32em" textAnchor="end" fontSize={13} fontWeight={600} fill="var(--ink)">
                  {r.label}
                </text>
                <line x1={0} x2={iw} y1={0} y2={0} stroke="var(--rule)" />
                <line x1={left} x2={left + w} y1={0} y2={0} stroke={hiColor} strokeWidth={2.5} strokeLinecap="round" />
                <circle cx={loX} cy={0} r={6.5} fill={loColor} stroke="var(--cloth)" strokeWidth={1.5} />
                <circle cx={hiX} cy={0} r={6.5} fill={hiColor} stroke="var(--cloth)" strokeWidth={1.5} />
                <text x={loX} y={-14} textAnchor="middle" fontSize={11} fontFamily="var(--font-mono)" fill="var(--ink-2)">
                  {format(r.lo)}
                </text>
                <text x={hiX} y={16} textAnchor="middle" fontSize={11} fontFamily="var(--font-mono)" fontWeight={600} fill="var(--ink)">
                  {format(r.hi)}
                </text>
              </g>
            )
          })}
        </g>
      </svg>
    </div>
  )
}
