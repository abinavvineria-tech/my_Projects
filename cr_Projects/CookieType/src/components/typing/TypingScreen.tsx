import React, { useEffect, useRef, useState, useCallback } from 'react'
import { useTheme } from '../../hooks/useTheme'

interface TypingScreenProps {
  test: any
  onTestComplete: (stats: any) => void
  focusMode: boolean
  soundEnabled: boolean
}

export function TypingScreen({ test, onTestComplete, focusMode, soundEnabled }: TypingScreenProps) {
  const inputRef = useRef<HTMLInputElement>(null)
  const [typed, setTyped] = useState('')
  const [currentIndex, setCurrentIndex] = useState(0)
  const [errors, setErrors] = useState(0)
  const [wpm, setWpm] = useState(0)
  const [startTime, setStartTime] = useState(0)
  const [isStarted, setIsStarted] = useState(false)
  const { theme } = useTheme()

  useEffect(() => {
    inputRef.current?.focus()
  }, [])

  const handleKey = useCallback((e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.ctrlKey || e.metaKey || e.altKey) return
    if (!isStarted) {
      setIsStarted(true)
      setStartTime(Date.now())
    }

    const key = e.key
    if (key.length > 1) {
      if (key === 'Backspace') {
        setCurrentIndex(prev => Math.max(0, prev - 1))
        setTyped(prev => prev.slice(0, -1))
        return
      }
      return
    }

    const expected = test?.testText?.[currentIndex] || ''
    const isCorrect = key === expected

    setTyped(prev => prev + key)
    setCurrentIndex(prev => prev + 1)
    if (!isCorrect) setErrors(prev => prev + 1)

    // WPM calc
    const elapsed = (Date.now() - startTime) / 1000
    const netChars = typed.length + (isCorrect ? 1 : 0) - errors - (!isCorrect ? 0 : 0)
    const calcWPM = Math.round(((netChars / 5) / (Math.max(0.1, elapsed) / 60)))
    setWpm(Math.max(0, calcWPM))
  }, [test, currentIndex, startTime, isStarted, typed, errors])

  const renderChar = (char: string, index: number) => {
    const isTyped = index < typed.length
    const isCurrent = index === currentIndex

    if (isTyped) {
      const isCorrect = typed[index] === char
      return (
        <span 
          key={index}
          className={`typing-char ${isCorrect ? 'correct' : 'incorrect'} relative`}
        >
          {char}
        </span>
      )
    }

    if (isCurrent) {
      return (
        <span 
          key={index}
          className="typing-char current relative"
        >
          {char}
        </span>
      )
    }

    return (
      <span key={index} className="typing-char pending relative">
        {char}
      </span>
    )
  }

  const textToShow = test?.testText || 'Type the kingdom. Break the clock.'

  return (
    <div className="min-h-[85vh] flex flex-col items-center justify-center gap-8 animate-fade-in">
      {/* Minimal Header */}
      <header className={`w-full flex items-center justify-between px-6 py-4 transition-all duration-500 ${focusMode ? 'opacity-50 scale-95' : 'opacity-100 scale-100'}`}>
        <div className="flex items-center gap-2">
          <div className="w-2 h-2 rounded-full bg-green-400 animate-pulse-soft"></div>
          <span className="text-xs text-subtext font-mono tracking-widest uppercase">CookieType × B!TES × Timebreaker</span>
        </div>
        <div className="flex items-center gap-4 text-xs font-medium text-subtext">
          <span className="px-2 py-1 rounded-md bg-white/5 glass-strong">Mode: Time</span>
          <span className="px-2 py-1 rounded-md bg-white/5 glass-strong">Focus: {focusMode ? 'On' : 'Off'}</span>
        </div>
      </header>

      {/* Main Typing Area */}
      <div className="w-full max-w-5xl px-4 md:px-8">
        <div className="glass-strong rounded-3xl p-6 md:p-10 relative overflow-hidden shadow-2xl shadow-purple-900/20">
          {/* Background effects */}
          <div className="absolute inset-0 bg-gradient-to-br from-purple-500/5 to-pink-500/5 rounded-3xl"></div>
          <div className="absolute top-0 right-0 w-64 h-64 bg-gradient-to-br from-amber-300/10 to-purple-500/10 rounded-full blur-3xl -translate-y-1/3 translate-x-1/3"></div>
          
          <div className="relative z-10">
            <div className="mono text-xl md:text-3xl lg:text-4xl leading-relaxed tracking-tight">
              {!isStarted && (
                <div className="text-subtext text-center py-20">
                  <div className="w-12 h-12 mx-auto mb-6 rounded-full bg-white/5 glass flex items-center justify-center">
                    <span className="text-2xl">⌨️</span>
                  </div>
                  <p className="text-base font-medium">Press any key to begin...</p>
                  <p className="text-xs text-subtext mt-2 opacity-70">Focus Mode: {focusMode ? 'Active' : 'Inactive'}</p>
                </div>
              )}
              {isStarted && (
                <div className="break-words">
                  {textToShow.split('').map(renderChar)}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Live Stats */}
      <div className="flex items-center gap-6 md:gap-12 text-sm font-mono animate-fade-in-up" style={{ animationDelay: '200ms' }}>
        <div className="text-center">
          <div className="text-3xl md:text-4xl font-bold bg-gradient-to-t from-amber-300 to-amber-500 bg-clip-text text-transparent">
            {wpm}
          </div>
          <div className="text-[10px] text-subtext uppercase tracking-widest mt-1">WPM</div>
        </div>
        <div className="w-px h-10 bg-white/10"></div>
        <div className="text-center">
          <div className="text-3xl md:text-4xl font-bold bg-gradient-to-t from-green-400 to-green-600 bg-clip-text text-transparent">
            {Math.round((typed.length - errors) / Math.max(typed.length, 1) * 100)}%
          </div>
          <div className="text-[10px] text-subtext uppercase tracking-widest mt-1">Accuracy</div>
        </div>
        <div className="w-px h-10 bg-white/10"></div>
        <div className="text-center">
          <div className="text-3xl md:text-4xl font-bold bg-gradient-to-t from-red-400 to-red-600 bg-clip-text text-transparent">
            {errors}
          </div>
          <div className="text-[10px] text-subtext uppercase tracking-widest mt-1">Errors</div>
        </div>
        <div className="w-px h-10 bg-white/10"></div>
        <div className="text-center">
          <div className="text-lg font-mono text-subtext">
            {typed.length}/{textToShow.length}
          </div>
          <div className="text-[10px] text-subtext uppercase tracking-widest mt-1">Progress</div>
        </div>
      </div>

      {/* Progress Bar */}
      <div className="w-full max-w-3xl px-4 md:px-8 animate-fade-in-up" style={{ animationDelay: '400ms' }}>
        <div className="progress-bar">
          <div 
            className="progress-bar-fill"
            style={{ width: `${Math.min(100, (typed.length / textToShow.length) * 100)}%` }}
          ></div>
        </div>
        <div className="flex justify-between text-[10px] text-subtext mt-1">
          <span>0%</span>
          <span>Complete</span>
        </div>
      </div>

      {/* Hidden input */}
      <input
        ref={inputRef}
        type="text"
        autoFocus
        className="opacity-0 absolute -z-10 pointer-events-none"
        onKeyDown={handleKey}
      />

      {/* Footer hint */}
      <div className="text-[10px] text-subtext/50 font-medium tracking-widest uppercase animate-fade-in-up" style={{ animationDelay: '600ms' }}>
        Type the Kingdom • Break the Clock • Focus Mode: {focusMode ? 'On' : 'Off'}
      </div>
    </div>
  )
}
