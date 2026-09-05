import React, { useRef } from 'react';

export default function DocumentUploader({ selectedFile, setSelectedFile, onAnalyze, loading, loadingPhase }) {
  const fileInputRef = useRef(null);

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setSelectedFile(e.target.files[0]);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setSelectedFile(e.dataTransfer.files[0]);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  const getLoadingText = () => {
    if (loadingPhase === 'analyzing') return 'Analyzing Compliance...';
    if (loadingPhase === 'loading_sample') return 'Loading Sample...';
    return 'Extracting Vision Data...';
  };

  return (
    <div className="glass-panel" style={{ padding: '1.25rem' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1rem' }}>
        <h3 style={{ fontSize: '1rem', color: '#f8fafc', fontWeight: '600', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <span style={{ color: 'var(--accent-blue)' }}>📄</span> 2. Document Ingestion
        </h3>
        <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Supports clean PDF, scanned PDF, JPG/PNG</span>
      </div>

      <div 
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onClick={() => fileInputRef.current?.click()}
        style={{
          border: '2px dashed var(--border-color)',
          borderRadius: '10px',
          padding: '2rem 1.5rem',
          textAlign: 'center',
          cursor: 'pointer',
          background: selectedFile ? 'rgba(59, 130, 246, 0.08)' : 'rgba(10, 15, 29, 0.4)',
          borderColor: selectedFile ? 'var(--accent-blue)' : 'var(--border-color)',
          transition: 'all 0.2s ease'
        }}
      >
        <input 
          type="file" 
          ref={fileInputRef} 
          onChange={handleFileChange} 
          accept=".pdf,.jpg,.jpeg,.png,.webp"
          style={{ display: 'none' }}
        />

        {selectedFile ? (
          <div>
            <div style={{ fontSize: '2rem', marginBottom: '0.4rem' }}>
              {selectedFile.name.endsWith('.pdf') ? '📕' : '🖼️'}
            </div>
            <div style={{ fontWeight: '600', color: '#f8fafc', fontSize: '0.95rem' }}>
              {selectedFile.name}
            </div>
            <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginTop: '0.2rem' }}>
              {(selectedFile.size / 1024).toFixed(1)} KB • Ready for Vision Extraction
            </div>
          </div>
        ) : (
          <div>
            <div style={{ fontSize: '2.2rem', marginBottom: '0.5rem' }}>📥</div>
            <div style={{ fontWeight: '600', color: '#f8fafc', fontSize: '0.95rem' }}>
              Drag & Drop your Labour Compliance Document here
            </div>
            <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginTop: '0.3rem' }}>
              or click to browse from your computer (Wage Register, Inspection Report, License PDF)
            </div>
          </div>
        )}
      </div>

      <div style={{ marginTop: '1.25rem', display: 'flex', justifyContent: 'flex-end', gap: '0.75rem' }}>
        {selectedFile && (
          <button 
            type="button" 
            className="btn-secondary" 
            onClick={(e) => { e.stopPropagation(); setSelectedFile(null); }}
          >
            Clear Selection
          </button>
        )}
        <button 
          type="button" 
          className="btn-primary" 
          disabled={!selectedFile || loading}
          onClick={onAnalyze}
          style={{ minWidth: '180px', justifyContent: 'center' }}
        >
          {loading ? (
            <>
              <span style={{
                display: 'inline-block',
                width: '16px',
                height: '16px',
                border: '2px solid rgba(255,255,255,0.3)',
                borderTopColor: '#ffffff',
                borderRadius: '50%',
                animation: 'spin 0.8s linear infinite'
              }}></span>
              {getLoadingText()}
            </>
          ) : (
            <>⚡ Analyze Document</>
          )}
        </button>
      </div>

      <style>{`
        @keyframes spin {
          to { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  );
}
