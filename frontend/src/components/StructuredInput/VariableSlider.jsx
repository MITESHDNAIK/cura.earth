import React from 'react';
export default function VariableSlider({ label, value, min, max, step, unit, onChange }) {
  const pct = ((value - min) / (max - min)) * 100;
  return (
    <div className="slider-field">
      <div className="slider-label"><span>{label}</span><strong>{value} {unit}</strong></div>
      <input type="range" min={min} max={max} step={step} value={value} onChange={(e) => onChange(Number(e.target.value))} style={{ '--range-progress': `${pct}%` }} />
    </div>
  );
}
