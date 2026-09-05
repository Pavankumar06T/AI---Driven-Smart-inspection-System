import React from 'react';

export default function QualityCard({ documentQuality }) {
  if (!documentQuality) return null;

  const score = documentQuality.overall_score || 0;
  const scorePercent = Math.round(score * 100);
  const issues = documentQuality.issues || [];

  let statusColor = '#10b981'; // Green
  let statusLabel = 'High Legibility';
  if (score < 0.65) {
    statusColor = '#ef4444'; // Red
    statusLabel = 'Poor / Blurred Quality';
  } else if (score < 0.85) {
    statusColor = '#f59e0b'; // Amber
    statusLabel = 'Acceptable Quality';
  }

  return (
    <div className="glass-card" style={{ padding: '1rem 1.25rem', marginBottom: '1rem' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <div>
          <div style={{ fontSize: '0.75rem', fontWeight: '600', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
            DOCUMENT LEGIBILITY QUALITY SCORE
          </div>
          <div style={{ display: 'flex', alignItems: 'baseline', gap: '0.6rem', marginTop: '0.2rem' }}>
            <span style={{ fontSize: '1.8rem', fontWeight: '800', color: statusColor, fontFamily: 'var(--font-heading)' }}>
              {scorePercent}%
            </span>
            <span style={{
              background: `${statusColor}20`,
              color: statusColor,
              border: `1px solid ${statusColor}40`,
              padding: '0.15rem 0.5rem',
              borderRadius: '9999px',
              fontSize: '0.7rem',
              fontWeight: '700'
            }}>
              {statusLabel}
            </span>
          </div>
        </div>

        {/* Circular Progress Indicator */}
        <div style={{ width: '50px', height: '50px', position: 'relative' }}>
          <svg width="50" height="50" viewBox="0 0 36 36">
            <path
              d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
              fill="none"
              stroke="rgba(255,255,255,0.1)"
              strokeWidth="3.5"
            />
            <path
              d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
              fill="none"
              stroke={statusColor}
              strokeWidth="3.5"
              strokeDasharray={`${scorePercent}, 100`}
              strokeLinecap="round"
            />
          </svg>
        </div>
      </div>

      {issues.length > 0 ? (
        <div style={{ marginTop: '0.85rem', paddingTop: '0.75rem', borderTop: '1px solid var(--border-color)' }}>
          <div style={{ fontSize: '0.75rem', fontWeight: '600', color: '#f87171', marginBottom: '0.3rem', display: 'flex', alignItems: 'center', gap: '0.3rem' }}>
            <span>⚠️</span> DETECTED QUALITY ISSUES ({issues.length})
          </div>
          <ul style={{ paddingLeft: '1.2rem', margin: 0 }}>
            {issues.map((issue, idx) => (
              <li key={idx} style={{ fontSize: '0.8rem', color: '#fca5a5', marginBottom: '0.15rem' }}>
                {issue}
              </li>
            ))}
          </ul>
        </div>
      ) : (
        <div style={{ marginTop: '0.75rem', paddingTop: '0.6rem', borderTop: '1px solid var(--border-color)', fontSize: '0.75rem', color: '#64748b' }}>
          ✓ No significant visual defects or occlusion detected.
        </div>
      )}
    </div>
  );
}
