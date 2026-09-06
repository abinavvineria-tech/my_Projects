import React, { useState, useEffect, useCallback, ReactNode } from 'react'
import { ThemeProvider } from './hooks/useTheme'
import { ThemeEngine } from './components/ThemeEngine'
import { TypingScreen } from './components/typing/TypingScreen'
import { ResultsScreen } from './components/results/ResultsScreen'
import { StatisticsScreen } from './components/statistics/StatisticsScreen'
import { ProfileScreen } from './components/profile/ProfileScreen'
import { SettingsScreen } from './components/settings/SettingsScreen'
import { Navigation } from './components/navigation/Navigation'
import { EcosystemSelector } from './components/ecosystem/EcosystemSelector'
import { useLocalStorage } from './hooks/useLocalStorage'
import { useTypingEngine } from './hooks/useTypingEngine'
import { useSound } from './hooks/useSound'
import { PerformanceMonitor } from './components/performance/PerformanceMonitor'
import { useAuth } from './hooks/useAuth'
import { Analytics } from './components/analytics/Analytics'
import { useAchievements } from './hooks/useAchievements'

export type Screen = 
  | 'typing' 
  | 'results' 
  | 'statistics' 
  | 'profile' 
  | 'settings' 
  | 'ecosystem'

export interface AppSettings {
  theme: string
  soundEnabled: boolean
  soundVolume: number
  soundPreset: string
  focusMode: boolean
  reducedMotion: boolean
  disableEffects: boolean
  notifications: boolean
  autoStart: boolean
  defaultTime: number
  language: string
}

export interface DatabaseState {
  stats: any[]
  achievements: Record<string, boolean>
  profile: any
  themes: Record<string, any>
  history: any[]
}

function App() {
  const [currentScreen, setCurrentScreen] = useState<Screen>('typing')
  const [isEcosystemOpen, setIsEcosystemOpen] = useState(false)
  const [settings] = useLocalStorage<AppSettings>('cookietype-settings', {
    theme: 'purelily',
    soundEnabled: true,
    soundVolume: 0.7,
    soundPreset: 'soft',
    focusMode: false,
    reducedMotion: false,
    disableEffects: false,
    notifications: true,
    autoStart: true,
    defaultTime: 30,
    language: 'en'
  })

  const [dbState, setDbState] = useLocalStorage<DatabaseState>('cookietype-db', {
    stats: [],
    achievements: {},
    profile: {
      username: 'Player',
      avatar: '🍪',
      rank: 'cookie',
      bestWPM: 0,
      averageWPM: 0,
      totalTests: 0,
      totalWords: 0,
      totalCharacters: 0,
      totalTypingTime: 0,
      accuracy: 100,
      consistency: 100,
      streak: 0,
      achievements: [],
      favoriteTheme: 'purelily',
      lastTestDate: 0
    },
    themes: {},
    history: []
  })

  const typingEngine = useTypingEngine()
  const { playSound } = useSound()
  const auth = useAuth()

  useAchievements(dbState, setDbState)

  const handleTestComplete = useCallback((stats: any) => {
    const record = {
      id: Date.now().toString(),
      wpm: stats.wpm,
      accuracy: stats.accuracy,
      rawWPM: stats.rawWPM,
      consistency: stats.consistency,
      errors: stats.errors,
      charactersTyped: stats.characters,
      mode: stats.mode,
      theme: settings.theme,
      date: Date.now()
    }

    setDbState(prev => ({
      ...prev,
      stats: [...prev.stats, record],
      history: [...prev.history, record]
    }))

    playSound('success')
  }, [dbState, setDbState, playSound, settings.theme])

  const handleThemeChange = useCallback((theme: string) => {
    localStorage.setItem('cookietype-active-theme', theme)
  }, [])

  useEffect(() => {
    if (currentScreen === 'typing') {
      typingEngine.startTest(settings.defaultTime, 'time')
    }
  }, [currentScreen, typingEngine, settings.defaultTime])

  useEffect(() => {
    const savedTheme = localStorage.getItem('cookietype-active-theme')
    if (savedTheme) {
      handleThemeChange(savedTheme)
    }
  }, [handleThemeChange])

  return (
    <ThemeProvider theme={settings.theme as any}>
      <div className="min-h-screen w-full relative overflow-hidden">
        <Analytics data={dbState.stats} />
        <PerformanceMonitor />

        <ThemeEngine themes={dbState.themes} />

        <Navigation
          onNavigate={setCurrentScreen}
          currentScreen={currentScreen}
          focusMode={settings.focusMode}
          onToggleFocus={() => setSettings(prev => ({ ...prev, focusMode: !prev.focusMode }))}
          onOpenEcosystem={() => setIsEcosystemOpen(true)}
          settings={settings}
        />

        <EcosystemSelector
          isOpen={isEcosystemOpen}
          onClose={() => setIsEcosystemOpen(false)}
          onSelect={(ecosystem: string) => {
            setSettings(prev => ({ ...prev, theme: ecosystem }))
            setIsEcosystemOpen(false)
          }}
        />

        <main className="w-full h-full pt-20 px-4 pb-4">
          {currentScreen === 'typing' && (
            <TypingScreen
              test={typingEngine.test}
              onTestComplete={handleTestComplete}
              focusMode={settings.focusMode}
              soundEnabled={settings.soundEnabled}
            />
          )}

          {currentScreen === 'results' && typingEngine.lastTest && (
            <ResultsScreen
              stats={typingEngine.lastTest}
              onRetry={() => typingEngine.startTest(settings.defaultTime, 'time')}
              onContinue={() => setCurrentScreen('typing')}
            />
          )}

          {currentScreen === 'statistics' && (
            <StatisticsScreen
              stats={dbState.stats}
              onNavigate={setCurrentScreen}
            />
          )}

          {currentScreen === 'profile' && (
            <ProfileScreen
              profile={dbState.profile}
              achievements={dbState.achievements}
              onUpdate={profile => setDbState(prev => ({ ...prev, profile }))}
            />
          )}

          {currentScreen === 'settings' && (
            <SettingsScreen
              settings={settings}
              onUpdate={newSettings => {
                localStorage.setItem('cookietype-settings', JSON.stringify(newSettings))
              }}
              onNavigate={setCurrentScreen}
            />
          )}
        </main>

        {typingEngine.isRunning && (
          <div className="fixed bottom-4 right-4 glass rounded-lg p-3 z-50">
            <div className="text-xs text-subtext mb-1">Performance</div>
            <div className="flex items-center gap-4">
              <div>WPM: {typingEngine.currentWPM}</div>
              <div className="text-subtext">|</div>
              <div>Accuracy: {typingEngine.accuracyPercent}%</div>
              <div className="text-subtext">|</div>
              <div>Errors: {typingEngine.errors}</div>
            </div>
          </div>
        )}
      </div>
    </ThemeProvider>
  )
}

export default App