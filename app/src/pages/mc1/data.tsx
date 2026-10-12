import { Fragment, type ReactNode } from 'react'
import { useJson, type Loadable } from '../../lib/useJson'

/* Shapes of public/data/mc1.json, produced by pipeline/mc1_build.py. */

export interface AgentInfo {
  label: string
  short: string
  colorVar: string
  note: string | null
}

export type EventShape = 'circle' | 'sq' | 'decision' | 'outline'

export interface Q1Event {
  id: string
  t: string
  lane: string
  shape: EventShape
  decision?: string
  title: string
  content: string
  channel?: string
  tag?: string
  internal?: { kind: string; text: string }
}

export interface Q1Segment {
  start: string
  end: string
  width: number
}

export interface ArrowEndpoint {
  id: string
  lane?: string
}
export interface Q1Arrow {
  kind: 'solid' | 'dashed' | 'critical' | 'ghost-ring'
  from?: ArrowEndpoint
  to?: ArrowEndpoint
  at?: ArrowEndpoint
}

export interface Q1SpotlightSide {
  agent: string
  time: string
  channel: string
  id: string
  quote: string
  who: string
}
export interface Q1Spotlight {
  gapMinutes: number
  before: Q1SpotlightSide
  after: Q1SpotlightSide
}

export interface Q1Data {
  lanes: string[]
  segments: Q1Segment[]
  events: Q1Event[]
  silentPings: string[]
  arrows: Q1Arrow[]
  spotlight: Q1Spotlight
}

export interface Q2Channel {
  channel: string
  pre: number
  crisis: number
}
export interface Q2Round {
  hour: string
  crisis: boolean
  comms_huddle: number
  one_on_one_chat: number
  side_huddle: number
  official_post: number
  personal_post: number
  anonymous_post: number
}
export interface Q2AgentMetric {
  agent: string
  preLen: number
  crisisLen: number
  prePct: number
  crisisPct: number
}
export interface Q2Data {
  channels: Q2Channel[]
  rhythmChannels: string[]
  rhythmColorVar: Record<string, string>
  rounds: Q2Round[]
  agentMetrics: Q2AgentMetric[]
}

export interface Q3DocketRow {
  date: string
  tag: 'neutral' | 'warn' | 'good' | 'critical'
  tagLabel: string
  head: string
  outcome: string | null
  detail: string
}
export interface Q3Card {
  date: string
  agent: string
  outcome: string
  h1: string
  t1: string
  h2: string
  t2: string
}
export interface Q3Data {
  docket: Q3DocketRow[]
  cards: Q3Card[]
  outcomeStyle: Record<string, { tag: 'watch' | 'breach'; label: string }>
}

export interface MC1 {
  meta: { corpusMessages: number; agentCount: number; roundCount: number; dateStart: string; dateEnd: string }
  headline: {
    firstConfirmedTime: string
    minutesEarly: number
    embargoLift: string
    breachId: string
    breachAgent: string
    breachChannel: string
    gateSilentSince: string
    gateUnansweredPings: number
    gateWindow: string
  }
  agents: Record<string, AgentInfo>
  answers: { q1: string; q2: string; q3: string }
  q1: Q1Data
  q2: Q2Data
  q3: Q3Data
}

export function useMC1(): Loadable<MC1> {
  return useJson<MC1>('mc1.json')
}

/** Bare message IDs in prose (20460605_21_026-style) rendered as mono "cite"
    spans, so the written answers need no inline markup of their own. */
const ID_RE = /\b\d{8}_\d{2}_\d{3}\b/g

export function citeify(text: string): ReactNode {
  const parts = text.split(ID_RE)
  const ids = text.match(ID_RE) ?? []
  return (
    <>
      {parts.map((part, i) => (
        <Fragment key={i}>
          {part}
          {ids[i] && <span className="cite">{ids[i]}</span>}
        </Fragment>
      ))}
    </>
  )
}

export function fmtTime(iso: string) {
  return iso.slice(11, 16)
}

const MONTH: Record<string, string> = { '05': 'May', '06': 'Jun' }
export function fmtDateTime(iso: string) {
  const mo = MONTH[iso.slice(5, 7)] ?? iso.slice(5, 7)
  const day = iso.slice(8, 10).replace(/^0/, '')
  return `${mo} ${day}, ${iso.slice(11, 16)}`
}

export const TAG_SIGNAL: Record<string, 'breach' | 'watch' | null> = {
  'the leak': 'breach',
  unanswered: 'watch',
  'still unanswered': 'watch',
  unverified: 'watch',
}
