import React, { useState } from 'react';
import { Play, RotateCcw, Info, CheckCircle2, AlertCircle, FlaskConical, Sparkles } from 'lucide-react';
import MetricProjection from './MetricProjection';

const BACKEND_URL = import.meta.env.VITE_API_BASE_URL || (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' ? 'http://127.0.0.1:8000' : 'https://cura-earth.onrender.com');
const OPTIONS = [
  { key: 'agroforestry', label: 'Agroforestry / tree-crop integration' },
  { key: 'legume_intercropping', label: 'Legume intercropping' },
  { key: 'cover_cropping', label: 'Cover cropping + reduced disturbance' },
  { key: 'native_hedgerows', label: 'Native hedgerows / habitat corridors' },
];

export default function WhatIfSimulator({ context }) {
  const [intervention, setIntervention] = useState(context?.intervention || 'agroforestry');
  const [timeframe, setTimeframe] = useState(5);
  const [simulationData, setSimulationData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [status, setStatus] = useState('Select an intervention and run the ecological simulation.');

  const runSimulation = async () => {
    setLoading(true); setError(''); setSimulationData(null); setStatus('Connecting to Cura.Earth ecological engine...');
    const payload = { scenario_key: 'semi_arid_monoculture_agroforestry', timeframe_years: Number(timeframe), intervention };
    try {
      const response = await fetch(`${BACKEND_URL}/api/v1/simulator/simulate`, { method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(payload) });
      const text = await response.text();
      let data;
      try { data = JSON.parse(text); } catch { throw new Error(`Backend returned invalid JSON. HTTP ${response.status}`); }
      if (!response.ok) throw new Error(data?.detail || data?.message || `Backend returned HTTP ${response.status}`);
      if (!data || !Array.isArray(data.yearly_projections)) throw new Error('Simulation response is missing yearly projections.');
      setSimulationData(data);
      setStatus(`Simulation completed successfully for ${data.timeframe_years} years.`);
    } catch (err) {
      setError(err?.message || 'Could not connect to the Cura.Earth backend.');
      setStatus('Simulation failed.');
    } finally { setLoading(false); }
  };

  const resetSimulation = () => { setIntervention('agroforestry'); setTimeframe(5); setSimulationData(null); setError(''); setStatus('Select an intervention and run the ecological simulation.'); };

  return (
    <div className="page-stack simulator-page">
      <section className="diagnosis-hero simulator-hero">
        <div className="hero-copy hero-copy-large">
          <span className="eyebrow"><span className="pulse-dot" /> WHAT-IF ECOLOGY</span>
          <h2>Change one decision.<br /><em>Watch the ecosystem respond.</em></h2>
          <p>Explore how land-management changes can alter soil carbon, water retention, biodiversity, microbial diversity, pollinator richness and habitat connectivity over time.</p>
        </div>
        <div className="simulation-visual">
          <div className="sim-sun" /><div className="sim-ground" /><div className="sim-tree tree-one" /><div className="sim-tree tree-two" /><div className="sim-field" />
          <span className="sim-caption"><Sparkles size={13} /> FUTURE STATE ENGINE</span>
        </div>
      </section>

      <section className="glass-panel simulator-controls">
        <div className="simulator-control-grid">
          <label className="field"><span>INTERVENTION</span><select value={intervention} onChange={(e)=>{setIntervention(e.target.value);setSimulationData(null);setError('');setStatus('Intervention changed. Press Run simulation.')}} disabled={loading}>{OPTIONS.map(o=><option key={o.key} value={o.key}>{o.label}</option>)}</select></label>
          <label className="field"><span>TIMEFRAME</span><select value={timeframe} onChange={(e)=>{setTimeframe(Number(e.target.value));setSimulationData(null);setError('');setStatus('Timeframe changed. Press Run simulation.')}} disabled={loading}><option value={1}>1 year</option><option value={3}>3 years</option><option value={5}>5 years</option><option value={10}>10 years</option></select></label>
          <div className="simulator-actions"><button type="button" className="primary-button" disabled={loading} onClick={runSimulation}><Play size={15} />{loading?'Running...':'Run simulation'}</button><button type="button" className="icon-button" onClick={resetSimulation} disabled={loading} title="Reset simulation"><RotateCcw size={15}/></button></div>
        </div>
        <div className="sim-status">{loading ? <span className="status-pulse" /> : simulationData ? <CheckCircle2 size={15}/> : error ? <AlertCircle size={15}/> : <Info size={15}/>}<span>{status}</span></div>
      </section>

      {error && <div className="error-banner"><AlertCircle size={17}/><span>{error}</span><button type="button" onClick={()=>setError('')}>×</button></div>}
      {simulationData && <MetricProjection projections={simulationData.yearly_projections} baseline={simulationData.baseline_metrics} summary={simulationData.cascade_summary} confidence={simulationData.confidence_level} scenarioName={simulationData.scenario_name}/>}
    </div>
  );
}

