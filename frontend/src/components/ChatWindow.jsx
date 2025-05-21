import React, { useState } from "react";
import { askQuestion } from "../services/api";

export default function ChatWindow({ disabled, onSources }) {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);

  // sending the question to the backend
  const handleAsk = async () => {
    if (!question) return;
    setLoading(true); // start loading animation

    try {
      const res = await askQuestion(question); // send to backend
      setAnswer(res.data.answer); // show the reply
      onSources(res.data.sources); // pass sources to parent
    } catch (err) {
      setAnswer("Error generating answer.");
      console.error(err);
    } finally {
      setLoading(false); // always stop loading
    }
  };

  return (
    <div>
      <input
        type="text"
        placeholder="Ask a question..."
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        disabled={disabled}
      />
      <button onClick={handleAsk} disabled={disabled || loading}>
        {loading ? "Thinking…" : "Ask"}
      </button>
      <div>
        <strong>Answer:</strong>
        <p>{answer}</p>
      </div>
    </div>
  );
}
