import { useState, useCallback, useRef, useEffect } from 'react'
import type { TestStats, TestMode } from '../types'

export function useTypingEngine() {
  const [isRunning, setIsRunning] = useState(false)
  const [testText, setTestText] = useState('')
  const [typedText, setTypedText] = useState('')
  const [currentIndex, setCurrentIndex] = useState(0)
  const [startTime, setStartTime] = useState(0)
  const [elapsedTime, setElapsedTime] = useState(0)
  const [errors, setErrors] = useState(0)
  const [wpm, setWpm] = useState(0)
  const [accuracy, setAccuracy] = useState(100)
  const [isComplete, setIsComplete] = useState(false)
  const timerRef = useRef<number | null>(null)
  const [lastTest, setLastTest] = useState<TestStats | null>(null)

  const startTest = useCallback((durationSec = 30, mode: TestMode = 'time') => {
    const text = generateTestText(durationSec, mode)
    setTestText(text)
    setTypedText('')
    setCurrentIndex(0)
    setErrors(0)
    setIsRunning(true)
    setIsComplete(false)
    setStartTime(Date.now())
    setElapsedTime(0)
    setLastTest(null)

    if (timerRef.current) {
      clearInterval(timerRef.current)
    }

    timerRef.current = window.setInterval(() => {
      const elapsed = (Date.now() - startTime) / 1000
      setElapsedTime(elapsed)

      if (elapsed >= durationSec && mode === 'time') {
        setIsRunning(false)
        setIsComplete(true)
        setWpm(calculateWPM(typedText.length, elapsed, errors))
        if (timerRef.current) clearInterval(timerRef.current)
      }
    }, 50)
  }, [startTime])

  const handleKeyPress = useCallback((key: string) => {
    if (!isRunning || isComplete) return

    if (key.length > 1) {
      if (key === 'Backspace') {
        setCurrentIndex(prev => Math.max(0, prev - 1))
        setTypedText(prev => prev.slice(0, -1))
        return
      }
      return
    }

    const expectedChar = testText[currentIndex]
    const isCorrect = key === expectedChar

    setTypedText(prev => prev + key)
    setCurrentIndex(prev => prev + 1)

    if (!isCorrect) {
      setErrors(prev => prev + 1)
    }

    // Calculate WPM live
    const elapsed = (Date.now() - startTime) / 1000
    const correctChars = currentIndex + (isCorrect ? 1 : 0)
    const wpmCalc = Math.round((correctChars / 5) / (elapsed / 60))
    setWpm(Math.max(0, wpmCalc))

    // Check if test is done (all characters typed)
    if (currentIndex + 1 >= testText.length) {
      setIsRunning(false)
      setIsComplete(true)
      if (timerRef.current) clearInterval(timerRef.current)
      const stats: TestStats = {
        wpm,
        accuracy: Math.round(((currentIndex + 1 - errors) / (currentIndex + 1)) * 100),
        rawWPM: Math.round((typedText.length / 5) / (elapsed / 60)),
        consistency: 95,
        errors,
        characters: typedText.length + 1,
        correct: correctChars,
        incorrect: errors + (!isCorrect ? 1 : 0),
        time: elapsed,
        mode: 'time',
        wordCount: Math.round(typedText.length / 5),
        startedAt: startTime,
        completedAt: Date.now()
      }
      setLastTest(stats)
    }
  }, [isRunning, isComplete, testText, currentIndex, startTime, errors, typedText, wpm])

  const computeAccuracy = () => {
    const total = currentIndex
    const correct = total - errors
    return total > 0 ? Math.round((correct / total) * 100) : 100
  }

  const reset = useCallback(() => {
    setIsRunning(false)
    setIsComplete(false)
    setTypedText('')
    setCurrentIndex(0)
    setErrors(0)
    setElapsedTime(0)
    setWpm(0)
    setAccuracy(100)
    if (timerRef.current) clearInterval(timerRef.current)
  }, [])

  return {
    testText,
    typedText,
    currentIndex,
    isRunning,
    isComplete,
    errors,
    wpm,
    accuracy: computeAccuracy(),
    elapsedTime,
    lastTest,
    startTest,
    handleKeyPress,
    reset,
    currentWPM: Math.round(wpm),
    accuracyPercent: computeAccuracy()
  }
}

