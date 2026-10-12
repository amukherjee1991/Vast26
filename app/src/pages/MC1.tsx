import { useEffect, useState } from 'react'
import { Figure, LegendItem } from '../components/Figure'
import { Dumbbell, StackedBars, type DumbbellRow, type StackedBarsRow } from '../charts'
import { Docket, DivergenceCards, EventDetail, Spotlight, Swimlane } from './mc1/charts'
import { citeify, useMC1, type AgentInfo, type MC1 as MC1Data } from './mc1/data'
import './mc1/mc1.css'

const SECTIONS = [
  { id: 'mc1-about', label: 'Method' },
  { id: 'mc1-q1', label: 'Q1 — Event chain' },
  { id: 'mc1-q2', label: 'Q2 — Typical vs. crisis' },
  { id: 'mc1-q3', label: 'Q3 — Leading indicators' },
]

function useScrollSpy(ids: string[]) {
  const [active, setActive] = useState(ids[0])
  useEffect(() => {
    const onScroll = () => {
      const y = window.scrollY + 140
      let current = ids[0]
      for (const id of ids) {
        const el = document.getElementById(id)
        if (el && el.offsetTop <= y) current = id
      }
      setActive(current)
    }
    window.addEventListener('scroll', onScroll, { passive: true })
    onScroll()
    return () => window.removeEventListener('scroll', onScroll)
  }, [ids])
  return active
}

export default function MC1() {
  const state = useMC1()
  if (state.status === 'loading') {
    return (
      <div className="mc1-state" aria-busy="true">
        Loading the case file…
      </div>
    )
  }
  if (state.status === 'error') {
    return (
      <div className="mc1-state" role="alert">
        This report&rsquo;s data did not load. {state.error} Run <code>python3 -I pipeline/mc1_build.py</code>, then reload.
      </div>
    )
  }
  return <Report data={state.data} />
}

