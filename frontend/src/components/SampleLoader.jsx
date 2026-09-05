import React from 'react';

export default function SampleLoader({ onSelectSample, loading }) {
  const samples = [
    {
      id: 'sample_wage',
      label: '📷 Photographed Wage Register',
      desc: 'Blurred register photo with handwritten values & glare',
      filename: 'wage_register_blurred.jpg',
      badge: 'Blurred / Low Quality'
    },
    {
      id: 'sample_safety',
      label: '📄 Safety Inspection Report',
      desc: 'Clean digital PDF with safety committee & health records',
      filename: 'safety_inspection_clean.pdf',
      badge: 'Clean PDF / High Score'
    },
    {
      id: 'sample_license',
      label: '📑 Factory License (Scanned)',
      desc: 'Scanned registration PDF with contract labour & ISMW counts',
      filename: 'factory_license_scanned.pdf',
      badge: 'Scanned / Medium Quality'
    }
  ];

  return (
    <div className="glass-panel" style={{ padding: '1rem 1.25rem', marginBottom: '1.5rem' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.75rem' }}>
        <div style={{ fontSize: '0.85rem', fontWeight: '600', color: 'var(--text-secondary)', display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
          <span>💡</span> HACKATHON LIVE DEMO PRESETS (1-CLICK LOAD)
        </div>
        <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Loads test fixtures automatically</span>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '0.75rem' }}>
        {samples.map((s) => (
          <button
            key={s.id}
            type="button"
            className="btn-sample"
            disabled={loading}
            onClick={() => onSelectSample(s)}
            style={{
              textAlign: 'left',
              display: 'flex',
              flexDirection: 'column',
              gap: '0.2rem',
              padding: '0.65rem 0.85rem'
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <span style={{ fontWeight: '700', fontSize: '0.85rem', color: '#fef08a' }}>{s.label}</span>
              <span style={{ fontSize: '0.65rem', background: 'rgba(255,255,255,0.1)', padding: '0.1rem 0.4rem', borderRadius: '4px' }}>
                {s.badge}
              </span>
            </div>
            <span style={{ fontSize: '0.75rem', color: '#cbd5e1' }}>{s.desc}</span>
          </button>
        ))}
      </div>
    </div>
  );
}
