import React, { useState, useEffect } from 'react'
import { Trophy, TrendingUp, Clock, Target, BarChart3, Star, RotateCcw, Flame, Award, Crown } from 'lucide-react'
import { useTheme } from '../../hooks/useTheme'

interface ResultsScreenProps {
  stats: any
  onRetry: () => void
  onContinue: () => void
}

export function ResultsScreen({ stats, onRetry, onContinue }: ResultsScreenProps) {
  const [showAnimation, setShowAnimation] = useState(false)
  const { theme } = useTheme()

  useEffect(() => {
    const t = setTimeout(() => setShowAnimation(true), 100)
    return () => clearTimeout(t)
  }, [])

  const isBest = stats.wpm > 80
  const getRankColor = (wpm: number) => {
    if (wpm >= 200) return 'from-amber-300 to-yellow-400'
    if (wpm >= 150) return 'from-purple-400 to-pink-400'
    if (wpm >= 100) return 'from-blue-400 to-cyan-400'
    if (wpm >= 80) return 'from-green-400 to-emerald-400'
    return 'from-gray-400 to-gray-500'
  }

  return (
    <div className="min-h-[85vh] flex flex-col items-center justify-center gap-8 animate-fade-in">
      {isBest && (
        <div className="glass-strong rounded-full px-8 py-4 flex items-center gap-4 animate-pulse-soft animate-scale-in">
          <Crown className="w-6 h-6 text-amber-300 fill-amber-300" />
          <Star className="w-6 h-6 text-pink-400 fill-pink-400" />
          <span className="font-bold text-lg text-gradient">NEW PERSONAL BEST</span>
        </div>
      )}

      <div className="text-center">
        <div className={`text-7xl md:text-8xl font-bold bg-gradient-to-r ${getRankColor(stats.wpm)} bg-clip-text text-transparent relative mb-6`}>          {stats.wpm || 0}
          <div className="absolute -top-2 -right-2">
            <div className="w-3 h-3 rounded-full bg-green-400 animate-pulse-soft"></div>
          </div>
        </div>
        <div className="text-sm md:text-base text-subtext mt-3 font-medium tracking-widest uppercase">WPM</div>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 md:gap-6 w-full max-w-4xl animate-slide-up-fade" style={{ animationDelay: '200ms' }}>
        <div className="glass-strong rounded-2xl p-6 text-center interactive group">
          <Target className="w-6 h-6 mx-auto mb-3 text-green-400 group-hover:scale-110 transition-transform" />
          <div className={`text-3xl md:text-4xl font-bold text-green-400 group-hover:text-green-300 transition-colors`}>{stats.accuracy || 100}%</div>
          <div className="text-xs text-subtext uppercase tracking-wider mt-2">Accuracy</div>
        </div>

        <div className="glass-strong rounded-2xl p-6 text-center interactive group">
          <div className="w-6 h-6 mx-auto mb-3 text-red-400 group-hover:scale-110 transition-transform">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M12 2C6.5 2 2 6.5 2 12s4.5 10 10 10 10-4.5 10-10S17.5 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm.5-13H11v6l5.2 3.2.8-.9-4.3-3.8z"/>
            </svg>
          </div>
          <div className={`text-3xl md:text-4xl font-bold text-red-400 group-hover:text-red-300 transition-colors`}>{stats.errors || 0}</div>
          <div className="text-xs text-subtext uppercase tracking-wider mt-2">Errors</div>
        </div>

        <div className="glass-strong rounded-2xl p-6 text-center interactive group">
          <Clock className="w-6 h-6 mx-auto mb-3 text-blue-400 group-hover:scale-110 transition-transform" />
          <div className={`text-3xl md:text-4xl font-bold text-blue-400 group-hover:text-blue-300 transition-colors`}>{Math.round(stats.time || 0)}s</div>
          <div className="text-xs text-subtext uppercase tracking-wider mt-2">Time</div>
        </div>

        <div className="glass-strong rounded-2xl p-6 text-center interactive group">
          <TrendingUp className="w-6 h-6 mx-auto mb-3 text-purple-400 group-hover:scale-110 transition-transform" />
          <div className={`text-3xl md:text-4xl font-bold text-purple-400 group-hover:text-purple-300 transition-colors`}>{stats.rawWPM || 0}</div>
          <div className="text-xs text-subtext uppercase tracking-wider mt-2">Raw WPM</div>
        </div>
      </div>

      <div className="w-full max-w-4xl glass-strong rounded-3xl p-8 animate-slide-up-fade" style={{ animationDelay: '400ms' }}>
        <div className="flex items-center justify-between mb-8">
          <h3 className="text-lg font-bold text-subtext uppercase tracking-wider">Performance Breakdown</h3>
          <div className="flex gap-2">
            {['Time', 'Mode', 'Consistency'].map((item) => (
              <div key={item} className="px-3 py-1 rounded-full bg-white/5 text-xs text-subtext border border-white/10">
                {item}
              </div>
            ))}
          </div>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-sm">
          <div className="flex justify-between items-center p-4 rounded-xl bg-white/5 hover:bg-white/10 transition-colors">
            <span className="text-subtext font-medium">Characters</span>
            <span className="font-mono text-lg">{stats.characters || 0}</span>
          </div>
          <div className="flex justify-between items-center p-4 rounded-xl bg-white/5 hover:bg-white/10 transition-colors">
            <span className="text-subtext font-medium">Correct</span>
            <span className="font-mono text-lg text-green-400">{stats.correct || 0}</span>
          </div>
          <div className="flex justify-between items-center p-4 rounded-xl bg-white/5 hover:bg-white/10 transition-colors">
            <span className="text-subtext font-medium">Incorrect</span>
            <span className="font-mono text-lg text-red-400">{stats.incorrect || 0}</span>
          </div>
          <div className="flex justify-between items-center p-4 rounded-xl bg-white/5 hover:bg-white/10 transition-colors">
            <span className="text-subtext font-medium">Mode</span>
            <span className="font-mono text-lg text-amber-300 capitalize">{stats.mode || 'time'}</span>
          </div>
          <div className="flex justify-between items-center p-4 rounded-xl bg-white/5 hover:bg-white/10 transition-colors">
            <span className="text-subtext font-medium">Consistency</span>
            <span className="font-mono text-lg text-purple-400">{stats.consistency || 95}%</span>
          </div>
          <div className="flex justify-between items-center p-4 rounded-xl bg-white/5 hover:bg-white/10 transition-colors">
            <span className="text-subtext font-medium">Word Count</span>
            <span className="font-mono text-lg text-blue-400">{stats.wordCount || 0}</span>
          </div>
        </div>
      </div>

      <div className="flex gap-6 animate-slide-up-fade" style={{ animationDelay: '600ms' }}>
        <button 
          onClick={onRetry}
          className="btn-primary px-10 py-4 flex items-center gap-3"
        >
          <RotateCcw className="w-5 h-5" /> Retry
        </button>
        <button 
          onClick={onContinue}
          className="btn-secondary px-10 py-4 flex items-center gap-3 group"
        >
          <span className="group-hover:text-text transition-colors">Continue</span>
          <div className="w-2 h-2 rounded-full bg-green-400 animate-pulse-soft"></div>
        </button>
      </div>
    </div>
  )
}
