import { useState } from 'react'
import { Figure } from '../../components/Figure'
import { BurstTimeline, DayStrip, DeptMap } from '../../charts'
import type { MC2Data, WormName } from './types'
import { WORM_ORDER, fmtUtc, nice } from './types'

const JW_KIND_LABEL: Record<string, string> = {
  receive: 'received',
  forward: 'forwarded onward',
  self: 'self-loop',
}

export function Case1({ d }: { d: MC2Data }) {
  const sw = d.worms.SwiftWren
  const [showGate, setShowGate] = useState(false)
  const [orgWorm, setOrgWorm] = useState<WormName>('SwiftWren')
  const exposures = d.jwTimeline.filter((e) => e.kind === 'receive' || e.kind === 'self' || e.kind === 'forward')
  const burst = d.jwTimeline.filter((e) => e.id >= sw.chain[sw.chain.length - 1].id)
  const orgData = d.worms[orgWorm]

  return (
    <section className="mc2-case" id="q1">
      <div className="mc2-case__head">
        <span className="mc2-case__num">01</span>
        <h2>How the post was made</h2>
      </div>
      <p className="mc2-case__q">
        “How was the anomalous SaidIt post made? Build a visual tool that describes the sequence of events that led up to the post. Include people and
        system interactions that were important to the post being made.”
      </p>

      <article className="mc2-subcase" id="q1a">
        <h3>
          <span className="tag">1a</span>The exact chain
        </h3>
        <div className="mc2-prose">
          <p>
            The post that reached SaidIt at <span className="ev">{sw.postUtc} UTC</span> (04:21 local) is event <span className="ev">{sw.postEvent}</span> —
            Agent/person:john_windward posting to <span className="ev">system:saidit</span> with <span className="ev">{`{forum: "general", content_source: "${sw.postPayload}"}`}</span> and
            no <span className="ev">content</span> field. Nothing John Windward did produced it; his agent published it two seconds after an incoming
            instruction file.
          </p>
          <p>
            The chain starts eight days earlier. At {fmtUtc(sw.origin!.createUtc)}, {nice(sw.origin!.actor)}&rsquo;s agent reads{' '}
            <span className="ev">{sw.origin!.readTarget}</span>, creates <span className="ev">{sw.origin!.createTarget}</span> (
            <span className="ev">{sw.origin!.sizeHint.toLocaleString('en-US')} bytes</span>), then queues the first of <b>{sw.nHops}</b> agent-to-agent
            deliveries that pass across <b>{sw.nAgents}</b> agents over the next eight days — {sw.perDay[Object.keys(sw.perDay)[0]]} hops on day one, peaking
            at {Math.max(...Object.values(sw.perDay))} on {Object.entries(sw.perDay).find(([, v]) => v === Math.max(...Object.values(sw.perDay)))?.[0].slice(5)}, down to{' '}
            {sw.perDay[Object.keys(sw.perDay)[Object.keys(sw.perDay).length - 1]]} on the day of the post.
          </p>
          <p>
            John Windward&rsquo;s agent is not a first-time recipient. It receives the same instruction file four times before this one, and forwards it
            onward three of those times. None of those earlier deliveries triggers anything. The fifth delivery — from chloe_ballast, two seconds before the
            post — is the one that does.
          </p>
        </div>

        <Figure
          id="fig-daystrip"
          title={`Eight days, ${sw.nHops} hops — the SwiftWren chain, collapsed to one bar per day`}
          caption={
            <>
              Source: <code>worm_events.csv</code> → SwiftWren <code>queue_subordinate_task</code> rows. Drag the slider or click a day; the list shows the
              real deliveries logged that day.
            </>
          }
        >
          <DayStrip perDay={sw.perDay} chain={sw.chain} color={`var(--${sw.series})`} />
        </Figure>

        <Figure id="fig-exposure" title="John Windward's agent, five exposures over seven days" caption={<>Source: <code>worm_events.csv</code>, filtered to events naming john_windward as actor or target.</>}>
          <ol className="mc2-exposure">
            {exposures.map((e) => (
              <li key={e.id} className="mc2-exposure__row">
                <span className="t">{fmtUtc(e.utc)}</span>
                <span className="desc">
                  <b>{nice(e.from ?? '')}</b> → <b>{nice(e.to ?? e.from ?? '')}</b> ({JW_KIND_LABEL[e.kind] ?? e.kind})
                </span>
                {e.id === sw.chain[sw.chain.length - 1].id ? (
                  <span className="chip chip--breach">
                    <span className="dot" />
                    <span className="label">triggers the post</span>
                  </span>
                ) : e.kind === 'forward' ? (
                  <span className="chip chip--watch">
                    <span className="dot" />
                    <span className="label">forwarded, no effect</span>
                  </span>
                ) : (
                  <span className="chip chip--baseline">
                    <span className="dot" />
                    <span className="label">no effect</span>
                  </span>
                )}
              </li>
            ))}
          </ol>
        </Figure>

        <Figure
          id="fig-burst"
          title={`The final two seconds — events ${burst[0]?.id} to ${burst[burst.length - 1]?.id}`}
          controls={
            <button type="button" className="chip" aria-pressed={showGate} onClick={() => setShowGate((v) => !v)}>
              {showGate ? 'Hide' : 'Show'} proposed gate (Case 3b)
            </button>
          }
          caption={
            <>
              The payload and its instruction file delete themselves within three seconds of the post (<code>{sw.deletes[0]?.id}</code>,{' '}
              <code>{sw.deletes[1]?.id}</code>), erasing the only record of what <code>{sw.postPayload}</code> said.
            </>
          }
        >
          <BurstTimeline events={burst} showGate={showGate} />
        </Figure>
      </article>

      <article className="mc2-subcase" id="q1b">
        <h3>
          <span className="tag">1b</span>The system it moved through
        </h3>
        <div className="mc2-prose">
          <p>
            Zoom out from the {sw.nHops}-hop thread to where it sits in the company. Tenant Thread&rsquo;s org chart has {d.meta.orgNodes} nodes — one
            company, {d.meta.orgCounts.department} departments, {d.meta.orgCounts.team} teams, {d.meta.orgCounts.person} people — connected mostly by{' '}
            <span className="ev">contains</span> edges, plus five <span className="ev">led_by</span> edges naming department heads.
          </p>
          <p>
            Of the {sw.nAgents} agents SwiftWren passed through, all {d.org.deptHeadcount['Information Technologies']} of IT&rsquo;s people carried it, along
            with {sw.carrierDepts.Products ?? 0} of {d.org.deptHeadcount.Products} in Products and {sw.carrierDepts['Executive Suite'] ?? 0} of{' '}
            {d.org.deptHeadcount['Executive Suite']} in Executive Suite, where the file originated. Traffic stays heaviest inside IT and Products.
            Customer Support — {d.org.deptHeadcount['Customer Support']} people, not the usual correspondents of software agents — is touched exactly once,
            on the final hop, when chloe_ballast&rsquo;s IT agent reaches john_windward.
          </p>
          <p>
            The earlier worms show the same shape: HiddenOrca ({d.worms.HiddenOrca.nAgents} agents, all also SwiftWren carriers) and MellowOtter (
            {d.worms.MellowOtter.nAgents} agents, 10 shared with SwiftWren) both cross IT and Products for most of their length and reach Customer Support
            only at the post. Department boundaries slowed nothing; John Windward is simply the one carrier whose role is public-facing, so his agent is the
            one that publishes.
          </p>
        </div>

        <Figure
          id="fig-orgmap"
          title="Carrier departments vs. the terminal node"
          controls={
            <div className="mc2-toggle-row" role="group" aria-label="Choose worm">
              {WORM_ORDER.map((w) => (
                <button key={w} type="button" className="chip" aria-pressed={orgWorm === w} onClick={() => setOrgWorm(w)}>
                  {w}
                </button>
              ))}
            </div>
          }
          caption={
            <>
              Boxes show carriers touched / total people in that department, for {orgWorm}. Edge thickness is hop count between departments, on one shared
              scale across all three worms. Customer Support is ringed — the only customer-facing department in the path, and where every worm&rsquo;s post
              happens.
            </>
          }
        >
          <DeptMap
            deptOrder={d.org.deptOrder}
            headcount={d.org.deptHeadcount}
            carriers={orgData.carrierDepts}
            flow={orgData.deptFlow}
            maxFlow={d.org.maxDeptFlow}
            color={`var(--${orgData.series})`}
          />
        </Figure>
      </article>
    </section>
  )
}
