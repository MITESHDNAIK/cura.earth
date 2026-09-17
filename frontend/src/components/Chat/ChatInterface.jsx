import React, { useState } from 'react';
import {
  Send,
  Sparkles,
  RotateCcw,
  Database,
  ArrowDown,
  Leaf,
  Waves,
  Sprout,
  TreePine,
  Droplets,
  Bird,
  FlaskConical,
} from 'lucide-react';
import MessageList from './MessageList';
import { apiService } from '../../services/api';
import './ChatPrompts.css';

const SCENARIO_PROMPTS = [
  {
    id: 'benchmark',
    label: 'Benchmark',
    short: 'Dry monoculture',
    intervention: 'Agroforestry',
    icon: TreePine,
    prompt:
      'The soil organic carbon is 0.3%. Rainfall is low and I grow wheat as a monoculture. Diagnose the ecological system and recommend an intervention that can improve soil carbon, water availability and biodiversity.',
  },
  {
    id: 'intercropping',
    label: 'Low carbon farm',
    short: 'Diversify crops',
    intervention: 'Legume intercropping',
    icon: Sprout,
    prompt:
      'My farm has low soil organic carbon and I grow the same crop every season. I want to improve soil fertility and biodiversity without abandoning crop production. What intervention should I consider and why?',
  },
  {
    id: 'water',
    label: 'Water stress',
    short: 'Dry soil',
    intervention: 'Cover cropping',
    icon: Droplets,
    prompt:
      'My agricultural soil dries out quickly and water retention is poor. Rainfall is irregular and the soil has low organic carbon. What land-management intervention could improve water retention, soil carbon and biodiversity together?',
  },
  {
    id: 'pollinators',
    label: 'Pollinator decline',
    short: 'Habitat fragmentation',
    intervention: 'Native hedgerows',
    icon: Bird,
    prompt:
      'Pollinators are declining around my farm and the surrounding habitat is fragmented. I use conventional agriculture. What intervention could restore habitat connectivity and support biodiversity while also improving the farm ecosystem?',
  },
  {
    id: 'pesticides',
    label: 'Chemical pressure',
    short: 'Pesticide runoff',
    intervention: 'Pesticide reduction',
    icon: FlaskConical,
    prompt:
      'My farm has high pesticide use and chemical runoff is reaching nearby water. I am concerned about soil organisms, water quality and biodiversity. What intervention should I use and what ecological metrics should I monitor?',
  },
];

