import React, { useEffect, useState } from 'react'
import { Sparkles, Keyboard, BarChart3, User, Settings, Palette, Eye, EyeOff } from 'lucide-react'

interface NavigationProps {
  onNavigate: (screen: string) => void
  currentScreen: string
  focusMode: boolean
  onToggleFocus: () => void
  onOpenEcosystem: () => void
  settings: any
}

export function Navigation({ onNavigate, currentScreen, focusMode, onToggleFocus, onOpenEcosystem, settings }: NavigationProps) {
  const [isVisible, setIsVisible] = useState(true)

  useEffect(() => {
    if (settings.focusMode) {
      setIsVisible(false)
      const timer = setTimeout(() => setIsVisible(true), 500)
      return () => clearTimeout(timer)
    }
    setIsVisible(true)
  }, [settings.focusMode])

  const navItems = [
    { id: 'typing', label: 'Test', icon: Keyboard },
    { id: 'statistics', label: 'Stats', icon: BarChart3 },
    { id: 'profile', label: 'Profile', icon: User },
    { id: 'settings', label: 'Settings', icon: Settings }
  ]

  return (
    <nav className={`fixed top-0 left-0 right-0 z-50 transition-opacity duration-500 ${isVisible ? 'opacity-100' : 'opacity-0 pointer-events-none'}`}>
      <div className="glass">
        <div className="max-w-7xl mx-auto px-4 h-14 flex items-center justify-between">
          <button onClick={onOpenEcosystem} className="flex items-center gap-2 hover:opacity-80 transition">
            <div className="w-8 h-8 rounded-full bg-gradient-to-br from-amber-300 to-pink-500 flex items-center justify-center">
              <Sparkles className="w-4 h-4 text-white" />
            </div>
            <span className="font-extrabold tracking-tight hidden sm:inline">CookieType</span>
          </button>

          <div className="flex items-center gap-1">
            {navItems.map(item => (
              <button
                key={item.id}
                onClick={() => onNavigate(item.id)}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium transition flex items-center gap-1.5 ${
                  currentScreen === item.id 
                    ? 'bg-amber-300/20 text-amber-300' 
                    : 'hover:bg-white/5 text-subtext'
                }`}
              >
                <item.icon className="w-3.5 h-3.5" />
                <span className="hidden md:inline">{item.label}</span>
              </button>
            ))}
          </div>

          <div className="flex items-center gap-2">
            <button 
              onClick={onToggleFocus}
              className="glass rounded-lg p-2 hover:bg-white/5 transition"
              title={focusMode ? 'Exit Focus Mode' : 'Enter Focus Mode'}
            >
              {focusMode ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
            </button>
          </div>
        </div>
      </div>
    </nav>
  )
}