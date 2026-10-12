import { useWidth } from '../lib/useSize'
import type { DeptFlowEdge } from '../pages/mc2/types'

const SHORT: Record<string, string> = {
  'Executive Suite': 'Executive Suite',
  'Information Technologies': 'Information Technologies',
  Products: 'Products',
  'Human Resources': 'Human Resources',
  Legal: 'Legal',
  'Customer Support': 'Customer Support',
}

/** Department box positions, laid out loosely like the org chart: the
    origin department at top, the heavy IT/Products traffic in the middle,
    the terminal customer-facing department ringed at the bottom. */
const POS: Record<string, { x: number; y: number }> = {
  'Executive Suite': { x: 400, y: 54 },
  'Information Technologies': { x: 200, y: 170 },
  Products: { x: 600, y: 170 },
  'Human Resources': { x: 140, y: 290 },
  Legal: { x: 660, y: 290 },
  'Customer Support': { x: 400, y: 372 },
}
const BOX_W = 168
const BOX_H = 58

/** Department-level view of the org chart: boxes sized by headcount,
    carriers-touched shown as a meter, cross-department hops drawn as edges
    whose thickness is on one shared scale across all three worms, so the
    comparison between incidents is honest. Customer Support is ringed — the
    only customer-facing department in any worm's path, and where every
    worm's post happens. */
export function DeptMap({
  deptOrder,
  headcount,
  carriers,
  flow,
  maxFlow,
  color,
}: {
  deptOrder: string[]
  headcount: Record<string, number>
  carriers: Record<string, number>
  flow: DeptFlowEdge[]
  maxFlow: number
  color: string
}) {
  const [ref, width] = useWidth<HTMLDivElement>()
  const vbW = 800
  const vbH = 420
  const scale = Math.min(1, width / vbW)
  const height = vbH * scale

  const cross = flow.filter((e) => e.from !== e.to && POS[e.from] && POS[e.to])
  const selfLoops = flow.filter((e) => e.from === e.to)
  const selfCount = (dept: string) => selfLoops.find((e) => e.from === dept)?.count ?? 0

  return (
    <div ref={ref} style={{ overflowX: 'auto' }}>
      <svg
        className="chart"
        width={Math.max(width, 480)}
        height={Math.max(height, 480 * (vbH / vbW))}
        viewBox={`0 0 ${vbW} ${vbH}`}
        role="img"
        aria-label="Department-level view of the org chart, with carriers touched and hop traffic between departments"
      >
        <g>
          {cross.map((e, i) => {
            const a = POS[e.from]
            const b = POS[e.to]
            const w = Math.max(1, (e.count / maxFlow) * 11)
            return (
              <line
                key={i}
                x1={a.x}
                y1={a.y}
                x2={b.x}
                y2={b.y}
                stroke={color}
                strokeOpacity={0.55}
                strokeWidth={w}
                strokeLinecap="round"
              >
                <title>{`${e.from} → ${e.to}: ${e.count} hop${e.count > 1 ? 's' : ''}`}</title>
              </line>
            )
          })}
          {deptOrder.map((dept) => {
            const p = POS[dept]
            if (!p) return null
            const total = headcount[dept] ?? 0
            const touched = carriers[dept] ?? 0
            const terminal = dept === 'Customer Support'
            const meterW = BOX_W - 20
            const meterFill = total > 0 ? (touched / total) * meterW : 0
            const loop = selfCount(dept)
            return (
              <g key={dept} transform={`translate(${p.x - BOX_W / 2},${p.y - BOX_H / 2})`}>
                <rect
                  width={BOX_W}
                  height={BOX_H}
                  rx={10}
                  fill="var(--swell)"
                  stroke={terminal ? 'var(--signal-breach)' : 'var(--rule)'}
                  strokeWidth={terminal ? 2.5 : 1.5}
                />
                <text x={10} y={20} fontSize={12.5} fontWeight={700} fill="var(--ink)" fontFamily="var(--font-display)">
                  {SHORT[dept] ?? dept}
                </text>
                <text x={10} y={36} fontSize={11} fill="var(--ink-2)" fontFamily="var(--font-mono)">
                  {touched} / {total} carriers{loop ? ` · ${loop} internal` : ''}
                </text>
                <rect x={10} y={44} width={meterW} height={5} rx={2.5} fill="var(--rule)" />
                <rect x={10} y={44} width={Math.max(0, meterFill)} height={5} rx={2.5} fill={touched > 0 ? color : 'var(--rule)'} />
                {terminal && (
                  <text x={BOX_W - 10} y={20} textAnchor="end" fontSize={9.5} fontWeight={700} letterSpacing="0.04em" fill="var(--signal-breach)" fontFamily="var(--font-display)">
                    TERMINAL
                  </text>
                )}
              </g>
            )
          })}
        </g>
      </svg>
    </div>
  )
}
