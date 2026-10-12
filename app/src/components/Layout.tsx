import type { ReactNode } from 'react'
import { Link, useLocation } from 'react-router-dom'
import './Layout.css'

const NAV = [
  { to: '/', label: 'Forensic Ledger' },
  { to: '/mc1', label: 'MC1 — The HarborCrest Leak' },
  { to: '/mc2', label: 'MC2 — SwiftWren' },
]

export default function Layout({ children }: { children: ReactNode }) {
  const { pathname } = useLocation()
  return (
    <div className="site">
      <header className="site-header">
        <nav className="site-nav">
          {NAV.map((item) => (
            <Link
              key={item.to}
              to={item.to}
              className={pathname === item.to ? 'is-active' : ''}
            >
              {item.label}
            </Link>
          ))}
        </nav>
      </header>
      <main>{children}</main>
    </div>
  )
}