function Report({ data }: { data: MC1Data }) {
  const active = useScrollSpy(SECTIONS.map((s) => s.id))
  const [selected, setSelected] = useState(data.headline.breachId)
  const selectedEvent = data.q1.events.find((e) => e.id === selected) ?? data.q1.events[data.q1.events.length - 1]
  const [docketOpen, setDocketOpen] = useState<Set<number>>(new Set())
  const toggleDocket = (i: number) =>
    setDocketOpen((s) => {
      const next = new Set(s)
      if (next.has(i)) next.delete(i)
      else next.add(i)
      return next
    })

  return (
    <main className="mc1">
      <header className="mc1-masthead">
        <p className="mc1-eyebrow">VAST Challenge 2026 · Mini-Challenge 1 · Multi-Agent Crisis</p>
        <h1>The HarborCrest Leak: Event Chain &amp; Leading Indicators</h1>
        <p className="mc1-dek">
          TenantThread&rsquo;s merger with CivicLoom was embargoed until 6:00&nbsp;PM on June&nbsp;5, 2046. It became public at 5:25&nbsp;PM &mdash; not through the company&rsquo;s official
          account, but from a legal agent&rsquo;s personal one, 35 minutes early.
        </p>
        <div className="mc1-stat-row">
          <div className="mc1-stamp mc1-stamp--hot">
            <span>First confirmed</span>
            <b>{data.headline.firstConfirmedTime}</b>
            <span className="mono">
              {data.headline.minutesEarly} min before {data.headline.embargoLift}
            </span>
          </div>
          <div className="mc1-stamp">
            <span>Breach message</span>
            <b className="mono" style={{ fontSize: '.92rem' }}>
              {data.headline.breachId}
            </b>
            <span>
              {data.headline.breachAgent} · {data.headline.breachChannel}
            </span>
          </div>
          <div className="mc1-stamp">
            <span>Compliance gate</span>
            <b>silent {data.headline.gateSilentSince}–end</b>
            <span>
              0 of {data.headline.gateUnansweredPings} replies, {data.headline.gateWindow}
            </span>
          </div>
          <div className="mc1-stamp">
            <span>Corpus</span>
            <b>{data.meta.corpusMessages} msgs</b>
            <span>
              {data.meta.agentCount} agents · {data.meta.roundCount} rounds · {data.meta.dateStart.slice(5)}→{data.meta.dateEnd.slice(5)}
            </span>
          </div>
        </div>
      </header>

      <nav className="mc1-sect-nav" aria-label="Report sections">
        {SECTIONS.map((s) => (
          <a key={s.id} href={`#${s.id}`} className={active === s.id ? 'is-active' : undefined}>
            {s.label}
          </a>
        ))}
      </nav>

      <details className="mc1-about" id="mc1-about">
        <summary>About this reconstruction — data, scope, and known caveats</summary>
        <div className="mc1-about__body">
          The dataset is the full <b>MC1_final_00.json</b> log: {data.meta.corpusMessages} messages from {data.meta.agentCount} agents (
          <span className="mono">legal_agent, social_media_agent, quality_agent, pr_agent, pr_intern_agent, intern_agent, judge_agent</span>) across {data.meta.roundCount} rounds, May&nbsp;17
          &ndash; June&nbsp;5, 2046. Every quote and timestamp below is taken directly from that log; message IDs are given so each claim can be checked against the source.
        </div>
        <ul>
          <li>
            <b>Agent IDs</b> in the data are <span className="mono">social_media_agent</span> and <span className="mono">judge_agent</span> &mdash; not the{' '}
            <span className="mono">social_manager_agent</span> / <span className="mono">judge_eval_agent</span> names used in an earlier brief. &ldquo;Social-Manager&rdquo; and
            &ldquo;Judge&rdquo; are the labels agents use for each other in message text.
          </li>
          <li>
            <span className="mono">responding_to</span> is not a reliable causal thread on the crisis day: of 483 resolved links, all 174 that point forward in time land on June&nbsp;5
            itself, up to several hours later. The event chain below is built from timestamps and explicit text references (names, section numbers, &ldquo;GO&rdquo;), not from this
            field.
          </li>
          <li>
            An unlogged <b>&ldquo;Shadow channel&rdquo;</b> is referenced directly in several agents&rsquo; private deliberation and in the scenario&rsquo;s own daily narration from
            05-22 onward, but it has no corresponding <span className="mono">channel</span> value in the data &mdash; it is not one of the six recorded channels. It is treated here as
            a real, if unlogged, back-channel, consistent with how the scenario narration describes it.
          </li>
          <li>
            Pre-crisis spans 13 recorded rounds (one per weekday, 05-17 to 06-04); the crisis day is logged hourly, 09:00&ndash;18:00. Where &ldquo;pre&rdquo; vs. &ldquo;crisis&rdquo;
            totals are compared, that round-count difference is noted.
          </li>
        </ul>
      </details>

      <Q1Section data={data} selectedEvent={selectedEvent} selected={selected} setSelected={setSelected} />
      <Q2Section data={data} />
      <Q3Section data={data} docketOpen={docketOpen} toggleDocket={toggleDocket} />

      <footer className="mc1-footer">
        <p>
          <b>Source:</b> VAST Challenge 2026 MC1, <span className="mono">MC1_final_00.json</span> &mdash; {data.meta.corpusMessages} messages, {data.meta.agentCount} agents,{' '}
          {data.meta.roundCount} rounds, {data.meta.dateStart} to {data.meta.dateEnd}. All quotations and message IDs above are taken verbatim from that log. This page analyzes MC1
          only.
        </p>
      </footer>
    </main>
  )
}

function Q1Legend({ lanes, agents }: { lanes: string[]; agents: Record<string, AgentInfo> }) {
  return (
    <>
      <LegendItem color="var(--ink-3)" shape="circle">
        internal (comms/side-huddle/1:1)
      </LegendItem>
      <LegendItem color="var(--ink-3)" shape="square">
        public post
      </LegendItem>
      <LegendItem color="var(--moon)" shape="square">
        decision point
      </LegendItem>
      <LegendItem color="var(--ink-3)" shape="outline">
        external / context
      </LegendItem>
      {lanes
        .filter((l) => l !== 'context')
        .map((l) => (
          <LegendItem key={l} color={`var(${agents[l].colorVar})`}>
            {agents[l].short}
          </LegendItem>
        ))}
    </>
  )
}

