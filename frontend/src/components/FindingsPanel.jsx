import React, { useState } from 'react';

export default function FindingsPanel({ findingsOutput, activeFieldId, setActiveFieldId, analysisError }) {
  const [viewMode, setViewMode] = useState('employer'); // 'employer' | 'inspector'

  if (analysisError) {
    return (
      <div className="glass-panel" style={{ padding: '1.25rem', marginTop: '1.5rem', borderLeft: '4px solid #f59e0b' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', color: '#fbbf24' }}>
          <span style={{ fontSize: '1.4rem' }}>⚠️</span>
          <div>
            <h3 style={{ fontSize: '1.1rem', fontWeight: 600 }}>Compliance Analysis Unavailable</h3>
            <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginTop: '0.25rem' }}>
              {analysisError} — Showing document extraction & evidence grounding below.
            </p>
          </div>
        </div>
      </div>
    );
  }

  if (!findingsOutput) return null;

  const { risk_score, risk_tier, findings = [] } = findingsOutput;

  // Tier Color Mapping
  const getTierStyle = (tier) => {
    switch (tier?.toLowerCase()) {
      case 'low':
        return { bg: 'rgba(34, 197, 94, 0.15)', border: 'rgba(34, 197, 94, 0.4)', color: '#4ade80', label: 'LOW RISK' };
      case 'medium':
        return { bg: 'rgba(234, 179, 8, 0.15)', border: 'rgba(234, 179, 8, 0.4)', color: '#facc15', label: 'MEDIUM RISK' };
      case 'high':
        return { bg: 'rgba(239, 68, 68, 0.15)', border: 'rgba(239, 68, 68, 0.4)', color: '#f87171', label: 'HIGH RISK' };
      default:
        return { bg: 'rgba(148, 163, 184, 0.15)', border: 'rgba(148, 163, 184, 0.4)', color: '#94a3b8', label: 'UNKNOWN' };
    }
  };

  const tierInfo = getTierStyle(risk_tier);

  // Finding Type Badge Mapping
  const getTypeBadge = (type) => {
    switch (type) {
      case 'missing':
        return { bg: 'rgba(245, 158, 11, 0.15)', border: 'rgba(245, 158, 11, 0.3)', color: '#fbbf24', text: 'MISSING DATA' };
      case 'discrepancy':
        return { bg: 'rgba(239, 68, 68, 0.15)', border: 'rgba(239, 68, 68, 0.3)', color: '#f87171', text: 'DISCREPANCY' };
      case 'substantive':
        return { bg: 'rgba(168, 85, 247, 0.15)', border: 'rgba(168, 85, 247, 0.3)', color: '#c084fc', text: 'VIOLATION' };
      case 'cannot_determine':
        return { bg: 'rgba(148, 163, 184, 0.15)', border: 'rgba(148, 163, 184, 0.3)', color: '#94a3b8', text: 'CANNOT DETERMINE' };
      default:
        return { bg: 'rgba(255, 255, 255, 0.1)', border: 'rgba(255, 255, 255, 0.2)', color: 'var(--text-main)', text: type?.toUpperCase() };
    }
  };

  // Deduplicate findings by finding_id to prevent any duplicate card rendering
  const uniqueFindings = [];
  const seenFindingIds = new Set();
  (findings || []).forEach((f) => {
    const key = f.finding_id || `${f.type}-${f.explanation}`;
    if (!seenFindingIds.has(key)) {
      seenFindingIds.add(key);
      uniqueFindings.push(f);
    }
  });

  return (
    <div className="glass-panel" style={{ padding: '1.25rem', marginTop: '1.5rem' }}>
      {/* Header & Risk Scorecard Banner */}
      <div style={{
        display: 'flex',
        flexWrap: 'wrap',
        alignItems: 'center',
        justifyContent: 'space-between',
        gap: '1rem',
        paddingBottom: '1rem',
        borderBottom: '1px solid var(--border-color)',
        marginBottom: '1.25rem'
      }}>
        <div>
          <h2 style={{ fontSize: '1.2rem', color: 'var(--text-main)', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <span>📊</span> Compliance Reasoning Findings
          </h2>
          <p style={{ fontSize: '0.825rem', color: 'var(--text-secondary)', marginTop: '0.2rem' }}>
            Automated statutory check results from Ministry Labour Code Rules Engine
          </p>
        </div>

        {/* Risk Score Gauge & Badge */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <div style={{
            background: tierInfo.bg,
            border: `1px solid ${tierInfo.border}`,
            color: tierInfo.color,
            padding: '0.5rem 1rem',
            borderRadius: '8px',
            fontWeight: 700,
            fontSize: '0.9rem',
            display: 'flex',
            alignItems: 'center',
            gap: '0.5rem',
            boxShadow: '0 2px 8px rgba(0,0,0,0.2)'
          }}>
            <span style={{ width: '8px', height: '8px', borderRadius: '50%', background: tierInfo.color }}></span>
            {tierInfo.label}
          </div>

          <div style={{
            background: 'rgba(10, 15, 29, 0.7)',
            border: '1px solid var(--border-color)',
            padding: '0.5rem 1rem',
            borderRadius: '8px',
            textAlign: 'right'
          }}>
            <div style={{ fontSize: '0.725rem', color: 'var(--text-muted)', uppercase: 'true', fontWeight: 600 }}>RISK SCORE</div>
            <div style={{ fontSize: '1.1rem', fontWeight: 700, color: 'var(--accent-gold)' }}>{risk_score.toFixed(1)}</div>
          </div>
        </div>
      </div>

      {/* Mode Toggle Controls */}
      <div style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        flexWrap: 'wrap',
        gap: '0.75rem',
        marginBottom: '1.25rem'
      }}>
        <div style={{ fontSize: '0.875rem', fontWeight: 600, color: 'var(--text-secondary)' }}>
          {uniqueFindings.length} Finding{uniqueFindings.length !== 1 ? 's' : ''} Identified
        </div>

        {/* Employer / Inspector View Toggle */}
        <div style={{
          display: 'inline-flex',
          background: 'rgba(10, 15, 29, 0.8)',
          padding: '3px',
          borderRadius: '8px',
          border: '1px solid var(--border-color)'
        }}>
          <button
            type="button"
            onClick={() => setViewMode('employer')}
            style={{
              padding: '0.45rem 1rem',
              borderRadius: '6px',
              fontSize: '0.825rem',
              fontWeight: 600,
              border: 'none',
              cursor: 'pointer',
              transition: 'all 0.2s ease',
              background: viewMode === 'employer' ? 'linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%)' : 'transparent',
              color: viewMode === 'employer' ? '#ffffff' : 'var(--text-secondary)',
              boxShadow: viewMode === 'employer' ? '0 2px 8px rgba(37, 99, 235, 0.3)' : 'none'
            }}
          >
            🛠️ Employer View
          </button>
          <button
            type="button"
            onClick={() => setViewMode('inspector')}
            style={{
              padding: '0.45rem 1rem',
              borderRadius: '6px',
              fontSize: '0.825rem',
              fontWeight: 600,
              border: 'none',
              cursor: 'pointer',
              transition: 'all 0.2s ease',
              background: viewMode === 'inspector' ? 'linear-gradient(135deg, #8b5cf6 0%, #6d28d9 100%)' : 'transparent',
              color: viewMode === 'inspector' ? '#ffffff' : 'var(--text-secondary)',
              boxShadow: viewMode === 'inspector' ? '0 2px 8px rgba(139, 92, 246, 0.3)' : 'none'
            }}
          >
            🔍 Inspector View
          </button>
        </div>
      </div>

      {/* Findings List */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem' }}>
        {uniqueFindings.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '2rem', color: 'var(--text-muted)', fontSize: '0.9rem' }}>
            ✅ No compliance violations or discrepancies detected for this document profile.
          </div>
        ) : (
          uniqueFindings.map((finding, idx) => {
            const isCannotDetermine = finding.type === 'cannot_determine';
            const isActive = activeFieldId && finding.related_field_id === activeFieldId;
            const typeBadge = getTypeBadge(finding.type);

            return (
              <div
                key={finding.finding_id || `finding-${idx}`}
                onClick={() => {
                  if (finding.related_field_id) {
                    setActiveFieldId(finding.related_field_id);
                  }
                }}
                className="glass-card"
                style={{
                  padding: '1rem 1.15rem',
                  opacity: isCannotDetermine ? 0.9 : 1,
                  border: isActive
                    ? '1.5px solid #fbbf24'
                    : isCannotDetermine
                    ? '1px solid rgba(148, 163, 184, 0.25)'
                    : '1px solid var(--border-color)',
                  boxShadow: isActive ? '0 0 16px rgba(251, 191, 36, 0.25)' : 'none',
                  background: isCannotDetermine
                    ? 'rgba(15, 23, 42, 0.5)'
                    : isActive
                    ? 'rgba(251, 191, 36, 0.08)'
                    : 'rgba(18, 25, 41, 0.65)',
                  cursor: finding.related_field_id ? 'pointer' : 'default',
                  transition: 'all 0.2s ease'
                }}
              >
                {/* Badge Header Row */}
                <div style={{ display: 'flex', flexWrap: 'wrap', alignItems: 'center', gap: '0.5rem', marginBottom: '0.6rem' }}>
                  <span style={{
                    background: typeBadge.bg,
                    border: `1px solid ${typeBadge.border}`,
                    color: typeBadge.color,
                    padding: '0.15rem 0.55rem',
                    borderRadius: '4px',
                    fontSize: '0.725rem',
                    fontWeight: 700,
                    letterSpacing: '0.04em'
                  }}>
                    {typeBadge.text}
                  </span>

                  {finding.severity !== null && finding.severity !== undefined && (
                    <span style={{
                      background: 'rgba(239, 68, 68, 0.1)',
                      border: '1px solid rgba(239, 68, 68, 0.25)',
                      color: '#fca5a5',
                      padding: '0.15rem 0.55rem',
                      borderRadius: '4px',
                      fontSize: '0.725rem',
                      fontWeight: 600
                    }}>
                      Severity L{finding.severity}
                    </span>
                  )}

                  {finding.confidence && (
                    <span className={`badge-confidence-${finding.confidence}`}>
                      {finding.confidence} confidence
                    </span>
                  )}

                  {finding.citation && (
                    <span style={{
                      marginLeft: 'auto',
                      fontSize: '0.75rem',
                      color: 'var(--accent-gold)',
                      background: 'rgba(251, 191, 36, 0.1)',
                      padding: '0.15rem 0.5rem',
                      borderRadius: '4px',
                      fontFamily: 'monospace'
                    }}>
                      📜 {finding.citation.code} §{finding.citation.section}
                    </span>
                  )}
                </div>

                {/* Explanation */}
                <p style={{
                  fontSize: '0.875rem',
                  color: isCannotDetermine ? 'var(--text-secondary)' : 'var(--text-main)',
                  lineHeight: '1.45',
                  marginBottom: '0.6rem'
                }}>
                  {finding.explanation}
                </p>

                {/* Cannot Determine Warning Callout OR Action Box */}
                {isCannotDetermine ? (
                  <div style={{
                    background: 'rgba(148, 163, 184, 0.1)',
                    borderLeft: '3px solid #94a3b8',
                    padding: '0.6rem 0.85rem',
                    borderRadius: '4px',
                    fontSize: '0.8rem',
                    marginTop: '0.5rem'
                  }}>
                    {finding.reason && (
                      <div style={{ color: '#cbd5e1', marginBottom: '0.35rem', wordBreak: 'break-word' }}>
                        <strong>Reason:</strong> {finding.reason}
                      </div>
                    )}
                    {finding.missing_context && finding.missing_context.length > 0 && (
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', flexWrap: 'wrap', marginTop: '0.35rem' }}>
                        <span style={{ color: 'var(--text-muted)', fontSize: '0.75rem', fontWeight: 600 }}>Missing Context:</span>
                        {finding.missing_context.map((ctx, i) => (
                          <span key={`${finding.finding_id || idx}-ctx-${i}`} style={{
                            background: 'rgba(255,255,255,0.08)',
                            border: '1px solid rgba(255,255,255,0.12)',
                            color: '#cbd5e1',
                            padding: '0.15rem 0.5rem',
                            borderRadius: '4px',
                            fontSize: '0.75rem',
                            whiteSpace: 'normal',
                            wordBreak: 'break-word'
                          }}>
                            {ctx}
                          </span>
                        ))}
                      </div>
                    )}
                  </div>
                ) : (
                  <div style={{
                    background: viewMode === 'employer' ? 'rgba(37, 99, 235, 0.08)' : 'rgba(139, 92, 246, 0.08)',
                    borderLeft: viewMode === 'employer' ? '3px solid #3b82f6' : '3px solid #8b5cf6',
                    padding: '0.55rem 0.85rem',
                    borderRadius: '4px',
                    fontSize: '0.825rem',
                    marginTop: '0.5rem',
                    color: 'var(--text-main)'
                  }}>
                    <strong style={{ color: viewMode === 'employer' ? '#60a5fa' : '#c084fc' }}>
                      {viewMode === 'employer' ? '🛠️ Employer Action:' : '🔍 Inspector Action:'}
                    </strong>{' '}
                    {viewMode === 'employer'
                      ? (finding.employer_action || 'No action required.')
                      : (finding.inspector_action || 'Verify compliance during on-site inspection.')}
                  </div>
                )}

                {/* Evidence Grounding Link */}
                {finding.related_field_id && (
                  <div style={{
                    marginTop: '0.6rem',
                    fontSize: '0.75rem',
                    color: isActive ? '#fbbf24' : 'var(--accent-blue)',
                    fontWeight: 600,
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.3rem'
                  }}>
                    <span>📍</span>
                    <span>Evidence Grounding: Field [{finding.related_field_id}] (Click card to highlight on document)</span>
                  </div>
                )}
              </div>
            );
          })
        )}
      </div>
    </div>
  );
}
