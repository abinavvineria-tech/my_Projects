import React, { useState } from 'react'
import { User, Trophy, Star, Award, Settings as SettingsIcon, LogOut } from 'lucide-react'
import { useTheme } from '../../hooks/useTheme'

interface ProfileScreenProps {
  profile: any
  achievements: any
  onUpdate: (profile: any) => void
}

export function ProfileScreen({ profile, achievements, onUpdate }: ProfileScreenProps) {
  const [isEditing, setIsEditing] = useState(false)
  const [username, setUsername] = useState(profile.username || 'Player')
  const [avatar, setAvatar] = useState(profile.avatar || '🍪')
  const { theme } = useTheme()

  const handleSave = () => {
    onUpdate({ ...profile, username, avatar })
    setIsEditing(false)
  }

  const rankInfo: Record<string, { name: string; icon: string; color: string }> = {
    crumb: { name: 'Crumb', icon: ' crumbs', color: 'text-amber-200' },
    dough: { name: 'Dough', icon: '🌾', color: 'text-yellow-300' },
    cookie: { name: 'Cookie', icon: '🍪', color: 'text-amber-400' },
    'skilled-cookie': { name: 'Skilled Cookie', icon: '⭐', color: 'text-orange-400' },
    'royal-typist': { name: 'Royal Typist', icon: '👑', color: 'text-purple-400' },
    'kingdom-master': { name: 'Kingdom Master', icon: '🏰', color: 'text-indigo-400' },
    timebreaker: { name: 'Timebreaker', icon: '⏳', color: 'text-cyan-400' },
    'chrono-master': { name: 'Chrono Master', icon: '⏱️', color: 'text-blue-400' },
    'bites-master': { name: 'B!TES Master', icon: '💻', color: 'text-pink-400' },
    'legendary-typist': { name: 'Legendary Typist', icon: '✨', color: 'text-amber-300' }
  }

  const currentRank = rankInfo[profile.rank] || rankInfo.cookie

  const allAchievements = [
    { key: 'firstTest', name: 'First Test', icon: '🎯', unlocked: achievements.firstTest },
    { key: 'firstPerfectTest', name: 'Perfect Test', icon: '💎', unlocked: achievements.firstPerfectTest },
    { key: 'speedCookie', name: 'Speed Cookie', icon: '⚡', unlocked: achievements.speedCookie },
    { key: '100-tests', name: '100 Tests', icon: '🏆', unlocked: achievements['100-tests'] },
    { key: '1k-words', name: '1,000 Words', icon: '📝', unlocked: achievements['1k-words'] },
    { key: '1k-characters', name: '10,000 Characters', icon: '⌨️', unlocked: achievements['1k-characters'] },
    { key: '7-day-streak', name: '7 Day Streak', icon: '🔥', unlocked: achievements['7-day-streak'] },
    { key: '30-day-streak', name: '30 Day Streak', icon: '🌟', unlocked: achievements['30-day-streak'] },
    { key: 'codeRunner', name: 'Code Runner', icon: '🏃', unlocked: achievements.codeRunner },
    { key: 'timebreaker', name: 'Timebreaker', icon: '⏳', unlocked: achievements.timebreaker },
    { key: 'bitesBuilder', name: 'B!TES Builder', icon: '🛠️', unlocked: achievements.bitesBuilder },
    { key: 'kingdomTypist', name: 'Kingdom Typist', icon: '🏰', unlocked: achievements.kingdomTypist },
    { key: 'legendaryTypist', name: 'Legendary Typist', icon: '✨', unlocked: achievements.legendaryTypist }
  ]

  return (
    <div className="min-h-[85vh] flex flex-col items-center gap-8 animate-fade-in">
      <header className="w-full flex items-center justify-between px-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-full glass flex items-center justify-center">
            <User className="w-5 h-5 text-amber-300" />
          </div>
          <h1 className="text-xl font-extrabold">Profile</h1>
        </div>
        <button 
          onClick={() => onNavigate('settings')}
          className="glass rounded-lg px-3 py-2 hover:bg-white/5 transition"
        >
          <SettingsIcon className="w-4 h-4" />
        </button>
      </header>

      <div className="glass rounded-3xl p-8 w-full max-w-2xl text-center">
        {isEditing ? (
          <div className="space-y-4">
            <input
              type="text"
              value={avatar}
              onChange={e => setAvatar(e.target.value)}
              className="w-20 h-20 text-4xl text-center glass rounded-xl mx-auto block"
            />
            <input
              type="text"
              value={username}
              onChange={e => setUsername(e.target.value)}
              className="w-full max-w-xs px-4 py-2 glass rounded-lg text-center"
            />
            <div className="flex gap-2 justify-center">
              <button onClick={handleSave} className="px-4 py-2 rounded-lg bg-amber-300/20 text-amber-300 font-medium">Save</button>
              <button onClick={() => setIsEditing(false)} className="px-4 py-2 rounded-lg glass">Cancel</button>
            </div>
          </div>
        ) : (
          <>
            <div className="text-6xl mb-4">{avatar}</div>
            <h2 className="text-2xl font-extrabold mb-1">{username}</h2>
            <div className={`text-sm font-medium ${currentRank.color} mb-4`}>{currentRank.name}</div>
            <button onClick={() => setIsEditing(true)} className="text-xs text-subtext hover:text-text transition">Edit Profile</button>
          </>
        )}
      </div>

      <div className="grid grid-cols-2 md:grid-cols-3 gap-4 w-full max-w-2xl">
        <div className="glass rounded-2xl p-4 text-center">
          <Trophy className="w-5 h-5 text-amber-300 mx-auto mb-2" />
          <div className="text-2xl font-extrabold text-amber-300">{profile.bestWPM || 0}</div>
          <div className="text-[10px] text-subtext uppercase">Best WPM</div>
        </div>
        <div className="glass rounded-2xl p-4 text-center">
          <Clock className="w-5 h-5 text-blue-400 mx-auto mb-2" />
          <div className="text-2xl font-extrabold text-blue-400">{profile.totalTests || 0}</div>
          <div className="text-[10px] text-subtext uppercase">Tests</div>
        </div>
        <div className="glass rounded-2xl p-4 text-center">
          <Flame className="w-5 h-5 text-pink-400 mx-auto mb-2" />
          <div className="text-2xl font-extrabold text-pink-400">{profile.streak || 0}</div>
          <div className="text-[10px] text-subtext uppercase">Streak</div>
        </div>
      </div>

      <div className="w-full max-w-2xl glass rounded-2xl p-6">
        <h3 className="text-sm font-bold text-subtext uppercase tracking-wider mb-4">Achievements</h3>
        <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
          {allAchievements.map(a => (
            <div key={a.key} className={`glass rounded-xl p-3 flex items-center gap-3 ${a.unlocked ? 'border-amber-300/20' : 'opacity-50'}`}>
              <div className="text-2xl">{a.icon}</div>
              <div className="text-left">
                <div className="text-xs font-medium">{a.name}</div>
                <div className="text-[10px] text-subtext">{a.unlocked ? 'Unlocked' : 'Locked'}</div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}