export default function ChatInterface({ onOpenSimulator }) {
  const [messages, setMessages] = useState([{
    role: 'assistant',
    content: 'Describe an environmental problem in natural language. I will identify missing context, connect the ecological variables, and ground interventions in scientific evidence.',
  }]);
  const [inputText, setInputText] = useState('');
  const [loading, setLoading] = useState(false);
  const [sessionId, setSessionId] = useState(() => makeSessionId());
  const [environmentalProfile, setEnvironmentalProfile] = useState({ query: '', session_id: sessionId });

  const handleSend = async (customText = null) => {
    const text = (customText ?? inputText).trim();
    if (!text || loading) return;
    setMessages((prev) => [...prev, { role: 'user', content: text }]);
    if (!customText) setInputText('');
    setLoading(true);
    try {
      const response = await apiService.sendConversationMessage({ query: text, session_id: sessionId });
      const backendProfile = response?.environmental_profile || response?.profile || response?.environment || null;
      if (backendProfile && typeof backendProfile === 'object') setEnvironmentalProfile({ ...backendProfile, session_id: sessionId });

      if (response?.requires_clarification) {
        setMessages((prev) => [...prev, {
          role: 'assistant',
          content: 'I need a little more environmental context before making the diagnosis.',
          clarificationQuestions: response?.clarification_questions || [],
        }]);
      } else {
        setMessages((prev) => [...prev, {
          role: 'assistant',
          content: 'The environmental profile is sufficiently specified for multi-metric reasoning.',
          diagnosis: response,
        }]);
      }
    } catch (err) {
      setMessages((prev) => [...prev, { role: 'assistant', content: 'The scientific reasoning request failed: ' + (err?.message || 'Unknown error.'), isError: true }]);
    } finally {
      setLoading(false);
    }
  };

  const resetConversation = () => {
    const id = makeSessionId();
    setSessionId(id);
    setEnvironmentalProfile({ query: '', session_id: id });
    setMessages([{ role: 'assistant', content: 'New session started. Describe the environmental problem, then add soil, climate and land-use information when I ask for it.' }]);
    setInputText('');
    setLoading(false);
  };

  const handleScenarioClick = (scenario) => {
    handleSend(scenario.prompt);
  };

  return (
    <div className="chat-page">
      <section className="chat-hero">
        <div className="chat-hero-copy">
          <span className="eyebrow"><span className="pulse-dot" /> CONVERSATIONAL ECOLOGY ENGINE</span>
          <h1>Ask the Earth<br /><em>what it needs.</em></h1>
          <p>Cura.Earth thinks across soil, water, climate, land use and biodiversity — then shows you the chain of reasoning.</p>
          <div className="chat-status-row">
            <span><Sparkles size={13} /> Multi-metric reasoning</span>
            <span><Database size={13} /> Scientific evidence</span>
            <span><Leaf size={13} /> Intervention simulation</span>
          </div>
        </div>
        <div className="chat-hero-graphic">
          <div className="graphic-ring ring-one" />
          <div className="graphic-ring ring-two" />
          <div className="graphic-core"><Leaf size={48} /></div>
          <span className="graphic-label label-one"><Waves size={13} /> WATER</span>
          <span className="graphic-label label-two"><Sprout size={13} /> SOIL</span>
          <span className="graphic-label label-three"><Leaf size={13} /> LIFE</span>
        </div>
      </section>

      <div className="chat-shell glass-panel">
        <div className="chat-toolbar">
          <div><span className="live-dot" /> LIVE ECOLOGICAL SESSION</div>
          <button className="icon-button" onClick={resetConversation} title="New conversation" type="button"><RotateCcw size={16} /></button>
        </div>
        <div className="chat-scroll">
          <MessageList messages={messages} onSelectClarification={(field, value) => handleSend(clarificationToNaturalLanguage(field, value))} onOpenSimulator={(options = {}) => onOpenSimulator?.({ ...options, environment: options.environment || environmentalProfile })} />
          {loading && (
            <div className="typing-indicator">
              <span className="bot-dot"><Sparkles size={15} /></span>
              <span>Mapping variables · retrieving evidence · reasoning…</span><i /><i /><i />
            </div>
          )}
        </div>
        <div className="chat-composer">
          <div className="composer-inner">
            <input value={inputText} onChange={(e) => setInputText(e.target.value)} onKeyDown={(e) => e.key === 'Enter' && handleSend()} placeholder="e.g. SOC is 0.3%, rainfall is low, and I grow wheat as a monoculture…" disabled={loading} />
            <button className="primary-button send-button" onClick={() => handleSend()} disabled={loading || !inputText.trim()} type="button"><Send size={16} /> Send</button>
          </div>
          <div className="scenario-explorer">
            <div className="scenario-heading">
              <div>
                <span className="scenario-kicker">EXPLORE AN ECOLOGICAL SCENARIO</span>
                <span className="scenario-subtitle">
                  Start with a real environmental pattern
                </span>
              </div>
              <span className="scenario-count">5 scenarios</span>
            </div>

            <div className="scenario-grid">
              {SCENARIO_PROMPTS.map((scenario) => {
                const Icon = scenario.icon;

                return (
                  <button
                    key={scenario.id}
                    type="button"
                    className="scenario-card"
                    onClick={() => handleScenarioClick(scenario)}
                    disabled={loading}
                    title={`Explore ${scenario.intervention}`}
                  >
                    <span className="scenario-icon">
                      <Icon size={16} strokeWidth={1.8} />
                    </span>

                    <span className="scenario-copy">
                      <span className="scenario-label">{scenario.label}</span>
                      <span className="scenario-short">{scenario.short}</span>
                    </span>

                    <span className="scenario-arrow">↗</span>
                  </button>
                );
              })}
            </div>
          </div>

          <div className="composer-hint">
            <ArrowDown size={12} />
            <span>Or describe your own environmental problem above.</span>
          </div>
        </div>
      </div>
    </div>
  );
}

function clarificationToNaturalLanguage(fieldKey, value) {
  const key = String(fieldKey || '').toLowerCase();
  if (key.includes('rain') || key.includes('climate')) return 'Rainfall is ' + value + '.';
  if (key.includes('soil') || key.includes('carbon') || key.includes('soc')) return 'My soil condition is ' + value + '.';
  if (key.includes('moisture')) return 'Soil moisture is ' + value + '.';
  if (key.includes('crop') || key.includes('land') || key.includes('management')) return 'I use ' + value + ' for my crop or land management.';
  return String(fieldKey) + ' is ' + value + '.';
}
function makeSessionId() {
  if (typeof crypto !== 'undefined' && typeof crypto.randomUUID === 'function') return 'cura-' + crypto.randomUUID();
  return 'cura-' + Date.now() + '-' + Math.random().toString(36).slice(2, 10);
}
