// src/App.jsx

import React, { useState } from "react";
import FileUploader from "./components/FileUploader";
import ChatWindow from "./components/ChatWindow";
import SourceList from "./components/SourceList";

function App() {
  const [ready, setReady] = useState(false);   // true once upload+index completes
  const [sources, setSources] = useState([]);  // chunks returned by query

  return (
    <div style={{ maxWidth: 600, margin: "auto", padding: 20 }}>
      <h1>📄 Contract Companion</h1>

      {/* Step 1: Upload */}
      <FileUploader onUploaded={() => setReady(true)} />

      {/* Step 2: Ask */}
      {ready && (
        <ChatWindow
          disabled={!ready}
          onSources={(srcs) => setSources(srcs)}
        />
      )}

      {/* Step 3: Show citations */}
      <SourceList sources={sources} />
    </div>
  );
}

export default App;
