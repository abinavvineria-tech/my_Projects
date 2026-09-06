import React, { useEffect, useState } from 'react'

export function TypeEffect({ text, onComplete }: { text: string; onComplete?: () => void }) {
  const [displayText, setDisplayText] = useState('')

  useEffect(() => {
    let index = 0
    const interval = setInterval(() => {
      index++
      setDisplayText(text.slice(0, index))
      if (index >= text.length) {
        clearInterval(interval)
        onComplete?.()
      }
    }, 60)
    return () => clearInterval(interval)
  }, [text, onComplete])

  return <span className="font-mono text-sm md:text-xl">{displayText}</span>
}

export function LoadingScreen() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-black to-pink-900 flex items-center justify-center">
      <div className="text-center">
        <div className="w-16 h-16 rounded-full border-2 border-amber-300/30 border-t-amber-300 animate-spin mx-auto mb-4"></div>
        <TypeEffect text="Loading CookieType..." className="text-amber-300" />
      </div>
    </div>
  )
}

export function TypingDemo() {
  const [started, setStarted] = useState(false)

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-black to-pink-900 flex items-center justify-center">
      {!started ? (
        <button 
          onClick={() => setStarted(true)}
          className="px-8 py-4 bg-gradient-to-r from-amber-300 to-pink-500 rounded-full text-white font-bold text-lg hover:scale-105 transition"
        >
          Start Typing
        </button>
      ) : (
        <div className="text-center">
          <TypeEffect text="Welcome to CookieType" className="text-4xl text-amber-300" onComplete={() => {}} />
        </div>
      )}
    </div>
  )
}
