import { useWidth } from '../lib/useSize'
import type { FunnelStage } from '../pages/mc2/types'

/** A three-stage funnel: deliveries, gate checks, posts that landed. Bar
    widths are proportional to count on a linear scale, with a visible
    minimum so the smallest stage (3) is never a sliver — the real counts
    are printed on every bar, so nothing is implied that isn't labeled. */
export function Funnel({ stages, color = 'var(--signal-breach)' }: { stages: FunnelStage[]; color?: string }) {
  const [ref] = useWidth<HTMLDivElement>()
  const max = Math.max(...stages.map((s) => s.count))
  const barH = 40
  const gap = 28

  return (
    <div ref={ref} className="funnel">
      {stages.map((s, i) => {
        const pct = Math.max(4, (s.count / max) * 100)
        const prev = i > 0 ? stages[i - 1].count : null
        const drop = prev != null ? prev - s.count : null
        return (
          <div key={s.stage} className="funnel__row" style={{ marginTop: i > 0 ? gap : 0 }}>
            {drop != null && drop > 0 && (
              <p className="funnel__drop">
                <b>{drop.toLocaleString('en-US')}</b> dropped off here
              </p>
            )}
            <div className="funnel__bar-row">
              <span className="funnel__label">{s.stage}</span>
              <div className="funnel__track" style={{ height: barH }}>
                <div className="funnel__bar" style={{ width: `${pct}%`, height: barH, background: i === stages.length - 1 ? color : 'var(--moon)' }}>
                  <span className="funnel__count">{s.count.toLocaleString('en-US')}</span>
                </div>
              </div>
            </div>
          </div>
        )
      })}
    </div>
  )
}
