const BASE_URL = "http://127.0.0.1:8000/api/analyzer"; // include /api/analyzer

export const uploadResume = async (file) => {
  const formData = new FormData();
  formData.append("file", file); // matches your Django view

  const res = await fetch(`${BASE_URL}/upload/`, {
    method: "POST",
    body: formData,
  });

  return res.json();
};

export const analyzeResume = async (resumeId) => {
  const res = await fetch(`${BASE_URL}/analyze/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ resume_id: resumeId }),
  });

  return res.json();
};
