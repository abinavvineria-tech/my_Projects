import { createContext, useContext, useState, useEffect, useCallback, ReactNode } from 'react'
import type { ThemeKey, ThemeColors } from '../types'

interface ThemeContextType {
  theme: ThemeKey
  colors: ThemeColors
  setTheme: (theme: ThemeKey) => void
  customThemes: Record<string, ThemeColors>
  addCustomTheme: (name: string, colors: ThemeColors) => void
  removeCustomTheme: (name: string) => void
}

const ThemeContext = createContext<ThemeContextType | null>(null)

const DEFAULT_THEMES: Record<ThemeKey, ThemeColors> = {
  purelily: {
    background: '#FDF8FF',
    surface: '#FFFFFF',
    primary: '#7C3AED',
    secondary: '#F0ABFC',
    text: '#2D1B4E',
    subtext: '#6B5B7B',
    caret: '#F59E0B',
    error: '#EF4444',
    success: '#10B981',
    accent: '#EC4899',
    border: '#E9D5F0'
  },
  cookie: {
    background: '#FFF8F0',
    surface: '#FFFEF7',
    primary: '#C2410C',
    secondary: '#FED7AA',
    text: '#431407',
    subtext: '#8B5E3C',
    caret: '#F59E0B',
    error: '#EF4444',
    success: '#22C55E',
    accent: '#FB923C',
    border: '#FDE68A'
  },
  bites: {
    background: '#0A0514',
    surface: '#140E24',
    primary: '#A855F7',
    secondary: '#EC4899',
    text: '#F3F0F8',
    subtext: '#8B7FB0',
    caret: '#00FFFF',
    error: '#F87171',
    success: '#34D399',
    accent: '#06B6D4',
    border: '#2D1B4E'
  },
  timebreaker: {
    background: '#050312',
    surface: '#0D0820',
    primary: '#6366F1',
    secondary: '#EC4899',
    text: '#E0E7FF',
    subtext: '#818CF8',
    caret: '#FBBF24',
    error: '#F87171',
    success: '#34D399',
    accent: '#A855F7',
    border: '#1E1B4B'
  },
  'royal-vanilla': {
    background: '#FDFAF0',
    surface: '#FFFFF8',
    primary: '#B45309',
    secondary: '#FDE68A',
    text: '#3D2900',
    subtext: '#8B7355',
    caret: '#F59E0B',
    error: '#EF4444',
    success: '#22C55E',
    accent: '#D97706',
    border: '#FDE68A'
  },
  'sugar-dream': {
    background: '#FAF5FF',
    surface: '#FFFFFF',
    primary: '#C084FC',
    secondary: '#F9A8D4',
    text: '#4C1D95',
    subtext: '#A855F7',
    caret: '#F472B6',
    error: '#FCA5A5',
    success: '#86EFAC',
    accent: '#FDBA74',
    border: '#E9D5F0'
  },
  cosmic: {
    background: '#030014',
    surface: '#0A0524',
    primary: '#8B5CF6',
    secondary: '#06B6D4',
    text: '#F0F4FF',
    subtext: '#A5B4FC',
    caret: '#FDE047',
    error: '#FCA5A5',
    success: '#86EFAC',
    accent: '#EC4899',
    border: '#1E1B4B'
  },
  custom: {
    background: '#0A0514',
    surface: '#140E24',
    primary: '#A855F7',
    secondary: '#EC4899',
    text: '#F3F0F8',
    subtext: '#8B7FB0',
    caret: '#F59E0B',
    error: '#EF4444',
    success: '#10B981',
    accent: '#06B6D4',
    border: '#2D1B4E'
  }
}

export function ThemeProvider({ children, theme: initialTheme }: { children: ReactNode; theme: ThemeKey }) {
  const [theme, setThemeState] = useState<ThemeKey>(initialTheme)
  const [customThemes, setCustomThemes] = useState<Record<string, ThemeColors>>({})

  useEffect(() => {
    const saved = localStorage.getItem('cookietype-custom-themes')
    if (saved) {
      try { setCustomThemes(JSON.parse(saved)) } catch {}
    }
  }, [])

  useEffect(() => {
    localStorage.setItem('cookietype-custom-themes', JSON.stringify(customThemes))
  }, [customThemes])

  const colors = customThemes[theme] || DEFAULT_THEMES[theme] || DEFAULT_THEMES.custom

  useEffect(() => {
    const root = document.documentElement
    Object.entries(colors).forEach(([key, value]) => {
      root.style.setProperty(`--${key}`, value)
    })
    document.body.style.backgroundColor = colors.background
    document.body.style.color = colors.text
  }, [colors])

  const setTheme = useCallback((newTheme: ThemeKey) => {
    setThemeState(newTheme)
    localStorage.setItem('cookietype-active-theme', newTheme)
  }, [])

  const addCustomTheme = useCallback((name: string, themeColors: ThemeColors) => {
    setCustomThemes(prev => {
      const updated = { ...prev, [name]: themeColors }
      localStorage.setItem('cookietype-custom-themes', JSON.stringify(updated))
      return updated
    })
  }, [])

  const removeCustomTheme = useCallback((name: string) => {
    setCustomThemes(prev => {
      const { [name]: removed, ...rest } = prev
      localStorage.setItem('cookietype-custom-themes', JSON.stringify(rest))
      return rest
    })
  }, [])

  return (
    <ThemeContext.Provider value={{ theme, colors, setTheme, customThemes, addCustomTheme, removeCustomTheme }}>
      {children}
    </ThemeContext.Provider>
  )
}

export function useTheme() {
  const context = useContext(ThemeContext)
  if (!context) throw new Error('useTheme must be used within ThemeProvider')
  return context
}