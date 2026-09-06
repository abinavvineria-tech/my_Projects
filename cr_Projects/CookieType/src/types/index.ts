export type ThemeKey = 'purelily' | 'cookie' | 'bites' | 'timebreaker' | 'royal-vanilla' | 'sugar-dream' | 'cosmic' | 'custom' | string
export interface ThemeColors {
  background: string; surface: string; primary: string; secondary: string; text: string; subtext: string
  caret: string; error: string; success: string; accent: string; border: string
}
export type RankKey = 'crumb' | 'dough' | 'cookie' | 'skilled-cookie' | 'royal-typist' | 'kingdom-master' | 'timebreaker' | 'chrono-master' | 'bites-master' | 'legendary-typist'
export interface StorageAdapter { get: <T>(key:string)=>Promise<T|null>; set: <T>(key:string,value:T)=>Promise<void>; remove: <T>(key:string)=>Promise<void>; getAllKeys: ()=>Promise<string[]>; clear: ()=>Promise<void> }
export interface AuthState { isAuthenticated: boolean; user: { username: string; passwordHash: string } | null }
export interface PerformanceRecord { id: string; wpm: number; accuracy: number; rawWPM: number; consistency: number; errors: number; charactersTyped: number; mode: string; theme: ThemeKey; date: number; wordCount?: number; startedAt?: number; completedAt?: number; correct?: number; incorrect?: number; time?: number }
export interface UserProfile { username: string; avatar: string; rank: RankKey; bestWPM: number; averageWPM: number; totalTests: number; totalWords: number; totalCharacters: number; totalTypingTime: number; accuracy: number; consistency: number; streak: number; achievements: Record<string, boolean>; favoriteTheme: ThemeKey; lastTestDate: number }
export interface AchievementsState { firstTest?: boolean; firstPerfectTest?: boolean; speedCookie?: boolean; '100-tests'?: boolean; '1k-words'?: boolean; '1k-characters'?: boolean; codeRunner?: boolean; timebreaker?: boolean; bitesBuilder?: boolean; kingdomTypist?: boolean; legendaryTypist?: boolean }
export type TestMode = 'time' | 'words' | 'quote' | 'zen' | 'custom' | 'focus' | 'timebreaker'
export interface TestStats { wpm: number; accuracy: number; rawWPM: number; consistency: number; errors: number; characters: number; correct: number; incorrect: number; time: number; mode: string; wordCount: number; startedAt: number; completedAt: number }
