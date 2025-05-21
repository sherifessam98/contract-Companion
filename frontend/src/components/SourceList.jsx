import React from "react";

export default function SourceList({ sources }) {
  if (!sources || sources.length === 0) return null;
  return (
    <div>
      <h4>Source Chunks:</h4>
      {sources.map((chunk, idx) => (
        <div key={idx} style={{ border: "1px solid #ddd", margin: "8px", padding: "8px" }}>
          <strong>Chunk {idx + 1}:</strong>
          <p>{chunk}</p>
        </div>
      ))}
    </div>
  );
}