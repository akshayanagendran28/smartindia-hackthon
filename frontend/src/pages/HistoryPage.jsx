import React, { useState, useEffect } from 'react';
import { 
  History, Award, CheckCircle2, ArrowRight, ShieldCheck, Clock, 
  Building2, Landmark, RefreshCw, AlertCircle, FileText, Check, 
  ExternalLink, UserCheck, Sparkles, Send, Eye, XCircle,
  Calendar, DollarSign, Phone, MapPin, AlertTriangle, CheckCircle,
  TrendingUp, CreditCard
} from 'lucide-react';
import { Link, useNavigate } from 'react-router-dom';
import { useApplication } from '../context/ApplicationContext';
import { useLanguage } from '../context/LanguageContext';
import { applicationsAPI } from '../services/api';
import api from '../services/api';

export default function HistoryPage() {
  const { t } = useLanguage();
  const navigate = useNavigate();
  const { application, purposeType, selectedScheme, loanAmount } = useApplication();

  const [applications, setApplications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [filterPurpose, setFilterPurpose] = useState('ALL');
  const [actionLoadingId, setActionLoadingId] = useState(null);
  const [notificationMsg, setNotificationMsg] = useState(null);
  const [creatingDemo, setCreatingDemo] = useState(false);
  const [lastSyncedTime, setLastSyncedTime] = useState(new Date().toLocaleTimeString('en-IN'));

  const fetchApplications = async (isManual = false) => {
    if (isManual) setRefreshing(true);
    try {
      const res = await applicationsAPI.getMyApplications();
      if (res.data && Array.isArray(res.data)) {
        setApplications(res.data);
      }
      setLastSyncedTime(new Date().toLocaleTimeString('en-IN'));
    } catch (err) {
      console.warn('Could not fetch applications from API:', err);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  useEffect(() => {
    fetchApplications();
  }, []);

  // Real-time Background Polling every 6 seconds
  useEffect(() => {
    const interval = setInterval(() => {
      applicationsAPI.getMyApplications()
        .then(res => {
          if (res.data && Array.isArray(res.data)) {
            setApplications(res.data);
            setLastSyncedTime(new Date().toLocaleTimeString('en-IN'));
          }
        })
        .catch(err => console.debug('Background poll error:', err));
    }, 6000);

    return () => clearInterval(interval);
  }, []);

  const handlePartnerAction = async (appId, action) => {
    setActionLoadingId(appId);
    try {
      await applicationsAPI.partnerAction(appId, {
        action,
        remarks: action === 'ACCEPT' 
          ? 'Nodal Officer verified KYC and eligibility. Application accepted for in-principle sanction.' 
          : 'Additional documentation requested for verification.',
      });
      setNotificationMsg({
        type: action === 'ACCEPT' ? 'success' : 'info',
        text: action === 'ACCEPT' 
          ? t('Bank Partner successfully accepted the application! Status updated to PARTNER_ASSIGNED.') 
          : t('Bank Partner returned query on application.'),
      });
      setTimeout(() => setNotificationMsg(null), 5000);
      await fetchApplications();
    } catch (err) {
      console.error('Failed to trigger partner action:', err);
    } finally {
      setActionLoadingId(null);
    }
  };

  const handleCreateDemoApplication = async () => {
    setCreatingDemo(true);
    try {
      const pType = (purposeType || application.purpose_type || 'BUSINESS').toUpperCase();
      let schemeCode = 'PMEGP';
      let schemeName = 'Prime Minister Employment Generation Programme (PMEGP)';
      
      if (pType === 'EDUCATION') {
        schemeCode = 'CSIS';
        schemeName = 'Central Sector Interest Subsidy Scheme (CSIS)';
      } else if (pType === 'SELF_EMPLOYMENT') {
        schemeCode = 'PM-SVANIDHI';
        schemeName = "PM Street Vendor's AtmaNirbhar Nidhi (PM SVANidhi)";
      }

      if (selectedScheme?.scheme_code) {
        schemeCode = selectedScheme.scheme_code;
        schemeName = selectedScheme.scheme_name || selectedScheme.scheme_code;
      }

      const submitRes = await applicationsAPI.submit({
        purpose_type: pType,
        scheme_code: schemeCode,
        scheme_name: schemeName,
        loan_amount: application.loanAmount || loanAmount || 1200000,
        user_data: application,
      });

      const appId = submitRes.data?.application_id;

      if (appId) {
        // Invite a sample lead bank branch
        await applicationsAPI.invitePartner(appId, {
          partner_name: 'State Bank of India',
          partner_type: 'LEAD_BANK',
          branch_code: 'Lead District Commercial Branch',
          ifsc_code: 'SBIN0000421',
          district: application.district || 'Mumbai',
          state: application.state || 'Maharashtra',
          contact_person: 'R. Srinivasan (Lead District Officer)',
          contact_phone: '1800-425-3800',
        });
      }

      setNotificationMsg({
        type: 'success',
        text: `${t('New application created and partner invitation dispatched!')} (${pType})`,
      });
      setTimeout(() => setNotificationMsg(null), 5000);
      await fetchApplications();
    } catch (err) {
      console.error('Error creating demo app:', err);
    } finally {
      setCreatingDemo(false);
    }
  };

  const filteredApplications = applications.filter(app => {
    if (filterPurpose === 'ALL') return true;
    return (app.purpose_type || '').toUpperCase() === filterPurpose;
  });

  const getPurposeBadge = (pt) => {
    const p = (pt || 'BUSINESS').toUpperCase();
    if (p === 'EDUCATION') {
      return <span className="px-2.5 py-1 rounded-full text-xs font-black bg-blue-100 text-blue-900 border border-blue-200">🎓 {t('Education')}</span>;
    }
    if (p === 'SELF_EMPLOYMENT') {
      return <span className="px-2.5 py-1 rounded-full text-xs font-black bg-purple-100 text-purple-900 border border-purple-200">🛒 {t('Self-Employment')}</span>;
    }
    return <span className="px-2.5 py-1 rounded-full text-xs font-black bg-emerald-100 text-emerald-900 border border-emerald-200">🏭 {t('Business')}</span>;
  };

  return (
    <div className="max-w-6xl mx-auto py-8 px-4 sm:px-6 space-y-6 font-sans text-slate-900">
      
      {/* Header Banner */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-gradient-to-r from-slate-900 via-emerald-950 to-slate-900 text-white p-6 sm:p-8 rounded-3xl shadow-xl border border-slate-800">
        <div className="space-y-1.5">
          <div className="flex items-center gap-2">
            <span className="flex h-2.5 w-2.5 relative">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-500"></span>
            </span>
            <span className="px-2.5 py-0.5 rounded-full text-[10px] font-black uppercase tracking-wider bg-emerald-500/20 text-emerald-300 border border-emerald-400/30">
              Live Real-Time Connection
            </span>
            <span className="text-xs text-slate-400 font-mono hidden sm:inline">&bull; Synced at {lastSyncedTime}</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-black text-white">{t('Application & Loan Tracking Hub')}</h1>
          <p className="text-xs text-slate-300 max-w-2xl">
            {t('Real-time milestone transparency for AI document verification, bank branch invitations, credit appraisal, and government margin subsidy release.')}
          </p>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={() => fetchApplications(true)}
            disabled={refreshing}
            className="px-3.5 py-2.5 bg-slate-800 hover:bg-slate-700 text-slate-200 font-bold text-xs rounded-xl border border-slate-700 flex items-center gap-1.5 shadow-sm cursor-pointer transition-all"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${refreshing ? 'animate-spin text-emerald-400' : ''}`} />
            <span>{refreshing ? 'Syncing...' : 'Sync Status'}</span>
          </button>
          
          <button
            onClick={handleCreateDemoApplication}
            disabled={creatingDemo}
            className="px-4 py-2.5 bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-black text-xs rounded-xl shadow-md transition-all flex items-center gap-1.5 cursor-pointer"
          >
            {creatingDemo ? <RefreshCw className="w-3.5 h-3.5 animate-spin" /> : <Sparkles className="w-3.5 h-3.5" />}
            <span>+ {t('Apply for Scheme')}</span>
          </button>
        </div>
      </div>

      {/* Live Notification Banner */}
      {notificationMsg && (
        <div className={`p-4 rounded-2xl border text-xs font-bold flex items-center justify-between animate-in fade-in slide-in-from-top-2 duration-200 ${
          notificationMsg.type === 'success' 
            ? 'bg-emerald-50 border-emerald-300 text-emerald-950' 
            : 'bg-blue-50 border-blue-300 text-blue-950'
        }`}>
          <div className="flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
            <span>{notificationMsg.text}</span>
          </div>
          <button onClick={() => setNotificationMsg(null)} className="text-slate-400 hover:text-slate-600 text-sm">
            &times;
          </button>
        </div>
      )}

      {/* Track Filter Tabs */}
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div className="flex items-center gap-1.5 bg-slate-100 p-1.5 rounded-2xl border border-slate-200">
          {[
            { id: 'ALL', label: t('All Applications') },
            { id: 'BUSINESS', label: `🏭 ${t('Business')}` },
            { id: 'EDUCATION', label: `🎓 ${t('Education')}` },
            { id: 'SELF_EMPLOYMENT', label: `🛒 ${t('Self-Employment')}` },
          ].map(tab => (
            <button
              key={tab.id}
              onClick={() => setFilterPurpose(tab.id)}
              className={`px-3.5 py-1.5 rounded-xl text-xs font-bold transition-all cursor-pointer ${
                filterPurpose === tab.id 
                  ? 'bg-white text-slate-900 shadow-sm border border-slate-200/80' 
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>

        <span className="text-xs text-slate-500 font-semibold">
          {t('Showing')} {filteredApplications.length} {t('of')} {applications.length} {t('applications')}
        </span>
      </div>

      {/* Applications List */}
      {loading && applications.length === 0 ? (
        <div className="bg-white p-12 rounded-3xl border border-slate-200 shadow-sm text-center space-y-3">
          <RefreshCw className="w-8 h-8 text-emerald-600 animate-spin mx-auto" />
          <p className="text-sm font-bold text-slate-700">{t('Loading live application audit trails from database...')}</p>
        </div>
      ) : filteredApplications.length === 0 ? (
        <div className="bg-white p-12 rounded-3xl border border-slate-200 shadow-sm text-center space-y-4">
          <div className="w-16 h-16 bg-slate-100 text-slate-400 rounded-3xl flex items-center justify-center mx-auto">
            <FileText className="w-8 h-8" />
          </div>
          <div>
            <h3 className="font-extrabold text-slate-900 text-lg">{t('No Applications Found in this Category')}</h3>
            <p className="text-xs text-slate-500 max-w-md mx-auto mt-1">
              {t('You have not submitted a scheme application for this track yet. Explore the AI matching questionnaire to submit your application.')}
            </p>
          </div>
          <div className="pt-2 flex flex-wrap justify-center gap-3">
            <button
              onClick={handleCreateDemoApplication}
              className="px-5 py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-black rounded-xl shadow-md transition-all cursor-pointer"
            >
              + {t('Submit Application Now')}
            </button>
            <Link
              to="/find-scheme"
              className="px-4 py-2.5 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-bold rounded-xl"
            >
              {t('Go to Scheme Finder')}
            </Link>
          </div>
        </div>
      ) : (
        <div className="space-y-6">
          {filteredApplications.map((app) => {
            const history = app.status_history || [];

            return (
              <div 
                key={app.id} 
                className="bg-white rounded-3xl border-2 border-slate-200 p-6 sm:p-8 shadow-sm hover:border-emerald-300 transition-all space-y-6"
              >
                {/* Application Header */}
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-slate-100">
                  <div className="space-y-1">
                    <div className="flex flex-wrap items-center gap-2">
                      {getPurposeBadge(app.purpose_type)}
                      <span className="font-mono text-xs font-black bg-slate-900 text-emerald-400 px-2.5 py-0.5 rounded-lg">
                        {app.application_number}
                      </span>
                      <span className="text-xs text-slate-400">&bull; {new Date(app.created_at || Date.now()).toLocaleDateString()}</span>
                    </div>
                    <h2 className="text-xl font-black text-slate-900">{app.scheme_name || app.scheme_code}</h2>
                    <p className="text-xs text-slate-500">
                      Scheme Code: <strong className="font-mono text-slate-800">{app.scheme_code}</strong> &bull; Nodal Bank: <strong className="text-indigo-700">{app.partner_name || 'Awaiting Branch Invitation'}</strong>
                    </p>
                  </div>

                  <div className="flex flex-col sm:items-end gap-1">
                    <span className="text-[10px] uppercase font-bold text-slate-400 tracking-wider">Overall Status</span>
                    <span className="px-3 py-1 bg-emerald-100 text-emerald-900 border border-emerald-300 font-extrabold text-xs rounded-full inline-flex items-center gap-1.5">
                      <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
                      {app.status}
                    </span>
                  </div>
                </div>

                {/* 3 Real-time Status Columns */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  
                  {/* Loan Sanction Box */}
                  <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200 space-y-1.5">
                    <div className="flex items-center justify-between">
                      <span className="text-[10px] uppercase font-bold text-slate-400 tracking-wider">Loan Approval Status</span>
                      <span className={`w-2.5 h-2.5 rounded-full ${
                        app.loan_status === 'APPROVED' || app.loan_status === 'SANCTIONED'
                          ? 'bg-emerald-500 animate-pulse'
                          : app.loan_status === 'UNDER_REVIEW'
                          ? 'bg-amber-500 animate-pulse'
                          : app.loan_status === 'REJECTED'
                          ? 'bg-rose-500'
                          : 'bg-slate-400'
                      }`} />
                    </div>
                    <div>
                      <span className={`font-black text-sm block ${
                        app.loan_status === 'APPROVED' || app.loan_status === 'SANCTIONED'
                          ? 'text-emerald-700'
                          : app.loan_status === 'UNDER_REVIEW'
                          ? 'text-amber-700'
                          : app.loan_status === 'REJECTED'
                          ? 'text-rose-700'
                          : 'text-slate-800'
                      }`}>
                        {app.loan_status}
                      </span>
                      <span className="text-[11px] text-slate-500 block">
                        Principal Loan: <strong>₹{(app.loan_amount || 0).toLocaleString('en-IN')}</strong>
                      </span>
                    </div>
                  </div>

                  {/* Fund Disbursement Box */}
                  <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200 space-y-1.5">
                    <div className="flex items-center justify-between">
                      <span className="text-[10px] uppercase font-bold text-slate-400 tracking-wider">Govt Margin Subsidy</span>
                      <span className={`w-2.5 h-2.5 rounded-full ${
                        app.fund_status === 'RELEASED'
                          ? 'bg-emerald-500'
                          : app.fund_status === 'PROCESSING' || app.fund_status === 'APPROVED'
                          ? 'bg-indigo-500 animate-pulse'
                          : 'bg-slate-400'
                      }`} />
                    </div>
                    <div>
                      <span className={`font-black text-sm block ${
                        app.fund_status === 'RELEASED'
                          ? 'text-emerald-700'
                          : app.fund_status === 'PROCESSING' || app.fund_status === 'APPROVED'
                          ? 'text-indigo-700'
                          : 'text-slate-800'
                      }`}>
                        {app.fund_status}
                      </span>
                      <span className="text-[11px] text-slate-500 block">
                        {app.fund_amount > 0 ? (
                          <strong className="text-emerald-700">₹{app.fund_amount.toLocaleString('en-IN')} Approved Grant</strong>
                        ) : (
                          'Escrow Routing'
                        )}
                      </span>
                    </div>
                  </div>

                  {/* Desk Appointment Box */}
                  <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200 space-y-1.5">
                    <div className="flex items-center justify-between">
                      <span className="text-[10px] uppercase font-bold text-slate-400 tracking-wider">Branch Appointment</span>
                      <Calendar className={`w-3.5 h-3.5 ${app.appointment_status === 'SCHEDULED' ? 'text-indigo-600' : 'text-slate-400'}`} />
                    </div>
                    <div>
                      <span className={`font-black text-sm block ${
                        app.appointment_status === 'SCHEDULED' ? 'text-indigo-700' : 'text-slate-800'
                      }`}>
                        {app.appointment_status}
                      </span>
                      <span className="text-[11px] text-slate-500 block truncate" title={app.appointment_venue || ''}>
                        {app.appointment_date 
                          ? `${new Date(app.appointment_date).toLocaleDateString('en-IN')} (${app.appointment_time || '10:30 AM'})` 
                          : 'No visit required / pending'}
                      </span>
                    </div>
                  </div>

                </div>

                {/* Financial Summary Strip */}
                <div className="p-4 rounded-2xl bg-slate-900 text-white grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs">
                  <div>
                    <span className="text-slate-400 block text-[10px] uppercase font-bold">Loan Quantum</span>
                    <span className="font-mono font-bold text-emerald-400">₹{(app.loan_amount || 0).toLocaleString('en-IN')}</span>
                  </div>
                  <div>
                    <span className="text-slate-400 block text-[10px] uppercase font-bold">Govt Subsidy Grant</span>
                    <span className="font-mono font-bold text-amber-300">₹{(app.fund_amount || app.subsidy_amount || 0).toLocaleString('en-IN')}</span>
                  </div>
                  <div>
                    <span className="text-slate-400 block text-[10px] uppercase font-bold">Fixed Interest Rate</span>
                    <span className="font-bold text-slate-200">{app.interest_rate || 8.5}% p.a.</span>
                  </div>
                  <div>
                    <span className="text-slate-400 block text-[10px] uppercase font-bold">Tenure &amp; Moratorium</span>
                    <span className="font-bold text-slate-200">{app.tenure_months || 60}m ({app.moratorium_months || 6}m grace)</span>
                  </div>
                </div>

                {/* Scheduled Appointment Card Alert */}
                {app.appointment_status === 'SCHEDULED' && (
                  <div className="p-4 rounded-2xl bg-indigo-50 border border-indigo-200 text-indigo-950 space-y-2">
                    <div className="flex items-center gap-2 font-bold text-sm">
                      <Calendar className="w-5 h-5 text-indigo-600 shrink-0" />
                      <span>Scheduled Bank Desk Visit Pass</span>
                    </div>
                    <p className="text-xs text-indigo-800">
                      <strong>Venue:</strong> {app.appointment_venue || 'District Lead Bank Branch Office'}<br />
                      <strong>Date &amp; Time:</strong> {new Date(app.appointment_date).toLocaleDateString('en-IN')} at {app.appointment_time || '10:30 AM'}<br />
                      <strong>Instructions:</strong> {app.appointment_remarks || 'Please bring original Aadhaar, PAN card, caste certificate and DPR.'}
                    </p>
                  </div>
                )}

                {/* 5-Stage Visual Stepper */}
                <div className="grid grid-cols-2 sm:grid-cols-5 gap-3 bg-slate-50 p-4 rounded-2xl border border-slate-200/60 text-xs">
                  <div className="space-y-1">
                    <span className="text-[10px] font-bold uppercase text-slate-400 tracking-wider block">Stage 1</span>
                    <span className="font-black text-emerald-800 flex items-center gap-1">
                      <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" /> AI Profile Match
                    </span>
                    <span className="text-[10px] text-slate-500 block">Gazette Rules Met</span>
                  </div>

                  <div className="space-y-1">
                    <span className="text-[10px] font-bold uppercase text-slate-400 tracking-wider block">Stage 2</span>
                    <span className="font-black text-emerald-800 flex items-center gap-1">
                      <ShieldCheck className="w-3.5 h-3.5 text-emerald-600" /> OCR Verified
                    </span>
                    <span className="text-[10px] text-slate-500 block">Mandatory Docs</span>
                  </div>

                  <div className="space-y-1">
                    <span className="text-[10px] font-bold uppercase text-slate-400 tracking-wider block">Stage 3</span>
                    <span className={`font-black flex items-center gap-1 ${
                      app.partner_name ? 'text-emerald-800' : 'text-indigo-800'
                    }`}>
                      {app.partner_name ? <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" /> : <Send className="w-3.5 h-3.5 text-indigo-600" />}
                      Partner Desk
                    </span>
                    <span className="text-[10px] text-slate-500 block truncate">{app.partner_name || 'Pending Invite'}</span>
                  </div>

                  <div className="space-y-1">
                    <span className="text-[10px] font-bold uppercase text-slate-400 tracking-wider block">Stage 4</span>
                    <span className={`font-black flex items-center gap-1 ${
                      app.loan_status === 'APPROVED' || app.loan_status === 'SANCTIONED' ? 'text-emerald-800' : 'text-slate-600'
                    }`}>
                      {app.loan_status === 'APPROVED' || app.loan_status === 'SANCTIONED' ? (
                        <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
                      ) : (
                        <Clock className="w-3.5 h-3.5 text-slate-400" />
                      )}
                      Loan Sanction
                    </span>
                    <span className="text-[10px] text-slate-500 block">{app.loan_status}</span>
                  </div>

                  <div className="space-y-1 col-span-2 sm:col-span-1">
                    <span className="text-[10px] font-bold uppercase text-slate-400 tracking-wider block">Stage 5</span>
                    <span className={`font-black flex items-center gap-1 ${
                      app.fund_status === 'RELEASED' ? 'text-emerald-800' : 'text-slate-600'
                    }`}>
                      {app.fund_status === 'RELEASED' ? (
                        <Award className="w-3.5 h-3.5 text-emerald-600" />
                      ) : (
                        <Clock className="w-3.5 h-3.5 text-slate-400" />
                      )}
                      Margin Subsidy
                    </span>
                    <span className="text-[10px] text-slate-500 block">{app.fund_status}</span>
                  </div>
                </div>

                {/* Partner Accept Simulation (If not accepted yet) */}
                {app.status !== 'PARTNER_ASSIGNED' && app.status !== 'SANCTIONED' && app.status !== 'COMPLETED' && (
                  <div className="bg-emerald-50 border border-emerald-200 rounded-2xl p-4 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                    <div className="space-y-0.5">
                      <span className="text-xs font-black text-emerald-950 block">
                        🏛️ Partner Desk Acceptance Simulation
                      </span>
                      <p className="text-[11px] text-emerald-800">
                        Test the real-time workflow by simulating branch acceptance.
                      </p>
                    </div>

                    <button
                      onClick={() => handlePartnerAction(app.id, 'ACCEPT')}
                      disabled={actionLoadingId === app.id}
                      className="px-3.5 py-2 bg-emerald-600 hover:bg-emerald-700 text-white font-black text-xs rounded-xl shadow-sm transition-all flex items-center gap-1.5 cursor-pointer shrink-0"
                    >
                      {actionLoadingId === app.id ? <RefreshCw className="w-3.5 h-3.5 animate-spin" /> : <Check className="w-3.5 h-3.5" />}
                      <span>Bank Accept Application</span>
                    </button>
                  </div>
                )}

                {/* Full Real-Time Audit History Trail */}
                {history.length > 0 && (
                  <div className="pt-2 border-t border-slate-100 space-y-3">
                    <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider block">
                      Official Status Transition Audit Trail ({history.length} events logged in database)
                    </span>
                    <div className="space-y-2">
                      {history.slice().reverse().map((item, hIdx) => (
                        <div key={hIdx} className="flex items-start gap-3 text-xs bg-slate-50 p-3 rounded-xl border border-slate-100">
                          <div className="w-2.5 h-2.5 rounded-full bg-emerald-500 mt-1 shrink-0" />
                          <div className="flex-1 space-y-0.5">
                            <div className="flex items-center justify-between">
                              <span className="font-black text-slate-900">{item.title || item.status}</span>
                              <span className="text-[10px] text-slate-400 font-mono">
                                {item.timestamp ? new Date(item.timestamp).toLocaleString('en-IN') : ''}
                              </span>
                            </div>
                            <p className="text-slate-600 text-[11px]">{item.description || item.detail}</p>
                            <span className="text-[10px] font-bold text-indigo-700 block">
                              Updated By: {item.updated_by} ({item.actor_role || 'ADMIN'})
                            </span>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
