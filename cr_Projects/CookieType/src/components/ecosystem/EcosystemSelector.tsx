import React, { useState } from 'react'
import { X, Sparkles, Code, Clock, Flower } from 'lucide-react'

interface EcosystemSelectorProps {
  isOpen: boolean
  onClose: () => void
  onSelect: (ecosystem: string) => void
}

const ecosystems = [
  { 
    id: 'purelily', 
    name: 'PureLily', 
    icon: Flower,
    description: 'Peaceful & Elegant',
    colors: ['#7C3AED', '#F0ABFC', '#FDF8FF']
  },
  { 
    id: 'cookie', 
    name: 'Cookie Kingdom', 
    icon: Sparkles,
    description: 'Magical Fantasy',
    colors: ['#C2410C', '#FED7AA', '#FFF8F0']
  },
  { 
    id: 'bites', 
    name: 'B!TES Studio', 
    icon: Code,
    description: 'Developer Aesthetic',
    colors: ['#A855F7', '#EC4899', '#0A0514']
  },
  { 
    id: 'timebreaker', 
    name: 'Timebreaker', 
    icon: Clock,
    description: 'Futuristic Time',
    colors: ['#6366F1', '#EC4899', '#050312']
  }
]

export function EcosystemSelector({ isOpen, onClose, onSelect }: EcosystemSelectorProps) {
  const [selected, setSelected] = useState('purelily')

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 z-[100] flex items-center justify-center p-4" onClick={onClose}>
      <div className="absolute inset-0 bg-black/60 backdrop-blur-sm" />
      
      <div className="relative glass rounded-3xl p-8 max-w-3xl w-full animate-fade-in" onClick={e => e.stopPropagation()}>
        <button onClick={onClose} className="absolute top-4 right-4 p-2 rounded-lg hover:bg-white/5 transition">
          <X className="w-5 h-5" />
        </button>

        <h2 className="text-2xl font-extrabold text-center mb-2">Choose Your Ecosystem</h2>
        <p className="text-sm text-subtext text-center mb-8">Transform your typing experience</p>

        <div className="grid grid-cols-2 gap-4">
          {ecosystems.map(eco => (
            <button
              key={eco.id}
              onClick={() => setSelected(eco.id)}
              className={`glass rounded-2xl p-6 text-left transition-all ${
                selected === eco.id ? 'ring-2 ring-amber-300/50 scale-[1.02]' : 'hover:bg-white/5'
              }`}
            >
              <div className="flex items-center gap-3 mb-3">
                <div 
                  className="w-10 h-10 rounded-xl flex items-center justify-center"
                  style={{ background: `linear-gradient(135deg, ${eco.colors[0]}, ${eco.colors[1]})` }}
                >
                  <eco.icon className="w-5 h-5 text-white" />
                </div>
                <div>
                  <div className="font-bold">{eco.name}</div>
                  <div className="text-xs text-subtext">{eco.description}</div>
                </div>
              </div>
              <div className="flex gap-1.5">
                {eco.colors.map((color, i) => (
                  <div key={i} className="w-6 h-6 rounded-full border-2" style={{ backgroundColor: color, borderColor: 'rgba(255,255,255,0.1)' }} />
                ))}
              </div>
            </button>
          ))}
        </div>

        <button
          onClick={() => { onSelect(selected); onClose(); }}
          className="w-full mt-8 py-3 rounded-xl bg-gradient-to-r from-amber-300 to-pink-500 text-white font-bold hover:opacity-90 transition"
        >
          Apply {ecosystems.find(e => e.id === selected)?.name}
        </button>
      </div>
    </div>
  )
}