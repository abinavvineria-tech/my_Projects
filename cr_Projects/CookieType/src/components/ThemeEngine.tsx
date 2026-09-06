import React, { useEffect } from 'react'

interface ThemeEngineProps {
  themes: Record<string, any>
}

export function ThemeEngine({ themes }: ThemeEngineProps) {
  useEffect(() => {
    const style = document.createElement('style')
    style.id = 'theme-dynamic-styles'
    style.textContent = `
      @keyframes fade-in {
        from { opacity: 0; transform: translateY(8px); }
        to { opacity: 1; transform: translateY(0); }
      }
      .animate-fade-in { animation: fade-in 0.5s ease-out forwards; }
      
      @keyframes pulse-glow {
        0%, 100% { box-shadow: 0 0 20px rgba(168, 85, 247, 0.3); }
        50% { box-shadow: 0 0 40px rgba(168, 85, 247, 0.6); }
      }
      .glow { animation: pulse-glow 2s ease-in-out infinite; }
      
      @keyframes typing-cursor {
        0%, 100% { opacity: 1; }
        50% { opacity: 0; }
      }
      .cursor-blink { animation: typing-cursor 1s step-end infinite; }
      
      @keyframes sparkle {
        0%, 100% { opacity: 0; transform: scale(0) rotate(0deg); }
        50% { opacity: 1; transform: scale(1) rotate(180deg); }
      }
      .sparkle { animation: sparkle 2s ease-in-out infinite; }
      
      @keyframes float-gentle {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        33% { transform: translateY(-6px) rotate(1deg); }
        66% { transform: translateY(-3px) rotate(-1deg); }
      }
      .float-gentle { animation: float-gentle 8s ease-in-out infinite; }
      
      @keyframes gradient-shift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
      }
      .gradient-animate { 
        background-size: 200% 200%;
        animation: gradient-shift 8s ease infinite;
      }
      
      .text-subtext { color: var(--subtext, #8B7FB0); }
      
      .typing-char-correct { color: var(--success, #34D399); }
      .typing-char-incorrect { color: var(--error, #F87171); background: rgba(248, 113, 113, 0.1); }
      .typing-char-current { color: var(--caret, #F59E0B); }
      .typing-char-pending { color: var(--subtext); opacity: 0.3; }
    `
    document.head.appendChild(style)
    return () => { document.head.removeChild(style) }
  }, [])

  return null
}