function generateTestText(durationSec: number, mode: string): string {
  const cookieWords = [
    'cookie', 'magic', 'kingdom', 'time', 'speed', 'bites', 'keyboard', 'typing',
    'realm', 'fantasy', 'dream', 'sparkle', 'gold', 'vanilla', 'berry', 'sugar',
    'chocolate', 'cream', 'frosting', 'glitter', 'star', 'moon', 'sun', 'cloud',
    'rainbow', 'crystal', 'gem', 'jewel', 'pearl', 'diamond', 'ruby', 'emerald',
    'golden', 'silver', 'bronze', 'platinum', 'royal', 'noble', 'legendary', 'epic',
    'adventure', 'quest', 'journey', 'mission', 'challenge', 'victory', 'triumph',
    'glory', 'honor', 'pride', 'courage', 'bravery', 'strength', 'power', 'energy'
  ]

  const codeWords = [
    'function', 'const', 'let', 'var', 'if', 'else', 'return', 'export', 'import',
    'class', 'interface', 'type', 'extends', 'implements', 'new', 'this', 'try', 'catch',
    'map', 'filter', 'reduce', 'forEach', 'push', 'pop', 'shift', 'slice', 'splice',
    'string', 'number', 'boolean', 'array', 'object', 'null', 'undefined', 'void', 'any',
    'async', 'await', 'promise', 'then', 'catch', 'resolve', 'reject', 'setTimeout',
    'request', 'response', 'headers', 'body', 'json', 'status', 'method', 'path', 'route',
    'database', 'query', 'table', 'column', 'row', 'index', 'primary', 'foreign', 'key'
  ]

  const cliWords = [
    'git', 'npm', 'node', 'python', 'docker', 'docker-compose', 'kubectl', 'helm',
    'bash', 'zsh', 'fish', 'vim', 'neovim', 'emacs', 'nano', 'cat', 'grep', 'sed',
    'awk', 'find', 'locate', 'ps', 'top', 'htop', 'du', 'df', 'free', 'lsof',
    'chmod', 'chown', 'chgrp', 'mkdir', 'rmdir', 'touch', 'rm', 'cp', 'mv', 'ln',
    'tar', 'gzip', 'bzip2', 'xz', 'zip', 'unzip', 'curl', 'wget', 'ssh', 'scp',
    'systemctl', 'service', 'journalctl', 'dmesg', 'sysctl', 'modprobe', 'lsmod'
  ]

  const timeWords = [
    'chronos', 'time', 'clock', 'moment', 'second', 'minute', 'hour', 'day',
    'week', 'month', 'year', 'era', 'epoch', 'timeline', 'timeline', 'timeline',
    'duration', 'span', 'interval', 'instant', 'period', 'term', 'phase', 'stage',
    'deadline', 'schedule', 'calender', 'timer', 'stopwatch', 'alarm', 'countdown',
    'count', 'tick', 'tock', 'chime', 'bell', 'ring', 'hourglass', 'sundial', 'sun'
  ]

  let pool = cookieWords
  if (mode === 'code') pool = codeWords
  if (mode === 'cli') pool = cliWords
  if (mode === 'timebreaker' || mode === 'cookie') pool = cookieWords

  const wordCount = Math.max(10, Math.min(100, Math.round(durationSec / 2)))
  const result: string[] = []
  for (let i = 0; i < wordCount; i++) {
    const word = pool[Math.floor(Math.random() * pool.length)]
    result.push(word)
  }
  // Add punctuation and capitalization for quote-like text
  return result.join(' ') + '.'
}

function calculateWPM(chars: number, seconds: number, errors: number): number {
  if (seconds <= 0) return 0
  const netChars = Math.max(0, chars - errors)
  const words = netChars / 5
  return Math.round(words / (seconds / 60))
}
