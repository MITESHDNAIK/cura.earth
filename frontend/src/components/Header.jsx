import React from 'react';
import { Leaf, Activity, Sparkles, BookOpen, SlidersHorizontal, Circle } from 'lucide-react';

export default function Header({ activeTab, setActiveTab }) {
  const tabs = [
    { id: 'chat', label: 'Scientist', icon: Sparkles },
    { id: 'structured', label: 'Diagnosis', icon: SlidersHorizontal },
    { id: 'simulator', label: 'What-If', icon: Activity },
    { id: 'knowledge', label: 'Evidence', icon: BookOpen },
  ];

  return (
    <header className="topbar">
      <button className="brand" onClick={() => setActiveTab('chat')} type="button">
        <span className="brand-mark"><Leaf size={21} /></span>
        <span>
          <strong>Cura<span>.Earth</span></strong>
          <small>AI Environmental Scientist</small>
        </span>
      </button>

      <div className="system-live"><Circle size={7} fill="currentColor" /> ECOLOGY ENGINE ONLINE</div>

      <nav className="topnav">
        {tabs.map(({ id, label, icon: Icon }) => (
          <button key={id} className={`nav-tab ${activeTab === id ? 'active' : ''}`} onClick={() => setActiveTab(id)} type="button">
            <Icon size={16} /><span>{label}</span>
          </button>
        ))}
      </nav>
    </header>
  );
}
