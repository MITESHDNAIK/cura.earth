import React, { useState } from 'react';
import { SlidersHorizontal, Compass, CloudRain, Sprout, MapPin, Gauge } from 'lucide-react';
import VariableSlider from './VariableSlider';

export default function ParameterForm({ onSubmit, loading }) {
  const [soc, setSoc] = useState(0.3), [ph, setPh] = useState(6.5), [moisture, setMoisture] = useState(25);
  const [rainfallCategory, setRainfallCategory] = useState('low'), [rainfallMm, setRainfallMm] = useState(500), [temperature, setTemperature] = useState(28);
  const [cropType, setCropType] = useState('wheat'), [management, setManagement] = useState('monoculture'), [fragmentation, setFragmentation] = useState('high');
  const [region, setRegion] = useState('semi-arid agricultural landscape'), [latitude, setLatitude] = useState(19.076), [longitude, setLongitude] = useState(72.877);

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit({
      query: 'Structured environmental diagnosis for soil, climate, land use and biodiversity interactions.',
      soil: { organic_carbon_pct: soc, ph, moisture_pct: moisture, texture: 'loamy' },
      climate: { rainfall_category: rainfallCategory, annual_rainfall_mm: rainfallMm, temperature_celsius: temperature },
      land_use: { current_cover: `${cropType} ${management}`, crop_type: cropType, tillage_practice: 'conventional', habitat_fragmentation: fragmentation },
      spatial: { region, latitude, longitude },
    });
  };

  return (
    <form onSubmit={handleSubmit} className="glass-panel parameter-form">
      <div className="form-header">
        <div><span className="eyebrow">INPUT PROFILE · 01</span><h3>Describe the ecosystem</h3></div>
        <span className="form-badge"><Gauge size={13} /> 4 dimensions</span>
      </div>

      <div className="parameter-grid">
        <section className="parameter-section">
          <div className="section-icon"><SlidersHorizontal size={17} /></div>
          <div className="parameter-section-title"><h4>Soil system</h4><span>SOC · chemistry · moisture</span></div>
          <VariableSlider label="Soil Organic Carbon" value={soc} min={0.1} max={5} step={0.05} unit="%" onChange={setSoc} />
          <VariableSlider label="Soil pH" value={ph} min={4} max={10} step={0.1} unit="pH" onChange={setPh} />
          <VariableSlider label="Soil moisture" value={moisture} min={5} max={60} step={1} unit="%" onChange={setMoisture} />
        </section>

        <section className="parameter-section">
          <div className="section-icon"><CloudRain size={17} /></div>
          <div className="parameter-section-title"><h4>Climate & water</h4><span>rainfall · temperature</span></div>
          <Field label="Rainfall pattern"><select value={rainfallCategory} onChange={(e) => setRainfallCategory(e.target.value)}><option value="very_low">Very low</option><option value="low">Low / semi-arid</option><option value="moderate">Moderate</option><option value="high">High</option></select></Field>
          <VariableSlider label="Annual rainfall" value={rainfallMm} min={100} max={2000} step={25} unit="mm" onChange={setRainfallMm} />
          <VariableSlider label="Mean temperature" value={temperature} min={5} max={45} step={0.5} unit="°C" onChange={setTemperature} />
        </section>

        <section className="parameter-section">
          <div className="section-icon"><Sprout size={17} /></div>
          <div className="parameter-section-title"><h4>Land use</h4><span>cropping · habitat structure</span></div>
          <Field label="Crop"><input value={cropType} onChange={(e) => setCropType(e.target.value)} /></Field>
          <Field label="Management"><select value={management} onChange={(e) => setManagement(e.target.value)}><option value="monoculture">Monoculture</option><option value="intercropping">Intercropping</option><option value="agroforestry">Agroforestry</option><option value="mixed cropping">Mixed cropping</option></select></Field>
          <Field label="Habitat fragmentation"><select value={fragmentation} onChange={(e) => setFragmentation(e.target.value)}><option value="low">Low</option><option value="medium">Medium</option><option value="high">High</option></select></Field>
        </section>

        <section className="parameter-section">
          <div className="section-icon"><Compass size={17} /></div>
          <div className="parameter-section-title"><h4>Spatial context</h4><span>location signal</span></div>
          <Field label="Region"><input value={region} onChange={(e) => setRegion(e.target.value)} /></Field>
          <div className="two-col">
            <Field label="Latitude"><input type="number" step="0.0001" value={latitude} onChange={(e) => setLatitude(Number(e.target.value))} /></Field>
            <Field label="Longitude"><input type="number" step="0.0001" value={longitude} onChange={(e) => setLongitude(Number(e.target.value))} /></Field>
          </div>
          <div className="map-signal"><MapPin size={13} /> Spatial context included in diagnosis</div>
        </section>
      </div>
      <button className="primary-button full-button" disabled={loading}>{loading ? 'Synthesizing ecosystem…' : 'Run scientific diagnosis'} <ArrowMini /></button>
    </form>
  );
}
function Field({ label, children }) { return <label className="field"><span>{label}</span>{children}</label>; }
function ArrowMini() { return <span aria-hidden="true">→</span>; }
