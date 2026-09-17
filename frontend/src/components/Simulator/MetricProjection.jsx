import React, { useMemo, useState } from 'react';
import { TrendingUp, ShieldCheck, Table2, LineChart, ArrowUpRight, Sparkles } from 'lucide-react';

export default function MetricProjection({ projections, baseline, summary, confidence, scenarioName }) {
  const [view, setView] = useState('chart');
  if (!projections?.length) return null;
  const metricKeys = Object.keys(projections[0].projected_metrics || {});
  const chartKeys = metricKeys.slice(0, 5);

  return (
    <section className="glass-panel projection-panel">
      <div className="projection-header">
        <div><span className="eyebrow">CASCADE OUTPUT · FUTURE STATE</span><h3>Watch the ecosystem evolve</h3><p>{scenarioName}</p></div>
        <span className="confidence-pill"><ShieldCheck size={13} /> {confidence || 'illustrative'}</span>
      </div>
      <div className="future-strip"><div><span>BASELINE</span><strong>Present ecosystem</strong></div><ArrowUpRight /><div><span>INTERVENTION</span><strong>Management change</strong></div><ArrowUpRight /><div><span>PROJECTION</span><strong>{projections.length - 1} years ahead</strong></div></div>
      <div className="projection-summary"><TrendingUp size={16} /><span>{summary}</span></div>
      <div className="view-toggle"><button className={view === 'chart' ? 'active' : ''} onClick={() => setView('chart')}><LineChart size={14} /> Trend view</button><button className={view === 'table' ? 'active' : ''} onClick={() => setView('table')}><Table2 size={14} /> Data table</button></div>
      {view === 'chart' ? <TrendChart projections={projections} keys={chartKeys} /> : <DataTable projections={projections} metricKeys={metricKeys} baseline={baseline} />}
      <p className="model-disclaimer"><Sparkles size={12} /> Illustrative cascade model. Projected values demonstrate connected ecological dynamics and should not be interpreted as measured or guaranteed site-specific outcomes.</p>
    </section>
  );
}

function TrendChart({ projections, keys }) {
  const width = 900, height = 330, padding = { top: 24, right: 30, bottom: 48, left: 62 };
  const series = useMemo(() => keys.map((key) => ({ key, values: projections.map((p) => Number(p.projected_metrics[key]) || 0) })), [keys, projections]);
  const all = series.flatMap((s) => s.values), min = Math.min(...all), max = Math.max(...all), range = max - min || 1;
  const x = (i) => padding.left + (i / Math.max(projections.length - 1, 1)) * (width - padding.left - padding.right);
  const y = (v) => height - padding.bottom - ((v - min) / range) * (height - padding.top - padding.bottom);
  return (
    <div className="chart-wrap">
      <svg viewBox={`0 0 ${width} ${height}`} className="trend-chart" role="img" aria-label="Ecological metric projection chart">
        <defs><filter id="glow"><feGaussianBlur stdDeviation="3" result="blur" /><feMerge><feMergeNode in="blur" /><feMergeNode in="SourceGraphic" /></feMerge></filter></defs>
        {[0,.25,.5,.75,1].map((f) => { const yy = padding.top + f*(height-padding.top-padding.bottom); return <g key={f}><line x1={padding.left} x2={width-padding.right} y1={yy} y2={yy} className="chart-grid" /><text x={padding.left-10} y={yy+4} textAnchor="end" className="chart-label">{formatNumber(max-f*range)}</text></g>; })}
        {projections.map((p,i) => <text key={p.year} x={x(i)} y={height-17} textAnchor="middle" className="chart-label">Y{p.year}</text>)}
        {series.map((s,si) => <g key={s.key}><polyline points={s.values.map((v,i)=>`${x(i)},${y(v)}`).join(' ')} fill="none" className={`series-line series-${si}`} filter="url(#glow)" />{s.values.map((v,i)=><circle key={i} cx={x(i)} cy={y(v)} r="3.5" className={`series-dot series-${si}`} />)}</g>)}
      </svg>
      <div className="chart-legend">{series.map((s,i)=><span key={s.key}><i className={`legend-dot series-${i}`} />{s.key.replace(/_/g,' ')}</span>)}</div>
    </div>
  );
}
function DataTable({ projections, metricKeys, baseline }) {
  return <div className="table-scroll"><table className="projection-table"><thead><tr><th>Year</th><th>Ecological state</th>{metricKeys.map(k=><th key={k}>{k.replace(/_/g,' ')}</th>)}</tr></thead><tbody>{projections.map(p=><tr key={p.year}><td>Year {p.year}</td><td><span className="state-pill">{p.ecological_state}</span></td>{metricKeys.map(k=><td key={k}>{formatNumber(p.projected_metrics[k])}</td>)}</tr>)}</tbody></table>{baseline&&<div className="baseline-row"><strong>Baseline</strong>{metricKeys.map(k=><span key={k}>{k.replace(/_/g,' ')}: {formatNumber(baseline[k])}</span>)}</div>}</div>;
}
function formatNumber(v){return Number(v).toFixed(2);}
