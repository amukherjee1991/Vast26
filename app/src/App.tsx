import { Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Home from './pages/Home'
import MC1 from './pages/MC1'
import MC2 from './pages/MC2'

export default function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/mc1" element={<MC1 />} />
        <Route path="/mc2" element={<MC2 />} />
      </Routes>
    </Layout>
  )
}
