import { useState, type ReactNode } from 'react'
import './Figure.css'

export interface TableSpec {
  columns: string[]
  rows: (string | number | null)[][]
}

/** Every chart lives in a Figure: a title that states the finding, the plot,
    an optional legend, a caption with the source, and a "show table" toggle
    over the same data. */
export function Figure({
  title,
  subtitle,
  legend,
  caption,
  table,
  controls,
  children,
  id,
}: {
  title: ReactNode
  subtitle?: ReactNode
  legend?: ReactNode
  caption?: ReactNode
  table?: TableSpec
  controls?: ReactNode
  children: ReactNode
  id?: string
}) {
  const [asTable, setAsTable] = useState(false)
  return (
    <figure className="fig" id={id}>
      <header className="fig__head">
        <div>
          <h4 className="fig__title">{title}</h4>
          {subtitle && <p className="fig__sub">{subtitle}</p>}
        </div>
        {table && (
          <button type="button" className="chip" aria-pressed={asTable} onClick={() => setAsTable((v) => !v)}>
            {asTable ? 'Show chart' : 'Show table'}
          </button>
        )}
      </header>
      {controls && <div className="fig__controls">{controls}</div>}
      {legend && !asTable && <div className="fig__legend">{legend}</div>}
      <div className="fig__body">{asTable && table ? <DataTable spec={table} /> : children}</div>
      {caption && <figcaption className="fig__cap">{caption}</figcaption>}
    </figure>
  )
}

export function DataTable({ spec, max = 60 }: { spec: TableSpec; max?: number }) {
  return (
    <div className="table-wrap">
      <table className="data-table">
        <thead>
          <tr>
            {spec.columns.map((c) => (
              <th key={c} scope="col">
                {c}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {spec.rows.slice(0, max).map((r, i) => (
            <tr key={i}>
              {r.map((v, j) => (
                <td key={j} className={typeof v === 'number' ? 'num' : undefined}>
                  {v === null ? '—' : v}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
      {spec.rows.length > max && (
        <p className="table-more">
          Showing {max} of {spec.rows.length.toLocaleString('en-US')} rows.
        </p>
      )}
    </div>
  )
}

export function LegendItem({ color, children, shape }: { color: string; children: ReactNode; shape?: 'line' | 'square' | 'circle' | 'outline' }) {
  return (
    <span className="legend-item">
      <span className={`legend-swatch legend-swatch--${shape ?? 'square'}`} style={shape === 'outline' ? { borderColor: color } : { background: color }} aria-hidden />
      {children}
    </span>
  )
}
