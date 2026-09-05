import React, { useState } from 'react';

export default function FieldExtractorPanel({ fields, activeFieldId, setActiveFieldId, extractionOutput }) {
  const [searchTerm, setSearchTerm] = useState('');
  const [copied, setCopied] = useState(false);

  const filteredFields = fields.filter(f => 
    f.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    f.value.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleCopyJSON = () => {
    if (!extractionOutput) return;
    navigator.clipboard.writeText(JSON.stringify(extractionOutput, null, 2));
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="glass-panel" style={{ padding: '1.25rem', height: '100%', display: 'flex', flexDirection: 'column' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.85rem' }}>
        <div>
          <h3 style={{ fontSize: '1rem', color: '#f8fafc', fontWeight: '600', display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
            <span style={{ color: 'var(--accent-teal)' }}>🔍</span> Extracted Compliance Fields ({fields.length})
          </h3>
          <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
            Click any field to highlight grounded evidence on document
          </span>
        </div>
        <button 
          type="button" 
          className="btn-secondary" 
          onClick={handleCopyJSON}
          style={{ fontSize: '0.75rem', padding: '0.35rem 0.7rem' }}
          title="Copy ExtractionOutput JSON contract for reasoning module"
        >
          {copied ? '✓ Copied JSON' : '📋 Copy JSON Contract'}
        </button>
      </div>

      {/* Search Input */}
      <div style={{ marginBottom: '0.85rem' }}>
        <input 
          type="text" 
          className="form-input" 
          placeholder="Filter fields by name or value..." 
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          style={{ width: '100%', fontSize: '0.85rem', padding: '0.45rem 0.75rem' }}
        />
      </div>

      {/* Fields List */}
      <div style={{ flex: 1, overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '0.65rem', paddingRight: '0.2rem' }}>
        {filteredFields.length === 0 ? (
          <div style={{ textAlign: 'center', color: 'var(--text-muted)', padding: '2rem 1rem', fontSize: '0.85rem' }}>
            No compliance fields match search query.
          </div>
        ) : (
          filteredFields.map((field) => {
            const isActive = activeFieldId === field.field_id;
            const confClass = `badge-confidence-${field.extraction_confidence.toLowerCase()}`;

            return (
              <div 
                key={field.field_id}
                onClick={() => setActiveFieldId(field.field_id)}
                className="glass-card"
                style={{
                  padding: '0.85rem 1rem',
                  cursor: 'pointer',
                  borderColor: isActive ? 'var(--accent-gold)' : 'var(--border-color)',
                  background: isActive ? 'rgba(245, 158, 11, 0.12)' : undefined,
                  boxShadow: isActive ? '0 0 12px rgba(245, 158, 11, 0.25)' : undefined
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.3rem' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                    <span style={{
                      fontSize: '0.7rem',
                      fontFamily: 'monospace',
                      background: 'rgba(255,255,255,0.1)',
                      color: 'var(--text-secondary)',
                      padding: '0.1rem 0.35rem',
                      borderRadius: '4px'
                    }}>
                      {field.field_id}
                    </span>
                    <span style={{ fontWeight: '700', fontSize: '0.85rem', color: '#f8fafc' }}>
                      {field.name}
                    </span>
                  </div>
                  <span className={confClass}>
                    {field.extraction_confidence}
                  </span>
                </div>

                <div style={{
                  fontSize: '0.95rem',
                  fontWeight: '600',
                  color: isActive ? '#fef08a' : '#38bdf8',
                  wordBreak: 'break-word',
                  marginBottom: '0.35rem'
                }}>
                  {field.value}
                </div>

                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <span>📍 Page {field.evidence.page}</span>
                  <span>•</span>
                  <span style={{ fontStyle: 'italic', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap', maxWidth: '220px' }}>
                    "{field.evidence.text_snippet}"
                  </span>
                </div>
              </div>
            );
          })
        )}
      </div>
    </div>
  );
}
