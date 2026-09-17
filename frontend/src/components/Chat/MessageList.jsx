import React from 'react';
import { User, Bot, AlertCircle, Activity, Sparkles, ArrowUpRight } from 'lucide-react';
import ClarificationCard from './ClarificationCard';
import ReasoningGraph from '../Reasoning/ReasoningGraph';
import RecommendationCard from '../Reasoning/RecommendationCard';

export default function MessageList({ messages, onSelectClarification, onOpenSimulator }) {
  return (
    <div className="message-list">
      {messages.map((msg, idx) => {
        const isUser = msg.role === 'user';
        return (
          <div className={`message-row ${isUser ? 'user' : 'assistant'} message-enter`} key={idx}>
            {!isUser && <div className="avatar bot-avatar"><Bot size={17} /></div>}
            <div className={`message-bubble ${msg.isError ? 'message-error' : ''}`}>
              <div className="message-meta">{isUser ? 'YOU' : 'CURA.EARTH · SCIENTIST'}</div>
              <p>{msg.content}</p>
              {msg.clarificationQuestions && <ClarificationCard questions={msg.clarificationQuestions} onSelectOption={onSelectClarification} />}
              {msg.diagnosis && <DiagnosisBlock diagnosis={msg.diagnosis} onOpenSimulator={onOpenSimulator} />}
            </div>
            {isUser && <div className="avatar user-avatar"><User size={17} /></div>}
          </div>
        );
      })}
    </div>
  );
}

function DiagnosisBlock({ diagnosis, onOpenSimulator }) {
  return (
    <div className="diagnosis-block">
      <div className="diagnosis-header">
        <div><span className="eyebrow">MULTI-METRIC DIAGNOSIS</span><h3>Connected ecological system</h3></div>
        <span className="ready-pill"><Activity size={13} /> Analysis ready</span>
      </div>
      <div className="variable-strip">{diagnosis.interconnected_variables?.map((v) => <span key={v}>{pretty(v)}</span>)}</div>
      <ReasoningGraph variables={diagnosis.interconnected_variables} connections={diagnosis.variable_connections} compact />
      <div className="chat-recommendations">
        {diagnosis.recommendations?.map((rec, idx) => (
          <RecommendationCard key={idx} recommendation={rec} compact onSimulate={() => onOpenSimulator?.({ intervention: interventionKeyFromAction(rec.action) })} />
        ))}
      </div>
      {diagnosis.system_notes && <div className="mini-note"><Sparkles size={14} /> {diagnosis.system_notes}</div>}
    </div>
  );
}
function pretty(v = '') { return v.replace(/_/g, ' '); }
function interventionKeyFromAction(action = '') {
  const t = action.toLowerCase();
  if (t.includes('agroforestry') || t.includes('tree-crop')) return 'agroforestry';
  if (t.includes('legume')) return 'legume_intercropping';
  if (t.includes('cover crop')) return 'cover_cropping';
  if (t.includes('hedgerow') || t.includes('habitat corridor')) return 'native_hedgerows';
  return null;
}
