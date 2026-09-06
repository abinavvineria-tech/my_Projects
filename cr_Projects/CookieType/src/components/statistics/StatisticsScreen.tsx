import React, { useState } from 'react'
import { BarChart3, TrendingUp, Clock, Calendar, Flame, Award } from 'lucide-react'
import { useTheme } from '../../hooks/useTheme'

interface StatisticsScreenProps {
  stats: any[]
  onNavigate: (screen: string) => void
}

export function StatisticsScreen({ stats, onNavigate }: StatisticsScreenProps) {
  const [period, setPeriod] = useState('30')
  const { theme } = useTheme()

  const filteredStats = stats.filter(s => {
    const cutoff = Date.now() - parseInt(period) * 24 * 60 * 60 * 1000
    return s.date > cutoff
  })

  const bestWPM = Math.max(...filteredStats.map(s => s.wpm), 0)
  const avgWPM = Math.round(filteredStats.reduce((sum, s) => sum + s.wpm, 0) / Math.max(1, filteredStats.length))
  const totalTests = filteredStats.length
  const totalWords = filteredStats.reduce((sum, s) => sum + s.wordCount, 0)
  const totalChars = filteredStats.reduce((sum, s) => sum + s.charactersTyped, 0)
  const totalMinutes = Math.round(filteredStats.reduce((sum, s) => sum + s.wpm, 0) / 60)

  return (
    <div className="min-h-[85vh] flex flex-col items-center gap-8 animate-fade-in">
      <header className="w-full flex items-center justify-between px-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-full glass flex items-center justify-center">
            <BarChart3 className="w-5 h-5 text-amber-300" />
          </div>
          <h1 className="text-xl font-extrabold">Statistics</h1>
        </div>
        <div className="flex gap-2">
          {['7', '30', '90', 'all'].map(p => (
            <button
              key={p}
              onClick={() => setPeriod(p)}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition ${period === p ? 'bg-amber-300/20 text-amber-300' : 'glass hover:bg-white/5'}`}
            >
              {p === 'all' ? 'All' : `${p}d`}
            </button>
          ))}
        </div>
      </header>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 w-full max-w-4xl">
        <div className="glass rounded-2xl p-5">
          <TrendingUp className="w-5 h-5 text-amber-300 mb-2" />
          <div className="text-3xl font-extrabold text-amber-300">{bestWPM}</div>
          <div className="text-[10px] text-subtext uppercase tracking-wider">Best WPM</div>
        </div>
        <div className="glass rounded-2xl p-5">
          <Clock className="w-5 h-5 text-blue-400 mb-2" />
          <div className="text-3xl font-extrabold text-blue-400">{avgWPM}</div>
          <div className="text-[10px] text-subtext uppercase tracking-wider">Average WPM</div>
        </div>
        <div className="glass rounded-2xl p-5">
          <Calendar className="w-5 h-5 text-green-400 mb-2" />
          <div className="text-3xl font-extrabold text-green-400">{totalTests}</div>
          <div className="text-[10px] text-subtext uppercase tracking-wider">Tests</div>
        </div>
        <div className="glass rounded-2xl p-5">
          <Flame className="w-5 h-5 text-pink-400 mb-2" />
          <div className="text-3xl font-extrabold text-pink-400">{totalWords}</div>
          <div className="text-[10px] text-subtext uppercase tracking-wider">Words</div>
        </div>
      </div>

      <div className="w-full max-w-4xl glass rounded-2xl p-6">
        <h3 className="text-sm font-bold text-subtext uppercase tracking-wider mb-4">WPM History</h3>
        <div className="h-48 flex items-end gap-1">
          {filteredStats.slice(-30).map((s, i) => (
            <div key={i} className="flex-1 flex flex-col items-center gap-1">
              <div 
                className="w-full bg-gradient-to-t from-amber-300/40 to-pink-500/40 rounded-t transition-all"
                style={{ height: `${Math.max(4, (s.wpm / 150) * 100)}%` }}
              />
              <div className="text-[8px] text-subtext/50 rotate-45 origin-left-left">{new Date(s.date).toLocaleDateString()}</div>
            </div>
          ))}
        </div>
      </div>

      <div className="w-full max-w-4xl glass rounded-2xl p-6">
        <h3 className="text-sm font-bold text-subtext uppercase tracking-wider mb-4">Accuracy History</h3>
        <div className="h-32 flex items-end gap-1">
          {filteredStats.slice(-30).map((s, i) => (
            <div key={i} className="flex-1 flex flex-col items-center gap-1">
              <div 
                className="w-full bg-gradient-to-t from-green-400/40 to-emerald-500/40 rounded-t transition-all"
                style={{ height: `${Math.max(4, (s.accuracy / 100) * 100)}%` }}
              />
            </div>
          ))}
        </div>
      </div>

      <div className="text-[10px] text-subtext/50 font-medium tracking-widest uppercase">
        {totalTests} tests · {totalChars} characters · {totalMinutes} minutes
      </div>
    </div>
  )
}