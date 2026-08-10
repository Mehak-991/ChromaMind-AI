import React, { useState } from 'react';
import { Send, Sparkles, MessageSquare, Bot, HelpCircle } from 'lucide-react';
import { assistantService } from '../services/assistant.service';
import type { ChatMessage } from '../services/assistant.service';

export const Assistant: React.FC = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      role: 'assistant',
      content: 'Hello! I am your ChromaMind Copilot. Ask me anything about paint mixing models, color properties, or coordinate systems.'
    }
  ]);
  const [input, setInput] = useState('');
  const [sending, setSending] = useState(false);

  const suggestedQuestions = [
    "What is the physical meaning of L* a* b*?",
    "Why does adding white paint increase lightness?",
    "How does the Differential Evolution optimization work?"
  ];

  const handleSend = async (text: string) => {
    if (!text.trim()) return;
    const userMsg: ChatMessage = { role: 'user', content: text };
    setMessages((prev) => [...prev, userMsg]);
    setInput('');
    setSending(true);

    try {
      const res = await assistantService.chat(text);
      const assistantMsg: ChatMessage = { role: 'assistant', content: res.response };
      setMessages((prev) => [...prev, assistantMsg]);
    } catch (err) {
      console.warn("Backend chat unavailable, returning mock RAG explanation.");
      // Simulated response in case backend is not running
      setTimeout(() => {
        const assistantMsg: ChatMessage = {
          role: 'assistant',
          content: `In CIELAB space, L* represents lightness, while a* and b* are chromaticity coordinates. Lightness increases when titanium dioxide is added, scattering incident light.`
        };
        setMessages((prev) => [...prev, assistantMsg]);
        setSending(false);
      }, 500);
      return;
    }
    setSending(false);
  };

  return (
    <div className="max-w-5xl mx-auto h-[calc(100vh-10rem)] flex flex-col gap-6">
      {/* Page Title */}
      <div>
        <h1 className="text-3xl font-extrabold tracking-tight">AI Copilot</h1>
        <p className="text-slate-400 text-sm">Query the Retrieval-Augmented Generation agent regarding formulation logic.</p>
      </div>

      <div className="flex-1 glass border border-slate-900 rounded-xl overflow-hidden flex flex-col justify-between">
        {/* Chat message space */}
        <div className="flex-1 overflow-y-auto p-6 space-y-4">
          {messages.map((msg, index) => (
            <div
              key={index}
              className={`flex gap-3 max-w-[80%] ${msg.role === 'user' ? 'ml-auto flex-row-reverse' : ''}`}
            >
              <div className={`w-8 h-8 rounded-full flex items-center justify-center ${msg.role === 'user' ? 'bg-brand-500' : 'bg-slate-800'}`}>
                {msg.role === 'user' ? <MessageSquare size={14} /> : <Bot size={14} />}
              </div>
              <div className={`p-4 rounded-xl text-sm leading-relaxed ${msg.role === 'user' ? 'bg-brand-500 text-white rounded-tr-none' : 'bg-slate-900 text-slate-100 rounded-tl-none border border-slate-800'}`}>
                {msg.content}
              </div>
            </div>
          ))}
          {sending && (
            <div className="flex gap-3 max-w-[80%]">
              <div className="w-8 h-8 rounded-full bg-slate-800 flex items-center justify-center">
                <Bot size={14} />
              </div>
              <div className="p-4 bg-slate-900 border border-slate-800 rounded-xl text-sm text-slate-500 rounded-tl-none flex items-center gap-2">
                <Sparkles className="animate-spin text-brand-400" size={14} />
                Thinking...
              </div>
            </div>
          )}
        </div>

        {/* Input box and suggestion cards */}
        <div className="p-6 border-t border-slate-900 bg-slate-950/20 space-y-4">
          {messages.length === 1 && (
            <div className="space-y-2">
              <p className="text-[10px] font-semibold text-slate-500 flex items-center gap-1 uppercase">
                <HelpCircle size={10} />
                Suggested Questions
              </p>
              <div className="flex flex-wrap gap-2">
                {suggestedQuestions.map((q, idx) => (
                  <button
                    key={idx}
                    onClick={() => handleSend(q)}
                    className="text-xs px-3 py-1.5 bg-slate-900/60 border border-slate-850 hover:bg-slate-900 text-slate-400 hover:text-slate-200 rounded-lg transition-colors"
                  >
                    {q}
                  </button>
                ))}
              </div>
            </div>
          )}

          <div className="flex gap-2">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSend(input)}
              className="flex-1 bg-slate-900 border border-slate-800 focus:border-brand-500 rounded-lg px-4 py-2.5 text-sm text-slate-100 placeholder-slate-600 focus:outline-none transition-colors"
              placeholder="Ask a question about color science..."
            />
            <button
              onClick={() => handleSend(input)}
              className="px-4 bg-brand-500 hover:bg-brand-600 rounded-lg text-white transition-colors flex items-center justify-center"
            >
              <Send size={16} />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