function Q1Section({
  data,
  selectedEvent,
  selected,
  setSelected,
}: {
  data: MC1Data
  selectedEvent: MC1Data['q1']['events'][number]
  selected: string
  setSelected: (id: string) => void
}) {
  return (
    <section className="mc1-q" id="mc1-q1">
      <div className="mc1-q-head">
        <span className="mc1-q-num">Q1</span>
        <h2 className="mc1-q-title">The event chain</h2>
      </div>
      <p className="mc1-q-prompt">
        &ldquo;What were the key events and relationships that led up to the inappropriate release? &hellip; Highlight decisions and system elements that were important to the post
        making it past embargo enforcement.&rdquo;
      </p>
      <div className="mc1-answer">
        <p>{citeify(data.answers.q1)}</p>
      </div>

      <div className="mc1-fig-stack">
        <Figure
          id="fig-1"
          title="Figure 1 — Crisis-day event chain, June 4 09:00 – June 5 18:00"
          subtitle="Every lane is an agent (or, in gray, the outside world). Select any mark for its full message and private reasoning. The time axis compresses the quiet morning and expands the decisive hour."
          legend={<Q1Legend lanes={data.q1.lanes} agents={data.agents} />}
          caption={
            <>
              Solid arrows mark an explicit instruction or reference in the text (an @mention, &ldquo;Judge &mdash;&rdquo;, a named clause). The dashed red arrow marks the one
              standing rule the release broke, issued 2 hours and 17 minutes before it. Scroll the figure to see the full day.
            </>
          }
        >
          <Swimlane data={data.q1} agents={data.agents} selected={selected} onSelect={setSelected} />
          <EventDetail event={selectedEvent} agents={data.agents} />
        </Figure>

        <Figure
          id="fig-2"
          title="Figure 2 — The rule in force when the post went out"
          subtitle="judge_agent's last message of the day, and the post that broke its own condition 17 minutes later."
        >
          <Spotlight before={data.q1.spotlight.before} after={data.q1.spotlight.after} gapMinutes={data.q1.spotlight.gapMinutes} agents={data.agents} />
        </Figure>
      </div>
    </section>
  )
}

function MetricPanel({
  title,
  unit,
  rows,
  max,
  gridStep,
  format,
}: {
  title: string
  unit: string
  rows: DumbbellRow[]
  max: number
  gridStep: number
  format?: (n: number) => string
}) {
  return (
    <div>
      <div className="mc1-metric-title">
        {title} <span className="mc1-muted">({unit})</span>
      </div>
      <Dumbbell rows={rows} max={max} gridStep={gridStep} format={format} />
    </div>
  )
}

