import React from 'react';

export default function ProfileForm({ profile, setProfile }) {
  const handleChange = (field, value) => {
    setProfile(prev => ({ ...prev, [field]: value }));
  };

  return (
    <div className="glass-panel" style={{ padding: '1.25rem' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1rem' }}>
        <h3 style={{ fontSize: '1rem', color: '#f8fafc', fontWeight: '600', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <span style={{ color: 'var(--accent-gold)' }}>📋</span> 1. Establishment Profile
        </h3>
        <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Required for compliance Context</span>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '1rem' }}>
        <div className="form-group">
          <label className="form-label">State / UT</label>
          <select 
            className="form-select"
            value={profile.state || 'Maharashtra'}
            onChange={(e) => handleChange('state', e.target.value)}
          >
            <option value="Maharashtra">Maharashtra</option>
            <option value="Karnataka">Karnataka</option>
            <option value="Gujarat">Gujarat</option>
            <option value="Delhi">Delhi</option>
            <option value="Tamil Nadu">Tamil Nadu</option>
            <option value="Uttar Pradesh">Uttar Pradesh</option>
            <option value="West Bengal">West Bengal</option>
          </select>
        </div>

        <div className="form-group">
          <label className="form-label">Sector</label>
          <select 
            className="form-select"
            value={profile.sector || 'Factory'}
            onChange={(e) => handleChange('sector', e.target.value)}
          >
            <option value="Factory">Factory & Manufacturing</option>
            <option value="Construction">Building & Construction</option>
            <option value="Shops & Establishments">Shops & Establishments</option>
            <option value="Chemical Operations">Chemical Operations (Hazardous)</option>
            <option value="Mining">Mining & Quarrying</option>
          </select>
        </div>

        <div className="form-group">
          <label className="form-label">Declared Headcount</label>
          <input 
            type="number"
            className="form-input"
            placeholder="e.g. 150"
            value={profile.headcount || ''}
            onChange={(e) => handleChange('headcount', e.target.value ? parseInt(e.target.value, 10) : null)}
          />
        </div>

        <div className="form-group">
          <label className="form-label">Contract Labour Involved?</label>
          <select 
            className="form-select"
            value={profile.contractor_involved === null ? 'unknown' : (profile.contractor_involved ? 'yes' : 'no')}
            onChange={(e) => {
              const val = e.target.value === 'yes' ? true : (e.target.value === 'no' ? false : null);
              handleChange('contractor_involved', val);
            }}
          >
            <option value="unknown">Unspecified / Unknown</option>
            <option value="yes">Yes (Contract Labour Deployed)</option>
            <option value="no">No (Direct Employment Only)</option>
          </select>
        </div>

        <div className="form-group">
          <label className="form-label">Worker Type</label>
          <select 
            className="form-select"
            value={profile.worker_type || 'Skilled'}
            onChange={(e) => handleChange('worker_type', e.target.value)}
          >
            <option value="Skilled">Skilled Workers</option>
            <option value="Unskilled">Unskilled Workers</option>
            <option value="Semi-Skilled">Semi-Skilled Workers</option>
            <option value="Hazardous">Hazardous Process Category</option>
            <option value="Inter-State Migrant">Inter-State Migrant Workers (ISMW)</option>
          </select>
        </div>
      </div>
    </div>
  );
}
