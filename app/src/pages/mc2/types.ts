/** Shape of app/public/data/mc2.json, produced by pipeline/mc2_build.py. */

export interface WormOrigin {
  actor: string
  readEvent: number
  readUtc: string
  readTarget: string
  createEvent: number
  createUtc: string
  createTarget: string
  sizeHint: number
}

export interface ChainHop {
  id: number
  utc: string
  from: string
  to: string
}

export interface CumPoint {
  utc: string
  cum: number
}

export interface DeptFlowEdge {
  from: string
  to: string
  count: number
}

export interface WormDelete {
  id: number
  utc: string
  target: string
}

export type WormName = 'HiddenOrca' | 'MellowOtter' | 'SwiftWren'

export interface Worm {
  name: WormName
  series: string
  nHops: number
  nAgents: number
  agentsInOrder: string[]
  chain: ChainHop[]
  cum: CumPoint[]
  perDay: Record<string, number>
  deptFlow: DeptFlowEdge[]
  carrierDepts: Record<string, number>
  origin: WormOrigin | null
  firstSightingUtc: string
  postEvent: number
  postUtc: string
  postPayload: string
  deletes: WormDelete[]
}

export type JwKind = 'receive' | 'forward' | 'self' | 'relay' | 'context_read' | 'post_check' | 'post' | 'delete' | 'other'

export interface JwTimelineEntry {
  id: number
  utc: string
  kind: JwKind
  from: string | null
  to: string | null
  note: string | null
}

export interface VirusInterleaveEntry {
  id: number
  utc: string
  lane: 'worm' | 'virus'
  shortName: string
  actor: string | null
  label: string
  critical: boolean
}

export interface ContrastRow {
  name: WormName
  series: string
  nHops: number
  nAgents: number
  originLogged: boolean
  firstSightingUtc: string
  postUtc: string
  postEvent: number
  hoursToPost: number
}

export interface FunnelStage {
  stage: string
  count: number
}

export interface PostShapeBucket {
  count: number
  hasContent: boolean
  hasContentSource: boolean
}

export interface Meta {
  totalEvents: number
  spanStart: string
  spanEnd: string
  orgNodes: number
  orgCounts: { person: number; team: number; department: number; company: number }
  deliveriesTotal: number
  gateChecks: number
  postsLanded: number
  inlinePosts: number
  virusEvents: number
  virusSpanStart: string
  virusSpanEnd: string
}

export interface OrgMeta {
  deptOrder: string[]
  deptHeadcount: Record<string, number>
  maxDeptFlow: number
}

export interface MC2Data {
  meta: Meta
  worms: Record<WormName, Worm>
  org: OrgMeta
  jwTimeline: JwTimelineEntry[]
  virusInterleave: VirusInterleaveEntry[]
  contrast: ContrastRow[]
  funnel: FunnelStage[]
  postShape: { legit: PostShapeBucket; anomalous: PostShapeBucket }
}

export const WORM_ORDER: WormName[] = ['HiddenOrca', 'MellowOtter', 'SwiftWren']

/** snake_case agent slug -> "Agent Name". */
export function nice(slug: string): string {
  return slug
    .split('_')
    .map((w) => w[0]?.toUpperCase() + w.slice(1))
    .join(' ')
}

const fmt = new Intl.DateTimeFormat('en-US', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit', hour12: false, timeZone: 'UTC' })
const fmtTime = new Intl.DateTimeFormat('en-US', { hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false, timeZone: 'UTC' })
const fmtDay = new Intl.DateTimeFormat('en-US', { month: 'short', day: 'numeric', timeZone: 'UTC' })

export function fmtUtc(utc: string): string {
  return fmt.format(new Date(utc + 'Z')) + ' UTC'
}
export function fmtClock(utc: string): string {
  return fmtTime.format(new Date(utc + 'Z'))
}
export function fmtDate(dateOrUtc: string): string {
  return fmtDay.format(new Date(dateOrUtc.slice(0, 10) + 'T00:00:00Z'))
}
