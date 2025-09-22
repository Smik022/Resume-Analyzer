import React, { useState, useEffect } from "react";
import { uploadResume, analyzeResume } from "../services/api";
import Loader from "./Loader";
import ReportCard from "./ResultCard";
import "./UploadResumeForm.css";

function UploadResumeForm() {
  const [file, setFile] = useState(null);
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(false);
  const [loadingText, setLoadingText] = useState("Preparing upload...");

  const loadingMessages = [
    "Preparing upload...",
    "Uploading resume...",
    "Analyzing sections...",
    "Fetching skills...",
    "Generating report...",
    "Finalizing..."
  ];

  const handleFileChange = (e) => setFile(e.target.files[0]);

  // Dynamic loader text
  useEffect(() => {
    if (!loading) return;
    let i = 0;
    const interval = setInterval(() => {
      setLoadingText(loadingMessages[i % loadingMessages.length]);
      i++;
    }, 1000);

    return () => clearInterval(interval);
  }, [loading]);

  const handleUpload = async () => {
    if (!file) return alert("Select a file first");
    setLoading(true);
    setReport(null);

    try {
      const uploadRes = await uploadResume(file);
      const analysis = await analyzeResume(uploadRes.id);
      setReport(analysis);
    } catch (err) {
      console.error(err);
      alert("Something went wrong!");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="upload-form-container">
      <h2 className="title">Resume Analyzer</h2>

      <div className="upload-controls">
        <input type="file" onChange={handleFileChange} className="file-input" />
        <button onClick={handleUpload} className="upload-btn">
          Upload & Analyze
        </button>
      </div>

      {loading && <Loader text={loadingText} />}

      {report && <ReportCard report={report} />}
    </div>
  );
}

export default UploadResumeForm;
