import React from 'react';
import { Award, Clock3, BookOpen, ArrowUpRight, FlaskConical, Leaf } from 'lucide-react';

const imagery = {
  agroforestry: 'https://images.unsplash.com/photo-1501004318641-b39e6451bec6?auto=format&fit=crop&w=900&q=80',
  legume: 'https://images.unsplash.com/photo-1492496913980-501348b61469?auto=format&fit=crop&w=900&q=80',
  cover: 'https://images.unsplash.com/photo-1473445361085-b9a07f55608b?auto=format&fit=crop&w=900&q=80',
  habitat: 'https://images.unsplash.com/photo-1448375240586-882707db888b?auto=format&fit=crop&w=900&q=80',
};

export default function RecommendationCard({ recommendation, onSimulate, compact = false }) {
  const { action, scientific_reasoning, impacted_metrics = [], measurable_improvements, time_horizon, confidence_level, evidence = [] } = recommendation;
  const image = action?.toLowerCase().includes('agroforestry') ? imagery.agroforestry
    : action?.toLowerCase().includes('legume') ? imagery.legume
    : action?.toLowerCase().includes('cover') ? imagery.cover
    : imagery.habitat;

  return (
    <article className={`recommendation-card glass-panel ${compact ? 'compact' : ''}`}>
      <div className="recommendation-image" style={{ backgroundImage: `linear-gradient(180deg, transparent 35%, rgba(5,18,13,.96)), url("${image}")` }}>
        <span className="image-chip"><Leaf size={12} /> ECOLOGICAL ACTION</span>
      </div>
      <div className="recommendation-content">
        <div className="recommendation-top">
          <div><span className="eyebrow">INTERVENTION</span><h3>{action}</h3></div>
          <span className="confidence-pill"><Award size={13} /> {confidence_level || 'unknown'}</span>
        </div>
        <p className="reasoning-copy"><strong>Why it matters:</strong> {scientific_reasoning}</p>
        <div className="impact-box"><span>MEASURABLE TARGET</span><p>{measurable_improvements}</p></div>
        <div className="metric-tags">{impacted_metrics.map((m) => <span key={m}>{m.replace(/_/g, ' ')}</span>)}</div>
        <div className="recommendation-footer">
          <span className="horizon"><Clock3 size={13} /> {pretty(time_horizon)}</span>
          {onSimulate && <button className="text-button" onClick={onSimulate}><FlaskConical size={14} /> What if? <ArrowUpRight size={13} /></button>}
        </div>
        {evidence.length > 0 && (
          <details className="evidence-details">
            <summary><BookOpen size={14} /> {evidence.length} scientific source{evidence.length > 1 ? 's' : ''}</summary>
            <div className="evidence-list">{evidence.map((ev, idx) => <div key={idx}><strong>{ev.source_organization} · {ev.year}</strong><span>{ev.title}</span><p>{ev.finding_summary}</p></div>)}</div>
          </details>
        )}
      </div>
    </article>
  );
}
function pretty(v = '') { return v.replace(/_/g, ' '); }
