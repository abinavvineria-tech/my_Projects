import { useState, useCallback } from 'react'

type SoundPreset = 'silent' | 'soft' | 'mechanical' | 'digital' | 'magic' | 'arcade'

export function useSound() {
  const [volume, setVolume] = useState(0.7)
  const [preset, setPreset] = useState<SoundPreset>('soft')
  const [enabled, setEnabled] = useState(true)
  const audioContextRef = useState<AudioContext | null>(null)

  const getAudioContext = useCallback(() => {
    if (!audioContextRef[0]) {
      audioContextRef[1](new (window.AudioContext || (window as any).webkitAudioContext)())
    }
    return audioContextRef[0]
  }, [])

  const playTone = useCallback((frequency: number, duration: number, type: OscillatorType = 'sine') => {
    if (!enabled) return
    
    const ctx = getAudioContext()
    if (!ctx) return

    const oscillator = ctx.createOscillator()
    const gainNode = ctx.createGain()
    
    oscillator.connect(gainNode)
    gainNode.connect(ctx.destination)
    
    oscillator.frequency.value = frequency
    oscillator.type = type
    
    gainNode.gain.setValueAtTime(volume * 0.3, ctx.currentTime)
    gainNode.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + duration)
    
    oscillator.start(ctx.currentTime)
    oscillator.stop(ctx.currentTime + duration)
  }, [enabled, volume, getAudioContext])

  const playSound = useCallback((type: 'key' | 'error' | 'success' | 'complete') => {
    if (!enabled) return

    const presets: Record<SoundPreset, Record<string, { freq: number; dur: number; type: OscillatorType }>> = {
      silent: {},
      soft: {
        key: { freq: 800, dur: 0.05, type: 'sine' },
        error: { freq: 200, dur: 0.15, type: 'sawtooth' },
        success: { freq: 1000, dur: 0.1, type: 'sine' },
        complete: { freq: 600, dur: 0.3, type: 'triangle' }
      },
      mechanical: {
        key: { freq: 1200, dur: 0.03, type: 'square' },
        error: { freq: 150, dur: 0.2, type: 'sawtooth' },
        success: { freq: 1500, dur: 0.08, type: 'square' },
        complete: { freq: 800, dur: 0.4, type: 'triangle' }
      },
      digital: {
        key: { freq: 1000, dur: 0.02, type: 'sine' },
        error: { freq: 300, dur: 0.1, type: 'square' },
        success: { freq: 2000, dur: 0.05, type: 'sine' },
        complete: { freq: 500, dur: 0.5, type: 'triangle' }
      },
      magic: {
        key: { freq: 1200, dur: 0.08, type: 'sine' },
        error: { freq: 250, dur: 0.2, type: 'sine' },
        success: { freq: 1500, dur: 0.15, type: 'sine' },
        complete: { freq: 880, dur: 0.6, type: 'sine' }
      },
      arcade: {
        key: { freq: 440, dur: 0.05, type: 'square' },
        error: { freq: 110, dur: 0.2, type: 'sawtooth' },
        success: { freq: 880, dur: 0.1, type: 'square' },
        complete: { freq: 660, dur: 0.4, type: 'triangle' }
      }
    }

    const sound = presets[preset]?.[type]
    if (sound) {
      playTone(sound.freq, sound.dur, sound.type)
    }
  }, [enabled, preset, playTone])

  return { playSound, volume, setVolume, preset, setPreset, enabled, setEnabled }
}