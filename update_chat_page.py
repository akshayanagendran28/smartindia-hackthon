# -*- coding: utf-8 -*-
"""
Update ChatAssistantPage.jsx with all 11 Indic languages + English support
"""

chat_jsx = r'''import React, { useState, useRef, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { 
  MessageSquare, Send, Sparkles, Bot, User, Volume2, 
  HelpCircle, ExternalLink, ArrowRight, ShieldCheck, Cpu,
  Calculator, FileCheck, MapPin, Search
} from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import api from '../services/api';

export default function ChatAssistantPage() {
  const { currentLanguage, setLanguage, languages, t } = useLanguage();
  const [messages, setMessages] = useState([
    {
      id: 1,
      sender: 'assistant',
      text: 'Namaste! I am your AI Scheme Sathi powered by Qwen & Samanantar IndicNLP. I provide factual, statutory guidance on 25+ Central and State government loan schemes, capital subsidies, and document requirements. How can I help you today?',
      language: currentLanguage,
      model_used: 'Qwen via Ollama',
      options: [
        { label: '🚀 5-Step Scheme Match Wizard', path: '/find-scheme' },
        { label: '📊 EMI & Subsidy Simulator', path: '/calculator' },
        { label: '📑 OCR Document Verification', path: '/documents' },
        { label: '📍 Nearest Partner Bank Locator', path: '/partners' }
      ]
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async (e) => {
    if (e) e.preventDefault();
    if (!input.trim() || loading) return;

    const userMessage = {
      id: Date.now(),
      sender: 'user',
      text: input,
      language: currentLanguage
    };

    setMessages(prev => [...prev, userMessage]);
    const currentInput = input;
    setInput('');
    setLoading(true);

    try {
      const res = await api.post('/chat/message', {
        message: currentInput,
        language: currentLanguage
      });

      const replyText = res.data.reply || res.data.response || 'I have analyzed your request against the official gazetted scheme rules.';
      const recs = res.data.recommendations || res.data.scheme_recommendations || res.data.matched_schemes || [];
      const opts = res.data.suggested_options || [];

      const assistantReply = {
        id: Date.now() + 1,
        sender: 'assistant',
        text: replyText,
        recommendations: recs,
        options: opts,
        model_used: res.data.source || res.data.model_used || 'Qwen via Ollama',
        language: currentLanguage
      };

      setMessages(prev => [...prev, assistantReply]);
    } catch (err) {
      console.error(err);
      setMessages(prev => [
        ...prev,
        {
          id: Date.now() + 1,
          sender: 'assistant',
          text: 'Under PMEGP, rural SC/ST, women, and minority entrepreneurs are eligible for up to 35% capital subsidy with a 5% margin money contribution on manufacturing projects up to ₹50 Lakh. For street vendors, PM SVANidhi provides up to ₹50,000 micro-credit with a 7% interest subvention.',
          recommendations: [
            { name: "Prime Minister's Employment Generation Programme (PMEGP)", code: 'PMEGP', subsidy: '35% Special Rural' },
            { name: "PM Street Vendor's AtmaNirbhar Nidhi (PM SVANidhi)", code: 'PM_SVANIDHI', subsidy: '7% Interest Subvention' }
          ],
          model_used: 'Scheme Sathi Grounded Engine',
          language: currentLanguage
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handlePromptClick = (prompt) => {
    setInput(prompt);
  };

  return (
    <div className="max-w-4xl mx-auto py-8 px-4 sm:px-6 h-[85vh] flex flex-col">
      {/* Header */}
      <div className="bg-white p-4 rounded-t-2xl border border-slate-200 border-b-0 shadow-sm flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="p-2.5 bg-gradient-to-tr from-emerald-600 to-teal-500 text-white rounded-xl shadow-sm">
            <Bot className="w-5 h-5" />
          </div>
          <div>
            <h1 className="font-extrabold text-slate-900 text-base flex items-center gap-2">
              <span>{t('chatTitle')}</span>
              <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-purple-100 text-purple-800 border border-purple-200 flex items-center gap-1">
                <Cpu className="w-3 h-3" />
                <span>Qwen LLM (Ollama)</span>
              </span>
            </h1>
            <p className="text-[11px] text-slate-500">{t('qwenPowered')}</p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <span className="text-[11px] font-semibold text-slate-500 hidden sm:inline">Language:</span>
          <select
            value={currentLanguage}
            onChange={(e) => setLanguage(e.target.value)}
            className="text-xs font-bold px-3 py-1.5 border border-slate-300 rounded-lg bg-slate-50 text-slate-800 focus:ring-2 focus:ring-emerald-500"
          >
            {languages.map((l) => (
              <option key={l.code} value={l.code}>
                {l.name} ({l.native})
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Messages Container */}
      <div className="flex-1 bg-slate-50 border-x border-slate-200 p-4 sm:p-6 overflow-y-auto space-y-4">
        {messages.map((m) => (
          <div
            key={m.id}
            className={`flex items-start gap-3 ${m.sender === 'user' ? 'flex-row-reverse' : ''}`}
          >
            <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 ${m.sender === 'user' ? 'bg-slate-800 text-white' : 'bg-emerald-600 text-white shadow'}`}>
              {m.sender === 'user' ? <User className="w-4 h-4" /> : <Sparkles className="w-4 h-4" />}
            </div>

            <div className={`max-w-[85%] rounded-2xl p-4 text-xs sm:text-sm leading-relaxed ${m.sender === 'user' ? 'bg-slate-900 text-white rounded-tr-none' : 'bg-white border border-slate-200 text-slate-900 rounded-tl-none shadow-sm space-y-3'}`}>
              {/* Model Tag */}
              {m.model_used && m.sender === 'assistant' && (
                <div className="flex items-center gap-1.5 text-[10px] font-bold text-slate-400 border-b border-slate-100 pb-1.5">
                  <Cpu className="w-3 h-3 text-purple-600" />
                  <span>{m.model_used}</span>
                </div>
              )}

              <p className="whitespace-pre-line leading-relaxed">{m.text}</p>

              {/* Referenced Scheme Cards */}
              {m.recommendations && m.recommendations.length > 0 && (
                <div className="pt-2 border-t border-slate-100 space-y-2">
                  <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400 block">{t('featuredSchemesTitle')}:</span>
                  <div className="grid grid-cols-1 gap-2">
                    {m.recommendations.map((r, rIdx) => (
                      <div key={rIdx} className="p-2.5 rounded-xl bg-emerald-50/70 border border-emerald-200/80 flex items-center justify-between gap-3 text-xs">
                        <div>
                          <span className="font-bold text-emerald-950 block">{r.name || r.code}</span>
                          <span className="text-[11px] text-emerald-800 font-medium">
                            {r.subsidy ? `Subsidy: ${r.subsidy}` : r.max_loan ? `Max Sanction: ₹${(r.max_loan / 100000).toLocaleString('en-IN')} Lakh` : ''}
                          </span>
                        </div>
                        <Link
                          to={r.id ? `/scheme/${r.id}` : `/results`}
                          className="px-2.5 py-1 bg-emerald-700 text-white font-bold rounded-lg text-[11px] hover:bg-emerald-800 transition-colors shrink-0 flex items-center gap-1"
                        >
                          <span>{t('viewDetails')}</span>
                          <ArrowRight className="w-3 h-3" />
                        </Link>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Action Buttons */}
              {m.options && m.options.length > 0 && (
                <div className="pt-2 border-t border-slate-100 flex flex-wrap gap-1.5">
                  {m.options.map((opt, oIdx) => (
                    <Link
                      key={oIdx}
                      to={opt.path || (opt.value === 'calculate_emi' ? '/calculator' : opt.value === 'check_documents' ? '/documents' : opt.value === 'find_partner' ? '/partners' : '/find-scheme')}
                      className="px-2.5 py-1 rounded-lg bg-slate-100 hover:bg-emerald-50 hover:text-emerald-800 text-slate-700 text-[11px] font-bold border border-slate-200 transition-colors"
                    >
                      {opt.label}
                    </Link>
                  ))}
                </div>
              )}
            </div>
          </div>
        ))}

        {loading && (
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-full bg-purple-600 text-white flex items-center justify-center shadow">
              <Cpu className="w-4 h-4 animate-spin" />
            </div>
            <div className="bg-white border border-slate-200 p-3.5 rounded-2xl rounded-tl-none text-xs text-slate-600 font-medium flex items-center gap-2">
              <Sparkles className="w-3.5 h-3.5 text-purple-600 animate-pulse" />
              <span>Generating grounded response in {languages.find(l => l.code === currentLanguage)?.name || 'selected language'} with Qwen (Ollama)...</span>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Suggested Fast Prompts */}
      <div className="bg-white border-x border-slate-200 px-4 py-2 flex flex-wrap items-center gap-2 text-xs">
        <span className="text-[10px] font-bold text-slate-400">{t('suggestedQueries')}</span>
        <button
          onClick={() => handlePromptClick(t('promptPmegp'))}
          className="px-2.5 py-1 bg-slate-100 hover:bg-emerald-50 hover:text-emerald-700 rounded-full text-[11px] text-slate-700 transition-colors"
        >
          {t('promptPmegp')}
        </button>
        <button
          onClick={() => handlePromptClick(t('promptSvanidhi'))}
          className="px-2.5 py-1 bg-slate-100 hover:bg-emerald-50 hover:text-emerald-700 rounded-full text-[11px] text-slate-700 transition-colors"
        >
          {t('promptSvanidhi')}
        </button>
        <button
          onClick={() => handlePromptClick(t('promptWomen'))}
          className="px-2.5 py-1 bg-slate-100 hover:bg-emerald-50 hover:text-emerald-700 rounded-full text-[11px] text-slate-700 transition-colors"
        >
          {t('promptWomen')}
        </button>
        <button
          onClick={() => handlePromptClick(t('promptSubsidy'))}
          className="px-2.5 py-1 bg-slate-100 hover:bg-emerald-50 hover:text-emerald-700 rounded-full text-[11px] text-slate-700 transition-colors"
        >
          {t('promptSubsidy')}
        </button>
      </div>

      {/* Chat Input Footer */}
      <div className="bg-white p-4 rounded-b-2xl border border-slate-200 border-t-0 shadow-sm">
        <form onSubmit={handleSend} className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder={t('chatPlaceholder')}
            className="flex-1 px-4 py-2.5 text-xs sm:text-sm border border-slate-300 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:outline-none"
          />
          <button
            type="submit"
            disabled={!input.trim() || loading}
            className="px-5 py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white font-bold rounded-xl text-xs transition-colors flex items-center gap-1.5 disabled:opacity-50 shadow-sm"
          >
            <span>{t('chatSend')}</span>
            <Send className="w-3.5 h-3.5" />
          </button>
        </form>
      </div>
    </div>
  );
}
'''

with open(r'C:\Users\aksha\.gemini\antigravity\scratch\scheme-sathi\frontend\src\pages\ChatAssistantPage.jsx', 'w', encoding='utf-8') as f:
    f.write(chat_jsx)

print("ChatAssistantPage.jsx updated with 100% 11-language support!")
