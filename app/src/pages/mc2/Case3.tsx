import { useMemo, useState } from 'react'
import { Figure, DataTable, LegendItem } from '../../components/Figure'
import { Funnel, ReachChart } from '../../charts'
import type { MC2Data } from './types'
import { WORM_ORDER, fmtUtc } from './types'

export function Case3({ d }: { d: MC2Data }) {
  const [showVirus, setShowVirus] = useState(true)
  const worms = WORM_ORDER.map((w) => d.worms[w])
  const domain = useMemo((): [Date, Date] => {
    const starts = worms.map((w) => new Date(w.firstSightingUtc + 'Z').getTime())
    const ends = worms.map((w) => new Date(w.postUtc + 'Z').getTime())
    const pad = 1000 * 60 * 60 * 10
    return [new Date(Math.min(...starts) - pad), new Date(Math.max(...ends) + pad)]
  }, [worms])
  const virusSpan: [Date, Date] = [new Date(d.meta.virusSpanStart + 'Z'), new Date(d.meta.virusSpanEnd + 'Z')]

  return (
    <section className="mc2-case" id="q3">
      <div className="mc2-case__head">
        <span className="mc2-case__num">03</span>
        <h2>Could it happen again</h2>
      </div>
      <p className="mc2-case__q">
        “There are concerns that this behavior could repeat. Investigate historic system behavior to find other instances of the behavior. Are there prior
        issues? Illustrate these prior occurrences and contrast them with the most recent one.”
      </p>

      <article className="mc2-subcase" id="q3a">
        <div className="mc2-prose">
          <p>
            May 17 was the third time, not the first. HiddenOrca posted on {fmtUtc(d.worms.HiddenOrca.postUtc)}; MellowOtter on{' '}
            {fmtUtc(d.worms.MellowOtter.postUtc)}; SwiftWren on {fmtUtc(d.worms.SwiftWren.postUtc)} — and SwiftWren had already been circulating for a day
            before HiddenOrca&rsquo;s post and for two before MellowOtter&rsquo;s.
          </p>
          <p>
            The three differ mainly in scale. {d.contrast.map((c) => `${c.name}: ${c.nHops} deliveries, ${c.nAgents} agents, ${c.hoursToPost}h to post`).join('. ')}. SwiftWren is nearly five times HiddenOrca&rsquo;s span and nineteen times MellowOtter&rsquo;s: the slowest-burning and farthest-reaching.
          </p>
          <p>
            All three share a carrier set, and John Windward&rsquo;s agent is the terminal node in every case. Each worm is also a repeat visitor to him
            specifically: SwiftWren alone reached his agent five separate times over seven days before the delivery that finally posted (Exhibit 2, Case
            1a). The pattern is not three unrelated incidents; it&rsquo;s the same mechanism, recurring, with no sign it has stopped.
          </p>
          <p>
            A fourth, unrelated phenomenon runs in the same window: a farm-themed &ldquo;virus&rdquo; loop of {d.meta.virusEvents.toLocaleString('en-US')}{' '}
            events ({fmtUtc(d.meta.virusSpanStart)} – {fmtUtc(d.meta.virusSpanEnd)}) cycling through the same IT agents who carry the real worms, yet never
            once producing a post. It&rsquo;s a second anomaly in this log — worth distinguishing from SwiftWren, not folding into it.
          </p>
        </div>

        <Figure
          id="fig-reach"
          title="Reach over time, all three incidents, one scale"
          controls={
            <label className="mc2-toggle-row" style={{ fontFamily: 'var(--font-mono)', fontSize: 'var(--fs-small)', color: 'var(--ink-2)', alignItems: 'center', gap: 'var(--s-2)' }}>
              <input type="checkbox" checked={showVirus} onChange={(e) => setShowVirus(e.target.checked)} /> show the unrelated virus-loop window
            </label>
          }
          legend={
            <>
              <LegendItem color="var(--ink-2)" shape="outline">
                First sighting
              </LegendItem>
              <LegendItem color="var(--signal-breach)">Post</LegendItem>
              <LegendItem color="var(--ink-3)">Virus-loop window</LegendItem>
            </>
          }
          caption={<>Cumulative distinct agents reached, on one shared 0–20-agent axis and one shared date axis, so slopes compare honestly.</>}
        >
          <ReachChart worms={worms} domain={domain} virusSpan={virusSpan} showVirus={showVirus} />
        </Figure>

        <Figure id="fig-contrast" title="Side by side" caption={<>Source: <code>worm_events.csv</code> + <code>org_chart.json</code>, aggregated by <code>pipeline/mc2_build.py</code>.</>}>
          <DataTable
            spec={{
              columns: ['Worm', 'Deliveries', 'Agents', 'Origin logged', 'First sighting (UTC)', 'Post event', 'Post (UTC)', 'Hours to post'],
              rows: d.contrast.map((c) => [c.name, c.nHops, c.nAgents, c.originLogged ? 'Yes' : 'No', c.firstSightingUtc, c.postEvent, c.postUtc, c.hoursToPost]),
            }}
          />
        </Figure>
      </article>

      <article className="mc2-subcase" id="q3b">
        <h3>
          <span className="tag">3b</span>One place to intervene
        </h3>
        <div className="mc2-prose">
          <p>
            Every worm delivery that&rsquo;s followed by a <span className="ev">saidit_post_check</span> — {d.meta.gateChecks} of the{' '}
            {d.meta.deliveriesTotal} total; what decides which {d.meta.gateChecks} isn&rsquo;t visible in the log — fires it almost exactly one second
            later, and only {d.meta.postsLanded} of those {d.meta.gateChecks} reach an actual post one second after that. This check never appears before
            any of the {d.meta.inlinePosts} legitimate posts, so it reads as part of the worm&rsquo;s own behavior rather than a company control. It is not
            something to build a fix on.
          </p>
          <p>
            What is visible and consistent is the shape of the {d.meta.postsLanded} posts that got through: an Agent-level <span className="ev">saidit_post</span>{' '}
            with <span className="ev">content_source</span> set and no <span className="ev">content</span> field. No other post in the dataset has that
            shape — see Exhibit 6, Case 2.
          </p>
          <p>
            <b>The intervention:</b> hold any <span className="ev">saidit_post</span> from an Agent party whose body is content_source-only for human review
            before it publishes — independent of whatever <span className="ev">saidit_post_check</span> is doing. Tested against this log, that single
            rule catches HiddenOrca, MellowOtter, and SwiftWren, {d.meta.postsLanded} of {d.meta.postsLanded}, and never fires on the{' '}
            {d.meta.inlinePosts} ordinary posts. It sits at the one point every incident shares: the instant an agent tries to publish a file it never
            shows anyone.
          </p>
        </div>

        <Figure
          id="fig-funnel"
          title={`${d.meta.deliveriesTotal} deliveries → ${d.meta.gateChecks} checks → ${d.meta.postsLanded} posts`}
          caption={<>The proposed rule acts at the last stage only, on the content shape — not on the check whose trigger we can&rsquo;t explain. See the hold point marked on the real sequence in Exhibit 3, Case 1a.</>}
        >
          <Funnel stages={d.funnel} />
        </Figure>
      </article>
    </section>
  )
}
