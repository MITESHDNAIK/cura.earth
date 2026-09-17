import React from 'react';
import { HelpCircle } from 'lucide-react';

export default function ClarificationCard({ questions, onSelectOption }) {
  if (!questions?.length) return null;
  return (
    <div className="clarification-card">
      <div className="clarification-title"><HelpCircle size={17} /><strong>Missing environmental context</strong></div>
      <p>Choose an option or type the value yourself.</p>
      <div className="clarification-list">
        {questions.map((q, idx) => (
          <div className="clarification-item" key={idx}>
            <span>{q.prompt_text}</span>
            {q.recommended_options?.length > 0 && <div className="option-row">{q.recommended_options.map((option)=><button key={option} onClick={()=>onSelectOption(q.field_key,option)} type="button">{option}</button>)}</div>}
          </div>
        ))}
      </div>
    </div>
  );
}
