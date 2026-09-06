import React, { useState } from 'react'
import { Volume2, VolumeX, Palette, Keyboard, Bell, Shield, Eye, EyeOff, Sun, Moon } from 'lucide-react'
import { useTheme } from '../../hooks/useTheme'

interface SettingsScreenProps {
  settings: any
  onUpdate: (settings: any) => void
  onNavigate: (screen: string) => void
}

export function SettingsScreen({ settings, onUpdate, onNavigate }: SettingsScreenProps) {
  const [local, setLocal] = useState(settings)
  const { theme } = useTheme()

  const toggle = (key: string) => {
    const updated = { ...local, [key]: !local[key] }
    setLocal(updated)
    onUpdate(updated)
  }

  return (
    <div className="min-h-[85vh] flex flex-col items-center gap-8 animate-fade-in">
      <header className="w-full flex items-center justify-between px-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-full glass flex items-center justify-center">
            <Palette className="w-5 h-5 text-amber-300" />
          </div>
          <h1 className="text-xl font-extrabold">Settings</h1>
        </div>
        <button onClick={() => onNavigate('typing')} className="text-sm text-subtext hover:text-text transition">Done</button>
      </header>

      <div className="w-full max-w-2xl space-y-4">
        <div className="glass rounded-2xl p-5">
          <h3 className="text-sm font-bold text-subtext uppercase tracking-wider mb-4">Audio</h3>
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              {local.soundEnabled ? <Volume2 className="w-5 h-5" /> : <VolumeX className="w-5 h-5" />}
              <span className="text-sm">Typing Sounds</span>
            </div>
            <button onClick={() => toggle('soundEnabled')} className={`w-12 h-6 rounded-full transition ${local.soundEnabled ? 'bg-amber-300' : 'bg-white/10'}`}>
              <div className={`w-5 h-5 rounded-full bg-white transition-transform ${local.soundEnabled ? 'translate-x-6' : 'translate-x-0.5'}`}></div>
            </button>
          </div>
        </div>

        <div className="glass rounded-2xl p-5">
          <h3 className="text-sm font-bold text-subtext uppercase tracking-wider mb-4">Display</h3>
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-sm">Focus Mode</span>
              <button onClick={() => toggle('focusMode')} className={`w-12 h-6 rounded-full transition ${local.focusMode ? 'bg-amber-300' : 'bg-white/10'}`}>
                <div className={`w-5 h-5 rounded-full bg-white transition-transform ${local.focusMode ? 'translate-x-6' : 'translate-x-0.5'}`}></div>
              </button>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm">Reduced Motion</span>
              <button onClick={() => toggle('reducedMotion')} className={`w-12 h-6 rounded-full transition ${local.reducedMotion ? 'bg-amber-300' : 'bg-white/10'}`}>
                <div className={`w-5 h-5 rounded-full bg-white transition-transform ${local.reducedMotion ? 'translate-x-6' : 'translate-x-0.5'}`}></div>
              </button>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm">Disable Effects</span>
              <button onClick={() => toggle('disableEffects')} className={`w-12 h-6 rounded-full transition ${local.disableEffects ? 'bg-amber-300' : 'bg-white/10'}`}>
                <div className={`w-5 h-5 rounded-full bg-white transition-transform ${local.disableEffects ? 'translate-x-6' : 'translate-x-0.5'}`}></div>
              </button>
            </div>
          </div>
        </div>

        <div className="glass rounded-2xl p-5">
          <h3 className="text-sm font-bold text-subtext uppercase tracking-wider mb-4">Notifications</h3>
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <Bell className="w-5 h-5" />
              <span className="text-sm">Achievement Alerts</span>
            </div>
            <button onClick={() => toggle('notifications')} className={`w-12 h-6 rounded-full transition ${local.notifications ? 'bg-amber-300' : 'bg-white/10'}`}>
              <div className={`w-5 h-5 rounded-full bg-white transition-transform ${local.notifications ? 'translate-x-6' : 'translate-x-0.5'}`}></div>
            </button>
          </div>
        </div>

        <div className="glass rounded-2xl p-5">
          <h3 className="text-sm font-bold text-subtext uppercase tracking-wider mb-4">About</h3>
          <div className="text-xs text-subtext space-y-2">
            <p>CookieType: B!TES × Timebreaker</p>
            <p>Version 0.0.0</p>
            <p>Local-first architecture</p>
          </div>
        </div>
      </div>
    </div>
  )
}