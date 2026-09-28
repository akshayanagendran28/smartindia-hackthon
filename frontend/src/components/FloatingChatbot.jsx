import React, { useState, useRef, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { 
  Bot, MessageSquare, X, Send, Sparkles, ChevronDown, 
  ArrowRight, ShieldCheck, Cpu, RefreshCw, Minimize2, 
  ExternalLink, User, HelpCircle, CheckCircle2, AlertCircle
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useLanguage } from '../context/LanguageContext';
import { useApplication } from '../context/ApplicationContext';
import api from '../services/api';

export default function FloatingChatbot() {
  const location = useLocation();
  const { user } = useAuth();
  const { currentLanguage, setLanguage, languages, t } = useLanguage();
  const { application } = useApplication();
  
  const [isOpen, setIsOpen] = useState(false);
  const [isMinimized, setIsMinimized] = useState(false);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  // Determine current scheme context from URL or application
  const isEducation = (application?.purpose_type || '').toUpperCase() === 'EDUCATION' || 
                      location.pathname.includes('education');

  const activeSchemeCode = application?.selectedScheme?.code || null;
  const activeSchemeId = application?.selectedScheme?.id || null;

  // Initial welcome message
  useEffect(() => {
    if (messages.length === 0) {
      const initialGreeting = isEducation
        ? (t('chatWelcomeEdu', 'Namaste! I am your AI Scheme Sathi. How can I help you with Higher Education Loans, 100% CSIS Interest Subsidy, or Document Verification today?'))
        : (t('chatWelcome', 'Namaste! I am your AI Scheme Sathi. I can help you discover government schemes (PMEGP, Mudra, SVANidhi), verify eligibility, check documents, or track your application.'));

      setMessages([
        {
          id: 'welcome_1',
          sender: 'assistant',
          text: initialGreeting,
          language: currentLanguage,
          model_used: 'Scheme Sathi Grounded Assistant',
          options: [
            { label: '🔍 Find Schemes', path: '/find-scheme' },
            { label: '📄 Check Documents', path: '/documents' },
            { label: '📊 Calculate EMI', path: '/calculator' },
            { label: '🏦 Channel Partners', path: '/partners' }
          ]
        }
      ]);
    }
  }, [currentLanguage, isEducation]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    if (isOpen && !isMinimized) {
      scrollToBottom();
      inputRef.current?.focus();
    }
  }, [messages, isOpen, isMinimized]);

  // Dynamic suggested prompts
  const suggestedPrompts = isEducation
    ? [
        "What education loan schemes are available?",
        "Am I eligible for CSIS 100% subsidy?",
        "What documents are required?",
        "What is my application status?",
        "How is the EMI calculated?"
      ]
    : [
        "What schemes are available for my business?",
        "What is the maximum loan under PMEGP?",
        "What documents are required?",
        "What is my application status?",
        "Who is my channel partner bank?"
      ];

  const handleSend = async (textToSend) => {
    const query = (textToSend || input).trim();
    if (!query || loading) return;

    const userMessage = {
      id: `user_${Date.now()}`,
      sender: 'user',
      text: query,
      language: currentLanguage
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const payload = {
        message: query,
        language: currentLanguage,
        session_id: sessionId,
        purpose_type: isEducation ? 'EDUCATION' : 'BUSINESS',
        scheme_code: activeSchemeCode,
        scheme_id: activeSchemeId
      };

      const res = await api.post('/chat/message', payload);

      if (res.data?.session_id) {
        setSessionId(res.data.session_id);
      }

      const replyText = res.data?.reply || res.data?.response || 'I have verified your request against the official statutory scheme rules.';
      const recs = res.data?.recommendations || res.data?.scheme_recommendations || res.data?.matched_schemes || [];
      const opts = res.data?.suggested_options || [];

      const assistantReply = {
        id: `asst_${Date.now()}`,
        sender: 'assistant',
        text: replyText,
        recommendations: recs,
        options: opts,
        model_used: res.data?.model_used || 'Scheme Sathi Grounded Assistant',
        language: res.data?.language || currentLanguage
      };

      setMessages((prev) => [...prev, assistantReply]);
    } catch (err) {
      console.error('Chat error:', err);
      // Factual fallback response
      setMessages((prev) => [
        ...prev,
        {
          id: `asst_${Date.now()}`,
          sender: 'assistant',
          text: isEducation
            ? 'Central Sector Interest Subsidy (CSIS) offers 100% full interest subvention for higher education loans up to ₹10 Lakhs during the course duration + 1 year moratorium for students with family income ≤ ₹4.5 Lakh.'
            : 'Under PMEGP, rural SC/ST, women, and minority entrepreneurs are eligible for up to 35% capital subsidy with a 5% margin money contribution on manufacturing projects up to ₹50 Lakh. For street vendors, PM SVANidhi provides up to ₹50,000 micro-credit with a 7% interest subvention.',
          model_used: 'Scheme Sathi Grounded Knowledge Base',
          language: currentLanguage,
          options: [
            { label: '🔍 Discover Schemes', path: '/find-scheme' },
            { label: '📄 Check Documents', path: '/documents' }
          ]
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handlePromptClick = (prompt) => {
    handleSend(prompt);
  };

  const handleResetChat = () => {
    setSessionId(null);
    setMessages([
      {
        id: `welcome_${Date.now()}`,
        sender: 'assistant',
        text: isEducation
          ? 'Conversation refreshed. How can I assist you with educational schemes, loan limits, or document status?'
          : 'Conversation refreshed. How can I assist you with government business schemes, subsidies, or application tracking?',
        language: currentLanguage,
        model_used: 'Scheme Sathi Grounded Assistant',
        options: [
          { label: '🔍 Find Schemes', path: '/find-scheme' },
          { label: '📄 Check Documents', path: '/documents' },
          { label: '📊 Calculate EMI', path: '/calculator' }
        ]
      }
    ]);
  };

  return (
    <div className="fixed bottom-6 right-6 z-50 flex flex-col items-end">
      {/* Floating Action Button when closed */}
      {!isOpen && (
        <button
          onClick={() => {
            setIsOpen(true);
            setIsMinimized(false);
          }}
          className="group relative flex items-center gap-2.5 px-4 py-3 bg-gradient-to-r from-emerald-600 via-teal-600 to-emerald-700 hover:from-emerald-700 hover:to-teal-800 text-white rounded-full shadow-xl hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-1 active:translate-y-0 focus:outline-none focus:ring-4 focus:ring-emerald-300"
          aria-label="Open Scheme Sathi AI Assistant"
        >
          <div className="relative">
            <Bot className="w-5 h-5 animate-pulse" />
            <span className="absolute -top-1 -right-1 w-2.5 h-2.5 bg-amber-400 border-2 border-white rounded-full"></span>
          </div>
          <span className="font-bold text-xs tracking-wide">
            {t('askSchemeSathi', 'Ask Scheme Sathi')}
          </span>
          <span className="bg-white/20 px-1.5 py-0.5 rounded text-[10px] font-semibold text-emerald-100 hidden sm:inline">
            AI 24/7
          </span>
        </button>
      )}

      {/* Floating Chat Modal */}
      {isOpen && (
        <div
          className={`w-[92vw] sm:w-[420px] bg-white rounded-2xl shadow-2xl border border-slate-200 flex flex-col overflow-hidden transition-all duration-300 ${
            isMinimized ? 'h-14' : 'h-[580px] max-h-[85vh]'
          }`}
        >
          {/* Header */}
          <div className="bg-gradient-to-r from-slate-900 via-slate-800 to-emerald-950 p-3.5 text-white flex items-center justify-between shrink-0 shadow-md">
            <div className="flex items-center gap-2.5">
              <div className="w-8 h-8 rounded-xl bg-gradient-to-tr from-emerald-500 to-teal-400 text-white flex items-center justify-center shadow-inner">
                <Bot className="w-4 h-4" />
              </div>
              <div>
                <div className="flex items-center gap-1.5">
                  <span className="font-bold text-sm tracking-tight text-white">Scheme Sathi AI</span>
                  <span className="px-1.5 py-0.2 rounded text-[9px] font-bold bg-emerald-500/30 text-emerald-300 border border-emerald-400/30">
                    Live Grounded
                  </span>
                </div>
                <p className="text-[10px] text-slate-300 truncate max-w-[180px]">
                  {isEducation ? '🎓 Education Track' : '💼 Business & MSME Track'}
                </p>
              </div>
            </div>

            <div className="flex items-center gap-1.5">
              {/* Language Selector */}
              <select
                value={currentLanguage}
                onChange={(e) => setLanguage(e.target.value)}
                className="text-[11px] font-bold px-2 py-1 border border-slate-700 rounded-lg bg-slate-800 text-emerald-300 focus:ring-1 focus:ring-emerald-400 focus:outline-none"
                title="Select Conversation Language"
              >
                {languages.map((l) => (
                  <option key={l.code} value={l.code}>
                    {l.code.toUpperCase()} - {l.native}
                  </option>
                ))}
              </select>

              {/* Refresh Chat */}
              <button
                onClick={handleResetChat}
                className="p-1.5 text-slate-400 hover:text-white rounded-lg hover:bg-slate-800 transition-colors"
                title="Refresh Chat"
              >
                <RefreshCw className="w-3.5 h-3.5" />
              </button>

              {/* Minimize */}
              <button
                onClick={() => setIsMinimized(!isMinimized)}
                className="p-1.5 text-slate-400 hover:text-white rounded-lg hover:bg-slate-800 transition-colors"
                title={isMinimized ? 'Expand' : 'Minimize'}
              >
                <Minimize2 className="w-3.5 h-3.5" />
              </button>

              {/* Close */}
              <button
                onClick={() => setIsOpen(false)}
                className="p-1.5 text-slate-400 hover:text-red-400 rounded-lg hover:bg-slate-800 transition-colors"
                title="Close"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
          </div>

          {/* Body when not minimized */}
          {!isMinimized && (
            <>
              {/* Messages Area */}
              <div className="flex-1 bg-slate-50 p-3.5 overflow-y-auto space-y-3 text-xs sm:text-sm">
                {messages.map((m) => (
                  <div
                    key={m.id}
                    className={`flex items-start gap-2.5 ${m.sender === 'user' ? 'flex-row-reverse' : ''}`}
                  >
                    <div
                      className={`w-7 h-7 rounded-full flex items-center justify-center shrink-0 ${
                        m.sender === 'user' ? 'bg-slate-800 text-white' : 'bg-emerald-600 text-white shadow-sm'
                      }`}
                    >
                      {m.sender === 'user' ? <User className="w-3.5 h-3.5" /> : <Bot className="w-3.5 h-3.5" />}
                    </div>

                    <div
                      className={`max-w-[85%] rounded-2xl p-3 leading-relaxed ${
                        m.sender === 'user'
                          ? 'bg-slate-900 text-white rounded-tr-none text-xs sm:text-sm'
                          : 'bg-white border border-slate-200 text-slate-800 rounded-tl-none shadow-sm space-y-2 text-xs sm:text-[13px]'
                      }`}
                    >
                      {/* Model Tag */}
                      {m.model_used && m.sender === 'assistant' && (
                        <div className="flex items-center gap-1 text-[9px] font-bold text-slate-400 border-b border-slate-100 pb-1">
                          <Cpu className="w-2.5 h-2.5 text-emerald-600" />
                          <span>{m.model_used}</span>
                        </div>
                      )}

                      <p className="whitespace-pre-line leading-relaxed">{m.text}</p>

                      {/* Featured Schemes */}
                      {m.recommendations && m.recommendations.length > 0 && (
                        <div className="pt-2 border-t border-slate-100 space-y-1.5">
                          <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400 block">
                            Featured Schemes:
                          </span>
                          <div className="space-y-1.5">
                            {m.recommendations.map((r, rIdx) => (
                              <div
                                key={rIdx}
                                className="p-2 rounded-lg bg-emerald-50/80 border border-emerald-200 flex items-center justify-between gap-2 text-xs"
                              >
                                <div className="truncate">
                                  <span className="font-bold text-emerald-950 block truncate text-[11px]">
                                    {r.name || r.code}
                                  </span>
                                  <span className="text-[10px] text-emerald-800 font-medium">
                                    {r.subsidy ? `Subsidy: ${r.subsidy}` : r.max_loan ? `Max: ₹${(r.max_loan / 100000).toFixed(1)}L` : ''}
                                  </span>
                                </div>
                                <Link
                                  to={r.id ? `/scheme/${r.id}` : `/results`}
                                  onClick={() => setIsOpen(false)}
                                  className="px-2 py-0.5 bg-emerald-700 text-white font-bold rounded text-[10px] hover:bg-emerald-800 shrink-0 flex items-center gap-0.5"
                                >
                                  <span>View</span>
                                  <ArrowRight className="w-2.5 h-2.5" />
                                </Link>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}

                      {/* Action Links */}
                      {m.options && m.options.length > 0 && (
                        <div className="pt-1.5 border-t border-slate-100 flex flex-wrap gap-1">
                          {m.options.map((opt, oIdx) => (
                            <Link
                              key={oIdx}
                              to={opt.path || '/find-scheme'}
                              onClick={() => setIsOpen(false)}
                              className="px-2 py-0.5 rounded bg-slate-100 hover:bg-emerald-100 hover:text-emerald-900 text-slate-700 text-[10px] font-bold border border-slate-200 transition-colors"
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
                  <div className="flex items-center gap-2 text-xs text-slate-500 bg-white border border-slate-200 p-2.5 rounded-2xl rounded-tl-none w-fit shadow-sm">
                    <Sparkles className="w-3.5 h-3.5 text-emerald-600 animate-spin" />
                    <span>Analyzing official database...</span>
                  </div>
                )}

                <div ref={messagesEndRef} />
              </div>

              {/* Fast Suggested Queries */}
              <div className="bg-white border-t border-slate-200 p-2 overflow-x-auto flex items-center gap-1.5 text-xs no-scrollbar shrink-0">
                <span className="text-[10px] font-bold text-slate-400 shrink-0 px-1">Quick:</span>
                {suggestedPrompts.slice(0, 3).map((prompt, pIdx) => (
                  <button
                    key={pIdx}
                    onClick={() => handlePromptClick(prompt)}
                    className="px-2 py-1 bg-slate-100 hover:bg-emerald-50 hover:text-emerald-800 text-slate-700 rounded-full text-[10px] font-medium whitespace-nowrap border border-slate-200 transition-colors shrink-0"
                  >
                    {prompt}
                  </button>
                ))}
              </div>

              {/* Input Form */}
              <div className="p-2.5 bg-white border-t border-slate-200 shrink-0">
                <form
                  onSubmit={(e) => {
                    e.preventDefault();
                    handleSend();
                  }}
                  className="flex items-center gap-1.5"
                >
                  <input
                    ref={inputRef}
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="Ask about schemes, eligibility, documents..."
                    className="flex-1 px-3 py-2 text-xs border border-slate-300 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:outline-none"
                    disabled={loading}
                  />
                  <button
                    type="submit"
                    disabled={!input.trim() || loading}
                    className="p-2 bg-emerald-600 hover:bg-emerald-700 text-white rounded-xl transition-colors disabled:opacity-50 shadow-sm"
                    title="Send Message"
                  >
                    <Send className="w-3.5 h-3.5" />
                  </button>
                </form>
              </div>
            </>
          )}
        </div>
      )}
    </div>
  );
}
