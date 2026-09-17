import React from 'react';
import { GitBranch, ArrowRight, Sparkles, CircleDot } from 'lucide-react';

export default function ReasoningGraph({ variables, connections, compact = false }) {
  if (!variables?.length) return null;
  return (
    <section className={`reasoning-card ${compact ? 'compact' : ''}`}>
      <div className="reasoning-heading">
        <div className="section-icon teal"><GitBranch size={17} /></div>
        <div><span className="eyebrow">CAUSAL CONTEXT</span><h3>Multi-variable ecological interconnections</h3></div>
      </div>

      <div className="causal-visual">
        {variables.slice(0, 5).map((v, i) => (
          <React.Fragment key={v}>
            <div className="causal-node" style={{ '--delay': `${i * 0.12}s` }}>
              <CircleDot size={12} /><span>{v.replace(/_/g, ' ')}</span>
            </div>
            {i < Math.min(variables.length, 5) - 1 && <ArrowRight className="causal-arrow" size={14} />}
          </React.Fragment>
        ))}
      </div>

      <div className="connection-list">
        {connections?.map((c, idx) => (
          <div className="connection-row" key={idx}>
            <div className="connection-path"><strong>{pretty(c.source_metric)}</strong><ArrowRight size={14} /><strong>{pretty(c.target_metric)}</strong></div>
            <span className={`relationship ${c.relationship_type || ''}`}>{pretty(c.relationship_type || 'linked')}</span>
            <p>{c.mechanism}</p>
          </div>
        ))}
      </div>
      <div className="reasoning-footnote"><Sparkles size={13} /> The engine reasons across connected variables rather than treating each metric independently.</div>
    </section>
  );
}
function pretty(v = '') { return v.replace(/_/g, ' '); }
