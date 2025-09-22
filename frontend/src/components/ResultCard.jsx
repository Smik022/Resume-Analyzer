import React from "react";
import "./ResultCard.css";

function ResultCard({ report }) {
  return (
    <div className="result-card">
      <h2 className="result-title">Resume Analysis Results</h2>

      <div className="section">
        <div className="section-title">Overall Score</div>
        <div className="progress-bar-container">
          <div
            className="progress-bar overall"
            style={{ width: `${report.overall_score}%` }}
          >
            {report.overall_score}%
          </div>
        </div>
      </div>

      <div className="section">
        <div className="section-title">ATS Score</div>
        <div className="progress-bar-container">
          <div
            className="progress-bar ats"
            style={{ width: `${report.ats_score}%` }}
          >
            {report.ats_score}%
          </div>
        </div>
      </div>

      {Object.entries(report.improvement_suggestions).map(([section, suggestions]) => (
        <div className="section" key={section}>
          <div className="section-title">{section.toUpperCase()}</div>
          <div className="section-content">
            {suggestions.length ? (
              suggestions.map((s, idx) => (
                <div className="suggestion" key={idx}>
                  {s}
                </div>
              ))
            ) : (
              <div className="suggestion">No suggestions</div>
            )}
          </div>
        </div>
      ))}
    </div>
  );
}

export default ResultCard;
