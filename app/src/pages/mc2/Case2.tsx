import { Figure, DataTable, LegendItem } from '../../components/Figure'
import { Interleave } from '../../charts'
import type { MC2Data, Worm } from './types'
import { WORM_ORDER, fmtUtc, nice } from './types'

function Arrow({ label, dashed }: { label: string; dashed?: boolean }) {
  return (
    <div className="mc2-prov__arrow" data-dashed={dashed}>
      <svg width={30} height={14} aria-hidden>
        <line x1={0} y1={7} x2={22} y2={7} stroke="var(--ink-3)" strokeWidth={1.5} strokeDasharray={dashed ? '3 3' : undefined} />
        <path d="M18,3 L24,7 L18,11" fill="none" stroke="var(--ink-3)" strokeWidth={1.5} />
      </svg>
      <span className="lbl">{label}</span>
    </div>
  )
}

function ProvCard({ title, detail, variant }: { title: string; detail: string; variant?: 'missing' | 'unknown' }) {
  return (
    <div className={`mc2-prov__card${variant ? ` ${variant}` : ''}`}>
      <div className="t">{title}</div>
      <div className="d">{detail}</div>
    </div>
  )
}

function ProvenanceRow({ w }: { w: Worm }) {
  const o = w.origin
  return (
    <div className="mc2-prov__row">
      <div className="mc2-prov__name">
        <span className="dot" style={{ background: `var(--${w.series})` }} />
        {w.name}
      </div>
      <div className="mc2-prov__chain">
        {o ? (
          <>
            <ProvCard title="Internal document" detail={`${o.readTarget} · read by ${nice(o.actor)}`} />
            <Arrow label="+1s, creates" />
            <ProvCard title={o.createTarget} detail={`${o.sizeHint.toLocaleString('en-US')} bytes`} />
          </>
        ) : (
          <>
            <ProvCard title="Internal document" detail="not in log" variant="missing" />
            <Arrow label="unlogged" dashed />
            <ProvCard title={`${w.name}.txt`} detail="creation not logged" variant="missing" />
          </>
        )}
        <Arrow label={`${w.nHops} deliveries`} />
        <ProvCard title="Instructions file" detail={`propagated to ${w.nAgents} agents`} />
        <Arrow label="final hop" />
        <ProvCard title={`Post #${w.postEvent}`} detail={fmtUtc(w.postUtc)} />
        <Arrow label="deleted, +1–2s" dashed />
        <ProvCard title="Payload text" detail="not recoverable" variant="unknown" />
      </div>
    </div>
  )
}

export function Case2({ d }: { d: MC2Data }) {
  const mo = d.worms.MellowOtter

  return (
    <section className="mc2-case" id="q2">
      <div className="mc2-case__head">
        <span className="mc2-case__num">02</span>
        <h2>What the posts mean</h2>
      </div>
      <p className="mc2-case__q">
        “What do the posts mean? What is the origin of their contents? Illustrate the reasoning behind your assertion of their meaning as well as the
        probable content.”
      </p>

      <div className="mc2-prose">
        <p>
          All three anomalous events — {WORM_ORDER.map((w, i) => (
            <span key={w}>
              {i > 0 && ', '}
              <span className="ev">{d.worms[w].postEvent}</span> ({w})
            </span>
          ))}{' '}
          — share one trait: no <span className="ev">content</span> field, only <span className="ev">content_source</span> naming a .txt file. None of
          those files, or the text they held, survive in the log; John Windward&rsquo;s agent deletes them one to two seconds after posting. So the honest
          answer to &ldquo;what do the posts say&rdquo; is: <b>we don&rsquo;t know, and can&rsquo;t recover it.</b>
        </p>
        <p>
          What the log does show is how each payload was built. Twice — {nice(d.worms.SwiftWren.origin!.actor)} and {nice(mo.origin!.actor)}, both at
          15:02:00–01 local-to-the-log time — an agent reads an internal company document and, one second later, writes a same-order-of-magnitude text file
          under the worm&rsquo;s name. That one-second read-then-write pattern is the strongest evidence for probable content: some transformation of that
          internal document, not arbitrary noise. HiddenOrca&rsquo;s own origin was never logged, so its payload&rsquo;s source is unconfirmed by this
          method.
        </p>
        <p>
          It is not the farm-themed &ldquo;virus&rdquo; loop running in parallel ({d.meta.virusEvents.toLocaleString('en-US')} events,{' '}
          {fmtUtc(d.meta.virusSpanStart)} – {fmtUtc(d.meta.virusSpanEnd)}): that loop&rsquo;s own files are created and deleted independently of the worm —
          one such cycle runs within the very same second as the MellowOtter post. The two mechanisms coexist in the log; only one of them posts, and no
          farm vocabulary appears in any of the {d.meta.inlinePosts} posts we can actually read.
        </p>
      </div>

      <Figure
        id="fig-provenance"
        title="Where each payload came from — logged vs. not"
        caption={
          <>
            Solid links are events present in the log; dashed means the step, or the node at its end, is <b>not</b> recoverable. HiddenOrca&rsquo;s origin
            document was never logged at all — only its propagation was. Every worm&rsquo;s payload text is unknown, by design of this figure.
          </>
        }
      >
        <div className="mc2-prov">
          {WORM_ORDER.map((w) => (
            <ProvenanceRow key={w} w={d.worms[w]} />
          ))}
        </div>
      </Figure>

      <Figure
        id="fig-evidence"
        title="The one shape only the anomalies have"
        caption={<>Source: <code>report_full.json</code> (post-shape counts) and <code>plans/mc2_plan.md</code> (post-type split). This table is the basis for the Case 3b intervention.</>}
      >
        <DataTable
          spec={{
            columns: ['', 'Legitimate posts', 'Anomalous posts'],
            rows: [
              ['Count', d.postShape.legit.count, d.postShape.anomalous.count],
              ['Party', 'Agent (105) or person (105)', 'Agent (3/3)'],
              ['content field present', `Yes (${d.postShape.legit.count}/${d.postShape.legit.count})`, `No (0/${d.postShape.anomalous.count})`],
              ['content_source field present', `No (0/${d.postShape.legit.count})`, `Yes (${d.postShape.anomalous.count}/${d.postShape.anomalous.count})`],
              ['Farm vocabulary found', 'No', 'Unknown — text unrecoverable'],
            ],
          }}
        />
      </Figure>

      <Figure
        id="fig-interleave"
        title={`Two mechanisms, one second, ${fmtUtc(d.virusInterleave[0].utc)}`}
        legend={
          <>
            <LegendItem color="var(--series-2)">MellowOtter mechanism</LegendItem>
            <LegendItem color="var(--ink-3)">Farm virus loop</LegendItem>
            <LegendItem color="var(--signal-breach)" shape="line">
              The post
            </LegendItem>
          </>
        }
        caption={
          <>
            MellowOtter&rsquo;s post (<code>{mo.postEvent}</code>) lands in the same second the unrelated virus loop creates and deletes a file on a
            different agent. Interleaved in time, unconnected in mechanism.
          </>
        }
      >
        <Interleave events={d.virusInterleave} wormLabel="MellowOtter mechanism" />
      </Figure>
    </section>
  )
}
