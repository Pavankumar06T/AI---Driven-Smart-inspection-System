const isLocal = typeof window !== 'undefined' && (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1');

const DEFAULT_API = isLocal ? 'http://localhost:8000' : 'https://shram-doc-intel-backend.onrender.com';
const DEFAULT_REASONING_API = isLocal ? 'http://localhost:8001' : 'https://shram-compliance-reasoning-backend.onrender.com';

function formatUrl(url, fallback) {
  const target = (url && url !== 'undefined') ? url : fallback;
  if (!target.startsWith('http://') && !target.startsWith('https://')) {
    return `https://${target}`.replace(/\/$/, '');
  }
  return target.replace(/\/$/, '');
}

const API_BASE_URL = formatUrl(import.meta.env.VITE_API_BASE_URL, DEFAULT_API);
const REASONING_API_BASE_URL = formatUrl(import.meta.env.VITE_REASONING_API_BASE_URL, DEFAULT_REASONING_API);




export async function analyzeDocument(extractionOutput) {
  const response = await fetch(`${REASONING_API_BASE_URL}/analyze`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(extractionOutput)
  });

  if (!response.ok) {
    const errorJson = await response.json().catch(() => null);
    throw new Error(formatErrorMessage(errorJson, 'Compliance analysis failed'));
  }

  return await response.json();
}


function formatErrorMessage(errorObj, fallbackText = 'Request failed') {
  if (!errorObj) return fallbackText;
  if (typeof errorObj === 'string') return errorObj;
  
  if (errorObj.detail) {
    if (typeof errorObj.detail === 'string') return errorObj.detail;
    if (Array.isArray(errorObj.detail)) {
      return errorObj.detail
        .map(item => `${item.loc ? item.loc.join('.') : 'error'}: ${item.msg || JSON.stringify(item)}`)
        .join('; ');
    }
    if (typeof errorObj.detail === 'object') {
      return errorObj.detail.msg || errorObj.detail.message || JSON.stringify(errorObj.detail);
    }
  }

  if (errorObj.message) return errorObj.message;
  return JSON.stringify(errorObj);
}

export async function saveEstablishmentProfile(profileData) {
  const response = await fetch(`${API_BASE_URL}/profile`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(profileData)
  });
  if (!response.ok) {
    const errorJson = await response.json().catch(() => null);
    throw new Error(formatErrorMessage(errorJson, 'Failed to save profile'));
  }
  return await response.json();
}

export async function extractDocument(file, profileData, documentId = null) {
  const formData = new FormData();
  formData.append('file', file);
  
  if (documentId) formData.append('document_id', documentId);
  if (profileData.state) formData.append('state', profileData.state);
  if (profileData.sector) formData.append('sector', profileData.sector);
  if (profileData.headcount !== null && profileData.headcount !== undefined) {
    formData.append('headcount', profileData.headcount);
  }
  if (profileData.contractor_involved !== null && profileData.contractor_involved !== undefined) {
    formData.append('contractor_involved', profileData.contractor_involved);
  }
  if (profileData.worker_type) formData.append('worker_type', profileData.worker_type);

  const response = await fetch(`${API_BASE_URL}/extract`, {
    method: 'POST',
    body: formData
  });

  if (!response.ok) {
    const errorJson = await response.json().catch(() => null);
    throw new Error(formatErrorMessage(errorJson, 'Document extraction failed'));
  }

  return await response.json();
}

export async function fetchFixtureBlob(filename) {
  const response = await fetch(`${API_BASE_URL}/fixtures/${filename}`);
  if (!response.ok) {
    throw new Error(`Failed to load fixture '${filename}' from backend server.`);
  }
  return await response.blob();
}

export async function getDocumentExtraction(documentId) {
  const response = await fetch(`${API_BASE_URL}/documents/${documentId}`);
  if (!response.ok) {
    throw new Error('Document extraction not found');
  }
  return await response.json();
}

export function getPageImageUrl(documentId, pageNum = 1) {
  return `${API_BASE_URL}/documents/${documentId}/pages/${pageNum}`;
}
