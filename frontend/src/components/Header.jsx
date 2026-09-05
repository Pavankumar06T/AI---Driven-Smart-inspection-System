import React from 'react';

export default function Header() {
  return (
    <header style={{
      background: 'linear-gradient(90deg, #0b192c 0%, #1e293b 100%)',
      borderBottom: '1px solid var(--border-color)',
      padding: '0.9rem 2rem',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      zIndex: 1000,
      height: '64px',
      boxShadow: '0 4px 20px rgba(0, 0, 0, 0.4)'
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
        <div style={{
          width: '42px',
          height: '42px',
          borderRadius: '10px',
          background: 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontWeight: '800',
          fontSize: '1.2rem',
          color: '#ffffff',
          boxShadow: '0 4px 10px rgba(245, 158, 11, 0.3)'
        }}>
          SS
        </div>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
            <h1 style={{ fontSize: '1.25rem', fontWeight: '700', color: '#ffffff' }}>
              Shram Sankalp 2026
            </h1>
            <span style={{
              background: 'rgba(59, 130, 246, 0.15)',
              color: '#60a5fa',
              border: '1px solid rgba(59, 130, 246, 0.3)',
              padding: '0.15rem 0.5rem',
              borderRadius: '4px',
              fontSize: '0.7rem',
              fontWeight: '600'
            }}>
              PS-05 PROTOTYPE
            </span>
          </div>
          <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
            Document Intelligence & Vision Evidence Grounding Module • Ministry of Labour & Employment
          </p>
        </div>
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: '1.5rem' }}>
        <div style={{ textAlign: 'right' }}>
          <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>PIPELINE STATUS</div>
          <div style={{ fontSize: '0.85rem', color: '#34d399', fontWeight: '600', display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
            <span style={{ width: '8px', height: '8px', borderRadius: '50%', background: '#34d399', display: 'inline-block' }}></span>
            Gemini Vision Grounding Engine Active
          </div>
        </div>
      </div>
    </header>
  );
}
