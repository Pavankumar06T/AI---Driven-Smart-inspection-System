import React, { useState, useEffect } from 'react';
import { getPageImageUrl } from '../services/api';

export default function DocumentViewer({ documentId, fields, activeFieldId, setActiveFieldId }) {
  const [currentPage, setCurrentPage] = useState(1);
  const [imageLoaded, setImageLoaded] = useState(false);
  const [imageError, setImageError] = useState(false);
  const [hoveredFieldId, setHoveredFieldId] = useState(null);

  // Reset state when documentId or currentPage changes
  useEffect(() => {
    setImageLoaded(false);
    setImageError(false);
  }, [documentId, currentPage]);

  // Determine max page number present in fields
  const maxPages = Math.max(1, ...fields.map(f => f.evidence?.page || 1));

  // Auto switch page when activeFieldId changes
  useEffect(() => {
    if (activeFieldId) {
      const activeField = fields.find(f => f.field_id === activeFieldId);
      if (activeField && activeField.evidence?.page) {
        setCurrentPage(activeField.evidence.page);
      }
    }
  }, [activeFieldId, fields]);

  // Fields on current page
  const pageFields = fields.filter(f => (f.evidence?.page || 1) === currentPage);
  const imageUrl = getPageImageUrl(documentId, currentPage);

  return (
    <div className="glass-panel" style={{ padding: '1.25rem', height: '100%', display: 'flex', flexDirection: 'column' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.85rem' }}>
        <h3 style={{ fontSize: '1rem', color: '#f8fafc', fontWeight: '600', display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
          <span style={{ color: 'var(--accent-gold)' }}>📌</span> Document Evidence Overlay
        </h3>
        
        {/* Page Selector */}
        {maxPages > 1 && (
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
            <button
              type="button"
              className="btn-secondary"
              disabled={currentPage <= 1}
              onClick={() => setCurrentPage(prev => Math.max(1, prev - 1))}
              style={{ padding: '0.2rem 0.6rem', fontSize: '0.75rem' }}
            >
              ◀ Prev
            </button>
            <span style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
              Page {currentPage} of {maxPages}
            </span>
            <button
              type="button"
              className="btn-secondary"
              disabled={currentPage >= maxPages}
              onClick={() => setCurrentPage(prev => Math.min(maxPages, prev + 1))}
              style={{ padding: '0.2rem 0.6rem', fontSize: '0.75rem' }}
            >
              Next ▶
            </button>
          </div>
        )}
      </div>

      {/* Document Viewport Container */}
      <div style={{
        flex: 1,
        position: 'relative',
        background: '#070b14',
        borderRadius: '8px',
        border: '1px solid var(--border-color)',
        overflow: 'auto',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        minHeight: '480px',
        padding: '1rem'
      }}>
        {imageError ? (
          <div style={{ color: 'var(--text-muted)', fontSize: '0.9rem', textAlign: 'center', padding: '2rem' }}>
            <div style={{ fontSize: '1.8rem', marginBottom: '0.5rem' }}>⚠️</div>
            <div style={{ fontWeight: '600', color: '#f87171', marginBottom: '0.3rem' }}>
              Document Page Image Unavailable
            </div>
            <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
              Target image path could not be loaded from backend server.
            </div>
            <button 
              type="button" 
              className="btn-secondary" 
              onClick={() => { setImageError(false); setImageLoaded(false); }}
              style={{ marginTop: '1rem', fontSize: '0.8rem', padding: '0.3rem 0.8rem' }}
            >
              🔄 Retry Loading Image
            </button>
          </div>
        ) : (
          <div style={{ position: 'relative', display: 'inline-block', width: '100%', maxWidth: '800px' }}>
            {/* Rendered Document Page Image */}
            <img 
              key={`${documentId}_page_${currentPage}`}
              src={imageUrl} 
              alt={`Document Page ${currentPage}`}
              onLoad={() => { setImageLoaded(true); setImageError(false); }}
              onError={() => setImageError(true)}
              style={{
                display: 'block',
                width: '100%',
                height: 'auto',
                borderRadius: '6px',
                boxShadow: '0 4px 24px rgba(0,0,0,0.7)'
              }}
            />

            {/* SVG Interactive Bounding Box Evidence Overlay */}
            {(imageLoaded || pageFields.length > 0) && (
              <svg 
                style={{
                  position: 'absolute',
                  top: 0,
                  left: 0,
                  width: '100%',
                  height: '100%',
                  pointerEvents: 'none'
                }}
                viewBox="0 0 100 100"
                preserveAspectRatio="none"
              >
                {pageFields.map((field) => {
                  const [x, y, w, h] = field.evidence?.bbox || [0, 0, 0, 0];
                  const isActive = activeFieldId === field.field_id;
                  const isHovered = hoveredFieldId === field.field_id;

                  const strokeColor = isActive ? '#f59e0b' : (isHovered ? '#38bdf8' : '#3b82f6');
                  const fillColor = isActive ? 'rgba(245, 158, 11, 0.25)' : (isHovered ? 'rgba(56, 189, 248, 0.2)' : 'rgba(59, 130, 246, 0.12)');
                  const strokeWidth = isActive ? '2.5' : (isHovered ? '2' : '1.2');

                  return (
                    <g 
                      key={field.field_id} 
                      style={{ pointerEvents: 'all', cursor: 'pointer' }}
                      onClick={() => setActiveFieldId(field.field_id)}
                      onMouseEnter={() => setHoveredFieldId(field.field_id)}
                      onMouseLeave={() => setHoveredFieldId(null)}
                    >
                      {/* Crisp Bounding Box Rect */}
                      <rect 
                        x={`${x}%`}
                        y={`${y}%`}
                        width={`${w}%`}
                        height={`${h}%`}
                        fill={fillColor}
                        stroke={strokeColor}
                        strokeWidth={strokeWidth}
                        vectorEffect="non-scaling-stroke"
                        style={{
                          transition: 'all 0.15s ease',
                          filter: isActive ? 'drop-shadow(0 0 6px #f59e0b)' : undefined
                        }}
                      >
                        <title>{`${field.field_id}: ${field.name} = "${field.value}"`}</title>
                      </rect>

                      {/* SVG Native Text Badge Pill (Scaled Perfectly) */}
                      {(isActive || isHovered) ? (
                        <g>
                          <rect 
                            x={`${Math.max(0, Math.min(x, 70))}%`}
                            y={`${Math.max(0, y - 3.2)}%`}
                            width={`${Math.min(30, Math.max(12, field.name.length * 1.4 + 4))}%`}
                            height="3%"
                            rx="0.4"
                            ry="0.4"
                            fill={isActive ? '#d97706' : '#0284c7'}
                            stroke="#ffffff"
                            strokeWidth="0.5"
                            vectorEffect="non-scaling-stroke"
                          />
                          <text 
                            x={`${Math.max(0.5, Math.min(x + 0.6, 70.6))}%`}
                            y={`${Math.max(2, y - 1.0)}%`}
                            fill="#ffffff"
                            fontSize="2.1px"
                            fontWeight="bold"
                            fontFamily="sans-serif"
                          >
                            {field.field_id}: {field.name}
                          </text>
                        </g>
                      ) : (
                        <g>
                          <rect 
                            x={`${x}%`}
                            y={`${y}%`}
                            width="3.5%"
                            height="2.2%"
                            rx="0.3"
                            ry="0.3"
                            fill="rgba(15, 23, 42, 0.85)"
                            stroke="#3b82f6"
                            strokeWidth="0.5"
                            vectorEffect="non-scaling-stroke"
                          />
                          <text 
                            x={`${x + 0.4}%`}
                            y={`${y + 1.6}%`}
                            fill="#93c5fd"
                            fontSize="1.6px"
                            fontWeight="bold"
                            fontFamily="monospace"
                          >
                            {field.field_id}
                          </text>
                        </g>
                      )}
                    </g>
                  );
                })}
              </svg>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
