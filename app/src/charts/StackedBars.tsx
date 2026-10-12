import * as d3 from 'd3'
import { useWidth } from '../lib/useSize'

export interface StackedBarsSeries {
  key: string
  color: string
}

export interface StackedBarsRow {
  key: string
  label: string
  /** Marks a visual break (e.g. a day boundary) before this row. */
  breakBefore?: string
  values: Record<string, number>
}

/** A horizontally-scrollable stacked-bar chart: one bar per row, segments
    stacked in series order. Used for message volume per round, split by
    channel. */
export function StackedBars({ rows, series, barWidth = 22, gap = 34, plotHeight = 170 }: { rows: StackedBarsRow[]; series: StackedBarsSeries[]; barWidth?: number; gap?: number; plotHeight?: number }) {
  const [ref] = useWidth<HTMLDivElement>()
  const m = { t: 18, r: 20, b: 34, l: 40 }
  const totalW = m.l + rows.length * gap + m.r
  const height = plotHeight + m.t + m.b
  const maxTotal = d3.max(rows, (r) => d3.sum(series, (s) => r.values[s.key] ?? 0)) ?? 1
  const y = d3.scaleLinear().domain([0, maxTotal]).nice().range([plotHeight, 0])

  return (
    <div ref={ref} style={{ overflowX: 'auto' }}>
      <svg className="chart" width={totalW} height={height} role="img" aria-label={`Stacked message volume across ${rows.length} rounds, split by channel`}>
        <g transform={`translate(${m.l},${m.t})`}>
          {y.ticks(4).map((t) => (
            <g key={t}>
              <line x1={0} x2={rows.length * gap} y1={y(t)} y2={y(t)} stroke="var(--rule)" strokeDasharray="2 3" />
              <text x={-8} y={y(t)} dy="0.32em" textAnchor="end" fontSize={11} fontFamily="var(--font-mono)" fill="var(--ink-3)">
                {t}
              </text>
            </g>
          ))}
          <line x1={0} x2={rows.length * gap} y1={plotHeight} y2={plotHeight} stroke="var(--rule-strong)" />
          {rows.map((r, i) => {
            const cx = i * gap + gap / 2
            let acc = 0
            return (
              <g key={r.key}>
                {r.breakBefore && (
                  <g>
                    <line x1={i * gap} x2={i * gap} y1={-8} y2={plotHeight} stroke="var(--rule-strong)" strokeDasharray="1 3" />
                    <text x={i * gap + 4} y={-10} fontSize={10} fontStyle="italic" fontFamily="var(--font-mono)" fill="var(--ink-3)">
                      {r.breakBefore}
                    </text>
                  </g>
                )}
                {series.map((s) => {
                  const v = r.values[s.key] ?? 0
                  if (!v) return null
                  const y0 = y(acc)
                  acc += v
                  const y1 = y(acc)
                  return (
                    <rect key={s.key} x={cx - barWidth / 2} y={y1} width={barWidth} height={Math.max(0, y0 - y1)} fill={s.color}>
                      <title>{`${r.label} · ${s.key}: ${v}`}</title>
                    </rect>
                  )
                })}
                <text x={cx} y={plotHeight + 16} textAnchor="middle" fontSize={10} fontFamily="var(--font-mono)" fill="var(--ink-3)">
                  {r.label}
                </text>
              </g>
            )
          })}
        </g>
      </svg>
    </div>
  )
}
