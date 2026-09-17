import React, { useState } from 'react';
import Header from './components/Header';
import ChatInterface from './components/Chat/ChatInterface';
import ParameterForm from './components/StructuredInput/ParameterForm';
import ReasoningGraph from './components/Reasoning/ReasoningGraph';
import RecommendationCard from './components/Reasoning/RecommendationCard';
import WhatIfSimulator from './components/Simulator/WhatIfSimulator';
import { apiService } from './services/api';
import { BookOpen, Search, AlertCircle } from 'lucide-react';

export default function App() {
  const [activeTab, setActiveTab] = useState('chat');
  const [reasoningResult, setReasoningResult] = useState(null);
  const [reasoningInput, setReasoningInput] = useState(null);
  const [reasoningLoading, setReasoningLoading] = useState(false);
  const [simulatorContext, setSimulatorContext] = useState(null);

  const [knowledgeQuery, setKnowledgeQuery] = useState('agroforestry and soil carbon');
  const [knowledgeResults, setKnowledgeResults] = useState([]);
  const [knowledgeLoading, setKnowledgeLoading] = useState(false);
  const [error, setError] = useState('');

  const handleStructuredSubmit = async (formData) => {
    setReasoningLoading(true);
    setError('');
    setReasoningInput(formData);

    try {
      const res = await apiService.performReasoning(formData);
      setReasoningResult(res);
    } catch (err) {
      setError(err.message);
    } finally {
      setReasoningLoading(false);
    }
  };

  const openSimulator = ({ intervention = null, environment = reasoningInput } = {}) => {
    setSimulatorContext({ intervention, environment });
    setActiveTab('simulator');
  };

  const handleSearchKnowledge = async (e) => {
    e.preventDefault();
    if (!knowledgeQuery.trim()) return;

    setKnowledgeLoading(true);
    setError('');
    try {
      const docs = await apiService.queryKnowledge(knowledgeQuery);
      setKnowledgeResults(Array.isArray(docs) ? docs : docs?.results || []);
    } catch (err) {
      setError(err.message);
    } finally {
      setKnowledgeLoading(false);
    }
  };

  return (
    <div className="app-shell">
      <Header activeTab={activeTab} setActiveTab={setActiveTab} />

      <main className="app-main">
        {error && (
          <div className="error-banner">
            <AlertCircle size={17} />
            <span>{error}</span>
            <button onClick={() => setError('')} aria-label="Dismiss">×</button>
          </div>
        )}

        {activeTab === 'chat' && (
          <ChatInterface onOpenSimulator={openSimulator} />
        )}

        {activeTab === 'structured' && (
          <div className="page-stack">
            <section className="hero-copy">
              <span className="eyebrow">SCIENTIFIC DIAGNOSIS</span>
              <h2>Turn environmental observations into a connected system.</h2>
              <p>
                Provide soil, climate and land-use conditions. Cura.Earth evaluates their
                interactions, retrieves scientific evidence and produces multi-metric interventions.
              </p>
            </section>

            <ParameterForm
              onSubmit={handleStructuredSubmit}
              loading={reasoningLoading}
            />

            {reasoningResult && !reasoningResult.requires_clarification && (
              <section className="page-stack">
                <div className="section-heading">
                  <div>
                    <span className="eyebrow">SYSTEM REASONING</span>
                    <h3>How the ecosystem variables connect</h3>
                  </div>
                  <button
                    className="secondary-button"
                    onClick={() => openSimulator({ environment: reasoningInput })}
                  >
                    Explore What-If
                  </button>
                </div>

                <ReasoningGraph
                  variables={reasoningResult.interconnected_variables}
                  connections={reasoningResult.variable_connections}
                />

                <div>
                  <div className="section-heading compact">
                    <div>
                      <span className="eyebrow">EVIDENCE-GROUNDED ACTIONS</span>
                      <h3>Recommended interventions</h3>
                    </div>
                  </div>

                  <div className="recommendation-grid">
                    {reasoningResult.recommendations?.map((rec, i) => (
                      <RecommendationCard
                        key={i}
                        recommendation={rec}
                        onSimulate={() => openSimulator({
                          intervention: interventionKeyFromAction(rec.action),
                          environment: reasoningInput,
                        })}
                      />
                    ))}
                  </div>
                </div>

                {reasoningResult.system_notes && (
                  <div className="note-box">{reasoningResult.system_notes}</div>
                )}
              </section>
            )}

            {reasoningResult?.requires_clarification && (
              <div className="glass-panel clarification-result">
                <strong>More environmental context is required.</strong>
                <p>{reasoningResult.system_notes}</p>
                <ul>
                  {reasoningResult.clarification_questions?.map((q, i) => (
                    <li key={i}>{q.prompt_text}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}

        {activeTab === 'simulator' && (
          <WhatIfSimulator context={simulatorContext} />
        )}

        {activeTab === 'knowledge' && (
          <div className="page-stack knowledge-page">
            <section className="hero-copy">
              <span className="eyebrow">SCIENTIFIC GROUNDING</span>
              <h2>Evidence Knowledge Base</h2>
              <p>
                Search the indexed FAO, IPCC, IPBES and other environmental evidence used by the reasoning layer.
              </p>
            </section>

            <div className="glass-panel search-panel">
              <form onSubmit={handleSearchKnowledge} className="search-form">
                <input
                  value={knowledgeQuery}
                  onChange={(e) => setKnowledgeQuery(e.target.value)}
                  placeholder="Try: soil carbon in semi-arid agroforestry"
                />
                <button className="primary-button" disabled={knowledgeLoading}>
                  <Search size={16} />
                  {knowledgeLoading ? 'Searching…' : 'Search evidence'}
                </button>
              </form>
            </div>

            <div className="knowledge-results">
              {knowledgeResults.map((item, idx) => (
                <article className="glass-panel evidence-card" key={idx}>
                  <div className="evidence-top">
                    <div>
                      <span className="source-label">
                        <BookOpen size={14} />
                        {item.metadata?.filename || item.doc_id || 'Knowledge document'}
                      </span>
                    </div>
                    {typeof item.score === 'number' && (
                      <span className="score-pill">{(item.score * 100).toFixed(1)}% relevance</span>
                    )}
                  </div>
                  <p>{item.content}</p>
                </article>
              ))}

              {!knowledgeLoading && knowledgeResults.length === 0 && (
                <div className="empty-state">
                  Search the knowledge base to inspect retrieved scientific evidence.
                </div>
              )}
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

function interventionKeyFromAction(action = '') {
  const text = action.toLowerCase();
  if (text.includes('agroforestry') || text.includes('tree-crop')) return 'agroforestry';
  if (text.includes('legume')) return 'legume_intercropping';
  if (text.includes('cover crop')) return 'cover_cropping';
  if (text.includes('hedgerow') || text.includes('habitat corridor')) return 'native_hedgerows';
  return null;
}
