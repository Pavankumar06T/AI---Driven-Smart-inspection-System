import React, { useState } from 'react';
import Header from './components/Header';
import ProfileForm from './components/ProfileForm';
import DocumentUploader from './components/DocumentUploader';
import SampleLoader from './components/SampleLoader';
import DocumentViewer from './components/DocumentViewer';
import FieldExtractorPanel from './components/FieldExtractorPanel';
import QualityCard from './components/QualityCard';
import FindingsPanel from './components/FindingsPanel';
import { extractDocument, analyzeDocument, fetchFixtureBlob } from './services/api';

export default function App() {
  const [profile, setProfile] = useState({
    state: 'Maharashtra',
    sector: 'Factory',
    headcount: 150,
    contractor_involved: true,
    worker_type: 'Skilled'
  });

  const [selectedFile, setSelectedFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [loadingPhase, setLoadingPhase] = useState(''); // 'loading_sample' | 'extracting' | 'analyzing' | ''
  const [error, setError] = useState(null);
  const [extractionResult, setExtractionResult] = useState(null);
  const [findingsResult, setFindingsResult] = useState(null);
  const [analysisError, setAnalysisError] = useState(null);
  const [activeFieldId, setActiveFieldId] = useState(null);

  const executePipeline = async (file, profileData) => {
    setLoading(true);
    setLoadingPhase('extracting');
    setError(null);
    setAnalysisError(null);
    setExtractionResult(null);
    setFindingsResult(null);
    setActiveFieldId(null);

    // 1. POST to /extract (port 8000)
    let extractionRes;
    try {
      extractionRes = await extractDocument(file, profileData);
      setExtractionResult(extractionRes);
      if (extractionRes.fields && extractionRes.fields.length > 0) {
        setActiveFieldId(extractionRes.fields[0].field_id);
      }
    } catch (err) {
      console.error('[Extraction Error]', err);
      const msg = typeof err === 'string' ? err : (err.message || String(err));
      setError(msg || 'Extraction failed. Please check backend server connection on http://localhost:8000');
      setLoading(false);
      setLoadingPhase('');
      return;
    }

    setLoadingPhase('analyzing');

    // 2. POST ExtractionOutput to /analyze (port 8001)
    try {
      const findingsRes = await analyzeDocument(extractionRes);
      setFindingsResult(findingsRes);
    } catch (err) {
      console.error('[Compliance Analysis Error]', err);
      const msg = typeof err === 'string' ? err : (err.message || String(err));
      setAnalysisError(msg || 'Could not connect to Compliance Reasoning service (http://localhost:8001).');
    } finally {
      setLoading(false);
      setLoadingPhase('');
    }
  };

  const handleAnalyze = async () => {
    if (!selectedFile) return;

    // Validate supported file extensions on client-side as well
    const ext = selectedFile.name.split('.').pop()?.toLowerCase();
    const supportedExts = ['pdf', 'jpg', 'jpeg', 'png', 'webp', 'bmp', 'tiff'];
    if (ext && !supportedExts.includes(ext)) {
      setError(`Unsupported file format (.${ext}). Please upload a valid document or image file (PDF, JPG, PNG, WEBP).`);
      return;
    }

    await executePipeline(selectedFile, profile);
  };

  const handleSelectSample = async (sample) => {
    setLoading(true);
    setLoadingPhase('loading_sample');
    setError(null);
    setAnalysisError(null);
    setExtractionResult(null);
    setFindingsResult(null);
    setActiveFieldId(null);

    // Update profile matching sample context
    let targetProfile = { ...profile };
    if (sample.id === 'sample_wage') {
      targetProfile = { state: 'Maharashtra', sector: 'Textile Factory', headcount: 85, contractor_involved: false, worker_type: 'Unskilled' };
    } else if (sample.id === 'sample_safety') {
      targetProfile = { state: 'Maharashtra', sector: 'Chemical Operations', headcount: 45, contractor_involved: false, worker_type: 'Hazardous' };
    } else {
      targetProfile = { state: 'Maharashtra', sector: 'Automobile Factory', headcount: 250, contractor_involved: true, worker_type: 'Skilled' };
    }
    setProfile(targetProfile);

    try {
      // Fetch real binary fixture file from backend
      const blob = await fetchFixtureBlob(sample.filename);
      const realFile = new File([blob], sample.filename, { type: blob.type || 'application/octet-stream' });
      setSelectedFile(realFile);

      await executePipeline(realFile, targetProfile);
    } catch (err) {
      console.error('[Sample Preset Error]', err);
      const msg = typeof err === 'string' ? err : (err.message || String(err));
      setError(msg || 'Could not load test fixture from backend server on http://localhost:8000');
      setLoading(false);
      setLoadingPhase('');
    }
  };

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      <Header />

      <main style={{ flex: 1, padding: '1.5rem 2rem', paddingTop: '5.5rem', maxWidth: '1600px', margin: '0 auto', width: '100%' }}>
        {/* Quick Demo Preset Selector */}
        <SampleLoader onSelectSample={handleSelectSample} loading={loading} />

        {/* Input Controls Grid */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(340px, 1fr))', gap: '1.25rem', marginBottom: '1.5rem' }}>
          <ProfileForm profile={profile} setProfile={setProfile} />
          <DocumentUploader 
            selectedFile={selectedFile} 
            setSelectedFile={setSelectedFile} 
            onAnalyze={handleAnalyze} 
            loading={loading} 
            loadingPhase={loadingPhase}
          />
        </div>

        {error && (
          <div style={{
            background: 'rgba(239, 68, 68, 0.15)',
            border: '1px solid rgba(239, 68, 68, 0.4)',
            color: '#f87171',
            padding: '0.85rem 1.25rem',
            borderRadius: '8px',
            marginBottom: '1.5rem',
            fontSize: '0.9rem',
            whiteSpace: 'pre-wrap',
            wordBreak: 'break-word'
          }}>
            ⚠️ {error}
          </div>
        )}

        {/* Results View — Document Evidence & Findings Workspace */}
        {extractionResult && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
            {/* Split Pane: Document Evidence Overlay + Extracted Fields List */}
            <div style={{ display: 'grid', gridTemplateColumns: '1.2fr 1fr', gap: '1.5rem', minHeight: '650px' }}>
              {/* Left Pane: Interactive Document Evidence Viewer */}
              <DocumentViewer 
                documentId={extractionResult.document_id}
                fields={extractionResult.fields || []}
                activeFieldId={activeFieldId}
                setActiveFieldId={setActiveFieldId}
              />

              {/* Right Pane: Quality Score Card & Extracted Fields List */}
              <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                <QualityCard documentQuality={extractionResult.document_quality} />
                <FieldExtractorPanel 
                  fields={extractionResult.fields || []}
                  activeFieldId={activeFieldId}
                  setActiveFieldId={setActiveFieldId}
                  extractionOutput={extractionResult}
                />
              </div>
            </div>

            {/* Findings Panel: Risk Scorecard, Employer/Inspector Action Toggle & Evidence Cross-Linking */}
            <FindingsPanel 
              findingsOutput={findingsResult}
              activeFieldId={activeFieldId}
              setActiveFieldId={setActiveFieldId}
              analysisError={analysisError}
            />
          </div>
        )}
      </main>
    </div>
  );
}
