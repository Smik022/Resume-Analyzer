import React from "react";
import "./Loader.css";

function Loader({ text }) {
  return (
    <div className="loader-container">
      <div className="spinner"></div>
      <p className="loader-text">{text}</p>
    </div>
  );
}

export default Loader;
