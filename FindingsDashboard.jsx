import { useState } from "react";

const TIER_COLORS = {
  low: "#2e7d32",
  medium: "#f9a825",
  high: "#c62828",
};

function FindingCard({ finding, onEvidenceClick, view }) {
  const isCannotDetermine = finding.type === "cannot_determine";

  return (
    <div style={{
      border: "1px solid #ddd",
      borderRadius: 8,
      padding: 16,
      marginBottom: 12,
      background: isCannotDetermine ? "#f5f5f5" : "#fff",
    }}>
      <div style={{ display: "flex", justifyContent: "space-between" }}>
        <strong style={{ textTransform: "uppercase", fontSize: 12 }}>
          {finding.type.replace("_", " ")}
        </strong>
        {finding.severity && (
          <span style={{ fontSize: 12, color: "#888" }}>
            Severity: {finding.severity}/5
          </span>
        )}
      </div>

      <p style={{ margin: "8px 0" }}>{finding.explanation}</p>

      {finding.citation && (
        <p style={{ fontSize: 13, color: "#555" }}>
          📖 {finding.citation.code}, {finding.citation.section}
        </p>
      )}

      {finding.confidence && (
        <p style={{ fontSize: 12, color: "#888" }}>
          Confidence: {finding.confidence}
        </p>
      )}

      {isCannotDetermine && (
        <p style={{ fontSize: 13, color: "#c62828" }}>
          ⚠ {finding.reason}
        </p>
      )}

      {!isCannotDetermine && (
        <p style={{ fontSize: 13, fontStyle: "italic" }}>
          {view === "employer" ? finding.employer_action : finding.inspector_action}
        </p>
      )}

      {finding.related_field_id && (
        <button
          onClick={() => onEvidenceClick?.(finding.related_field_id)}
          style={{ marginTop: 8, fontSize: 12 }}
        >
          🔍 Jump to evidence
        </button>
      )}
    </div>
  );
}

export default function FindingsDashboard({ findingsOutput, onEvidenceClick }) {
  const [view, setView] = useState("employer");

  if (!findingsOutput) return <p>No findings yet — upload a document to analyze.</p>;

  return (
    <div style={{ maxWidth: 600, margin: "0 auto" }}>
      <div style={{
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        marginBottom: 16,
      }}>
        <h2>Risk Scorecard</h2>
        <div style={{
          background: TIER_COLORS[findingsOutput.risk_tier],
          color: "#fff",
          padding: "4px 12px",
          borderRadius: 12,
          fontWeight: "bold",
        }}>
          {findingsOutput.risk_tier.toUpperCase()} ({findingsOutput.risk_score} pts)
        </div>
      </div>

      <div style={{ marginBottom: 16 }}>
        <button
          onClick={() => setView("employer")}
          style={{ fontWeight: view === "employer" ? "bold" : "normal", marginRight: 8 }}
        >
          Employer View
        </button>
        <button
          onClick={() => setView("inspector")}
          style={{ fontWeight: view === "inspector" ? "bold" : "normal" }}
        >
          Inspector View
        </button>
      </div>

      {findingsOutput.findings.map((f) => (
        <FindingCard
          key={f.finding_id}
          finding={f}
          view={view}
          onEvidenceClick={onEvidenceClick}
        />
      ))}
    </div>
  );
}