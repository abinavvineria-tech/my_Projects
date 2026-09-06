import { useEffect } from 'react'
import type { PerformanceRecord, UserProfile, AchievementsState } from '../types'

export function useAchievements(
  dbState: { stats: PerformanceRecord[]; profile: UserProfile; achievements: AchievementsState },
  setDbState: React.Dispatch<React.SetStateAction<any>>
) {
  useEffect(() => {
    const stats = dbState.stats
    const achievements = { ...dbState.achievements }
    let hasNew = false

    if (stats.length >= 1 && !achievements.firstTest) {
      achievements.firstTest = true
      hasNew = true
    }
    
    if (stats.some(s => s.accuracy === 100) && !achievements.firstPerfectTest) {
      achievements.firstPerfectTest = true
      hasNew = true
    }
    
    if (stats.some(s => s.wpm >= 100) && !achievements.speedCookie) {
      achievements.speedCookie = true
      hasNew = true
    }
    
    if (stats.length >= 100 && !achievements['100-tests']) {
      achievements['100-tests'] = true
      hasNew = true
    }
    
    if (stats.reduce((sum, s) => sum + (s.wordCount || 0), 0) >= 1000 && !achievements['1k-words']) {
      achievements['1k-words'] = true
      hasNew = true
    }
    
    if (stats.reduce((sum, s) => sum + s.charactersTyped, 0) >= 10000 && !achievements['1k-characters']) {
      achievements['1k-characters'] = true
      hasNew = true
    }
    
    if (stats.some(s => s.mode === 'code') && !achievements.codeRunner) {
      achievements.codeRunner = true
      hasNew = true
    }
    
    if (stats.some(s => s.mode === 'timebreaker') && !achievements.timebreaker) {
      achievements.timebreaker = true
      hasNew = true
    }
    
    if (stats.some(s => s.mode === 'bites') && !achievements.bitesBuilder) {
      achievements.bitesBuilder = true
      hasNew = true
    }
    
    if (stats.some(s => s.mode === 'cookie') && !achievements.kingdomTypist) {
      achievements.kingdomTypist = true
      hasNew = true
    }
    
    if (dbState.profile.bestWPM >= 200 && !achievements.legendaryTypist) {
      achievements.legendaryTypist = true
      hasNew = true
    }

    if (hasNew) {
      setDbState((prev: any) => ({ ...prev, achievements }))
    }
  }, [dbState.stats, dbState.profile, setDbState])
}