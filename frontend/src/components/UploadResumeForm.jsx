import React, { useState } from "react";
import { uploadResume, analyzeResume } from "../services/api";

function UploadResumeForm() {
  const [file, setFile] = useState(null);
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => setFile(e.target.files[0]);

  const handleUpload = async () => {
    if (!file) return alert("Select a file first");

    setLoading(true);
    try {
      // Upload file
      const uploadRes = await uploadResume(file);
      if (uploadRes.id) {
        // Analyze uploaded resume
        const analysis = await analyzeResume(uploadRes.id);
        setReport(analysis);
      }
    } catch (err) {
      console.error(err);
      alert("Error uploading or analyzing resume.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: "800px", margin: "20px auto", fontFamily: "Arial, sans-serif" }}>
      <h2>Resume Analyzer</h2>

      <input type="file" onChange={handleFileChange} />
      <button onClick={handleUpload} disabled={loading} style={{ marginLeft: "10px" }}>
        {loading ? "Processing..." : "Upload & Analyze"}
      </button>

      {report && (
        <div style={{ marginTop: "20px", padding: "10px", border: "1px solid #ccc", borderRadius: "5px" }}>
          <h3>Overall Score: {report.overall_score}</h3>
          <h4>ATS Score: {report.ats_score}</h4>

          <h4>Improvement Suggestions:</h4>
          {report.improvement_suggestions && Object.entries(report.improvement_suggestions).map(([section, suggestions]) => (
            <div key={section} style={{ marginBottom: "15px" }}>
              <strong>{section.charAt(0).toUpperCase() + section.slice(1)}:</strong>
              <ul>
                {suggestions.length ? suggestions.map((s, i) => <li key={i}>{s}</li>) : <li>No suggestions</li>}
              </ul>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default UploadResumeForm;