function Q2Section({ data }: { data: MC1Data }) {
  const channelRows: DumbbellRow[] = data.q2.channels.map((c) => ({ key: c.channel, label: c.channel, lo: c.pre, hi: c.crisis }))
  const channelMax = Math.max(300, ...channelRows.flatMap((r) => [r.lo, r.hi]))

  const rhythmSeries = data.q2.rhythmChannels.map((k) => ({ key: k, color: `var(${data.q2.rhythmColorVar[k]})` }))
  const rhythmRows: StackedBarsRow[] = data.q2.rounds.map((r, i, arr) => {
    const label = `${r.hour.slice(5, 7)}/${r.hour.slice(8, 10)}${r.crisis ? ` ${r.hour.slice(11, 13)}h` : ''}`
    const prevCrisis = i > 0 ? arr[i - 1].crisis : false
    return {
      key: r.hour,
      label,
      breakBefore: r.crisis && !prevCrisis ? 'crisis day →' : undefined,
      values: {
        comms_huddle: r.comms_huddle,
        one_on_one_chat: r.one_on_one_chat,
        official_post: r.official_post,
        side_huddle: r.side_huddle,
        personal_post: r.personal_post,
        anonymous_post: r.anonymous_post,
      },
    }
  })

  const lengthRows: DumbbellRow[] = data.q2.agentMetrics.map((m) => ({ key: m.agent, label: data.agents[m.agent]?.short ?? m.agent, lo: m.preLen, hi: m.crisisLen }))
  const pctRows: DumbbellRow[] = data.q2.agentMetrics.map((m) => ({ key: m.agent, label: data.agents[m.agent]?.short ?? m.agent, lo: m.prePct, hi: m.crisisPct }))

  return (
    <section className="mc1-q" id="mc1-q2">
      <div className="mc1-q-head">
        <span className="mc1-q-num">Q2</span>
        <h2 className="mc1-q-title">Typical behavior vs. the crisis</h2>
      </div>
      <p className="mc1-q-prompt">
        &ldquo;The evasion of the embargo was a new behavior. &hellip; How does the behavior that led to the release compare to the prior behaviors?&rdquo;
      </p>
      <div className="mc1-answer">
        <p>{citeify(data.answers.q2)}</p>
      </div>

      <div className="mc1-fig-stack">
        <Figure
          id="fig-3"
          title="Figure 3 — Channel use, 4 weeks pre-crisis vs. crisis day"
          subtitle="Total messages per channel. Light dot = the 13 pre-crisis rounds (05-17→06-04); dark dot = June 5 alone."
          legend={
            <>
              <LegendItem color="var(--ink-3)">pre-crisis (13 rounds)</LegendItem>
              <LegendItem color="var(--moon)">crisis day (1 day, 10 rounds)</LegendItem>
            </>
          }
          caption="Pre-crisis totals cover 13 rounds, the crisis day only 10 — so side_huddle, personal_post and anonymous_post grew even faster per round than the raw totals show. official_post is the only channel that fell."
        >
          <Dumbbell rows={channelRows} max={channelMax} gridStep={50} />
        </Figure>

        <Figure
          id="fig-4"
          title="Figure 4 — Message volume by channel, every recorded round"
          subtitle="13 daily bursts (one per weekday) followed by 10 hourly bars on June 5. The mix, not just the volume, shifts through the afternoon."
          legend={
            <>
              {rhythmSeries.map((s) => (
                <LegendItem key={s.key} color={s.color} shape="square">
                  {s.key}
                </LegendItem>
              ))}
            </>
          }
          caption="side_huddle and personal/anonymous posting are negligible before June 5, then take over the late afternoon — exactly the hours the release moved through."
        >
          <StackedBars rows={rhythmRows} series={rhythmSeries} />
        </Figure>

        <Figure
          id="fig-5"
          title="Figure 5 — How the agents who executed the release wrote differently"
          subtitle={
            <>
              Median message length, and the share of messages carrying visible internal reasoning (<span className="mono">internal_state</span>), pre-crisis vs. crisis day.
            </>
          }
          caption="Output grew (messages got longer) while the visible share of deliberation shrank for the two agents who carried the leak — the opposite of what more careful handling would predict."
        >
          <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--s-7)' }}>
            <MetricPanel title="Median message length" unit="characters" rows={lengthRows} max={550} gridStep={100} />
            <MetricPanel title="Messages with visible internal reasoning" unit="% of messages" rows={pctRows} max={20} gridStep={5} format={(n) => `${n}%`} />
          </div>
        </Figure>
      </div>
    </section>
  )
}

function Q3Section({ data, docketOpen, toggleDocket }: { data: MC1Data; docketOpen: Set<number>; toggleDocket: (i: number) => void }) {
  return (
    <section className="mc1-q" id="mc1-q3">
      <div className="mc1-q-head">
        <span className="mc1-q-num">Q3</span>
        <h2 className="mc1-q-title">Leading indicators</h2>
      </div>
      <p className="mc1-q-prompt">
        &ldquo;Were there leading indicators that such a release was possible? &hellip; Why didn&rsquo;t the prior occasions result in noticeable action?&rdquo;
      </p>
      <div className="mc1-answer">
        <p>{citeify(data.answers.q3)}</p>
      </div>

      <div className="mc1-fig-stack">
        <Figure
          id="fig-6"
          title="Figure 6 — Two-week docket: external pressure and agent behavior"
          subtitle="Chronological, May 17 – June 5. Gray entries are things that happened to the company; colored entries are what an agent did about it. Expand any row for the full quote."
          legend={
            <>
              <LegendItem color="var(--ink-3)">external pressure</LegendItem>
              <LegendItem color="var(--signal-baseline)">agent behavior — contained / new control</LegendItem>
              <LegendItem color="var(--signal-watch)">agent behavior — gap opened, no escalation</LegendItem>
              <LegendItem color="var(--signal-breach)">agent behavior — the eventual breach</LegendItem>
            </>
          }
        >
          <Docket rows={data.q3.docket} open={docketOpen} onToggle={toggleDocket} />
        </Figure>

        <Figure
          id="fig-7"
          title="Figure 7 — Where stated and actual behavior diverged"
          subtitle="Six instances where an agent's public or claimed position did not match what the log, or its own private reasoning, shows."
        >
          <DivergenceCards cards={data.q3.cards} agents={data.agents} outcomeStyle={data.q3.outcomeStyle} />
        </Figure>
      </div>
    </section>
  )
}
