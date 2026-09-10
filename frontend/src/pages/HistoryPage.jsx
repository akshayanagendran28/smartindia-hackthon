import React, { useState, useEffect } from 'react';
import { 
  History, Award, CheckCircle2, ArrowRight, ShieldCheck, Clock, 
  Building2, Landmark, RefreshCw, AlertCircle, FileText, Check, 
  ExternalLink, UserCheck, Sparkles, Send, Eye, XCircle
} from 'lucide-react';
import { Link, useNavigate } from 'react-router-dom';
import { useApplication } from '../context/ApplicationContext';
import { useLanguage } from '../context/LanguageContext';
import { applicationsAPI } from '../services/api';

export default function HistoryPage() {
  const { t } = useLanguage();
  const navigate = useNavigate();
  const { application, purposeType, selectedScheme, loanAmount } = useApplication();

  const [applications, setApplications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filterPurpose, setFilterPurpose] = useState('ALL');
  const [actionLoadingId, setActionLoadingId] = useState(null);
  const [notificationMsg, setNotificationMsg] = useState(null);
  const [creatingDemo, setCreatingDemo] = useState(false);

  const fetchApplications = async () => {
    setLoading(true);
    try {
      const res = await applicationsAPI.getMyApplications();
      if (res.data && Array.isArray(res.data)) {
        setApplications(res.data);
      }
    } catch (err) {
      console.warn('Could not fetch applications from API, using fallback data:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchApplications();
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
      // Optimistic local update for demo resilience
      setApplications(prev => prev.map(app => {
        if (app.id === appId) {
          const updatedHistory = [...(app.status_history || [])];
          if (action === 'ACCEPT') {
            updatedHistory.push({
              step: 'PARTNER_ASSIGNED',
              title: 'Partner Accepted Application',
              detail: 'Bank Branch accepted application. Assigned Nodal Officer for sanction processing.',
              timestamp: new Date().toISOString(),
            });
            return {
              ...app,
              status: 'PARTNER_ASSIGNED',
              invitation_status: 'ACCEPTED',
              status_history: updatedHistory,
            };
          }
        }
        return app;
      }));
      setNotificationMsg({
        type: 'success',
        text: t('Partner Action simulated! Status updated to PARTNER_ASSIGNED.'),
      });
      setTimeout(() => setNotificationMsg(null), 5000);
    } finally {
      setActionLoadingId(null);
    }
  };

  const handleCreateDemoApplication = async () => {
    setCreatingDemo(true);
    try {
      const pType = (purposeType || application.purpose_type || 'EDUCATION').toUpperCase();
      let schemeCode = 'CSIS';
      let schemeName = 'Central Sector Interest Subsidy Scheme (CSIS)';
      
      if (pType === 'BUSINESS') {
        schemeCode = 'PMEGP';
        schemeName = 'Prime Minister Employment Generation Programme (PMEGP)';
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
        loan_amount: application.loanAmount || loanAmount || 450000,
        user_data: application,
      });

      const appId = submitRes.data?.application_id;

      if (appId) {
        // Invite a sample lead bank branch
        await applicationsAPI.invitePartner(appId, {
          partner_name: 'State Bank of India',
          partner_type: 'LEAD_BANK',
          branch_code: 'Main Commercial Branch',
          ifsc_code: 'SBIN0000421',
          district: application.district || 'Thiruvallur',
          state: application.state || 'Tamil Nadu',
          contact_person: 'R. Srinivasan (Lead District Manager)',
          contact_phone: '1800-425-3800',
        });
      }

      setNotificationMsg({
        type: 'success',
        text: `${t('New application created and partner invitation sent!')} (${pType})`,
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
    const p = (pt || 'EDUCATION').toUpperCase();
    if (p === 'EDUCATION') {
      return <span className="px-2.5 py-1 rounded-full text-xs font-black bg-blue-100 text-blue-900 border border-blue-200">🎓 {t('Education')}</span>;
    }
    if (p === 'SELF_EMPLOYMENT') {
      return <span className="px-2.5 py-1 rounded-full text-xs font-black bg-purple-100 text-purple-900 border border-purple-200">🛒 {t('Self-Employment')}</span>;
    }
    return <span className="px-2.5 py-1 rounded-full text-xs font-black bg-emerald-100 text-emerald-900 border border-emerald-200">🏭 {t('Business')}</span>;
  };

  const getStatusBadge = (status) => {
    switch (status) {
      case 'PARTNER_ASSIGNED':
        return <span className="px-3 py-1 bg-emerald-100 text-emerald-900 border border-emerald-300 font-extrabold text-xs rounded-full flex items-center gap-1.5"><CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" /> {t('Partner Assigned')}</span>;
      case 'INVITATION_SENT':
        return <span className="px-3 py-1 bg-indigo-100 text-indigo-900 border border-indigo-300 font-extrabold text-xs rounded-full flex items-center gap-1.5"><Send className="w-3.5 h-3.5 text-indigo-600" /> {t('Invitation Dispatched')}</span>;
      case 'DOCUMENTS_VERIFIED':
        return <span className="px-3 py-1 bg-teal-100 text-teal-900 border border-teal-300 font-extrabold text-xs rounded-full flex items-center gap-1.5"><ShieldCheck className="w-3.5 h-3.5 text-teal-600" /> {t('Docs Verified')}</span>;
      case 'SANCTIONED':
        return <span className="px-3 py-1 bg-green-100 text-green-900 border border-green-300 font-extrabold text-xs rounded-full flex items-center gap-1.5"><Award className="w-3.5 h-3.5 text-green-600" /> {t('Sanctioned')}</span>;
      default:
        return <span className="px-3 py-1 bg-amber-100 text-amber-900 border border-amber-300 font-extrabold text-xs rounded-full flex items-center gap-1.5"><Clock className="w-3.5 h-3.5 text-amber-600" /> {t('Profile Submitted')}</span>;
    }
  };

  return (
    <div className="max-w-6xl mx-auto py-8 px-4 sm:px-6 space-y-6">
      
      {/* Header Banner */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-gradient-to-r from-slate-900 via-emerald-950 to-slate-900 text-white p-6 rounded-3xl shadow-lg border border-emerald-800/40">
        <div className="space-y-1.5">
          <div className="flex items-center gap-2">
            <span className="px-2.5 py-0.5 rounded-full text-[10px] font-black uppercase tracking-wider bg-emerald-500/20 text-emerald-300 border border-emerald-400/30">
              {t('SIH26092 Transparency Engine')}
            </span>
            <span className="text-xs text-slate-400">&bull; {t('Live Audit Trail')}</span>
          </div>
          <h1 className="text-2xl font-black text-white">{t('Application & Partner Tracking Hub')}</h1>
          <p className="text-xs text-slate-300 max-w-2xl">
            {t('Real-time milestone transparency for AI document verification, bank branch invitations, partner assignment, and loan sanction processing.')}
          </p>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={fetchApplications}
            disabled={loading}
            className="px-3.5 py-2.5 bg-slate-800 hover:bg-slate-700 text-slate-200 font-bold text-xs rounded-xl border border-slate-700 flex items-center gap-1.5 shadow-sm"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
            <span>{t('Refresh')}</span>
          </button>
          
          <button
            onClick={handleCreateDemoApplication}
            disabled={creatingDemo}
            className="px-4 py-2.5 bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-black text-xs rounded-xl shadow-md transition-all flex items-center gap-1.5"
          >
            {creatingDemo ? <RefreshCw className="w-3.5 h-3.5 animate-spin" /> : <Sparkles className="w-3.5 h-3.5" />}
            <span>+ {t('Apply Now (Active Track)')}</span>
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
            { id: 'EDUCATION', label: `🎓 ${t('Education')}` },
            { id: 'BUSINESS', label: `🏭 ${t('Business')}` },
            { id: 'SELF_EMPLOYMENT', label: `🛒 ${t('Self-Employment')}` },
          ].map(tab => (
            <button
              key={tab.id}
              onClick={() => setFilterPurpose(tab.id)}
              className={`px-3.5 py-1.5 rounded-xl text-xs font-bold transition-all ${
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
          <p className="text-sm font-bold text-slate-700">{t('Loading live application audit trails...')}</p>
        </div>
      ) : filteredApplications.length === 0 ? (
        <div className="bg-white p-12 rounded-3xl border border-slate-200 shadow-sm text-center space-y-4">
          <div className="w-16 h-16 bg-slate-100 text-slate-400 rounded-3xl flex items-center justify-center mx-auto">
            <FileText className="w-8 h-8" />
          </div>
          <div>
            <h3 className="font-extrabold text-slate-900 text-lg">{t('No Applications Found in this Category')}</h3>
            <p className="text-xs text-slate-500 max-w-md mx-auto mt-1">
              {t('You have not submitted a scheme application for this track yet. Complete document verification and invite your local bank branch to start tracking.')}
            </p>
          </div>
          <div className="pt-2 flex flex-wrap justify-center gap-3">
            <button
              onClick={handleCreateDemoApplication}
              className="px-5 py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-black rounded-xl shadow-md transition-all"
            >
              + {t('Create Sample Application Now')}
            </button>
            <Link
              to="/find-scheme"
              className="px-4 py-2.5 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-bold rounded-xl"
            >
              {t('Go to Dynamic Questionnaire')}
            </Link>
          </div>
        </div>
      ) : (
        <div className="space-y-6">
          {filteredApplications.map((app) => {
            const invitations = app.partner_invitations || [];
            const primaryInvite = invitations[0] || null;
            const history = app.status_history || [];

            return (
              <div 
                key={app.id} 
                className="bg-white rounded-3xl border border-slate-200 p-6 shadow-sm hover:border-emerald-300 transition-all space-y-6"
              >
                {/* Application Header */}
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-slate-100">
                  <div className="space-y-1">
                    <div className="flex flex-wrap items-center gap-2">
                      {getPurposeBadge(app.purpose_type)}
                      <span className="text-xs font-mono font-bold text-slate-400">ID: {app.id?.substring(0, 8)}...</span>
                      <span className="text-xs text-slate-400">&bull; {new Date(app.created_at || Date.now()).toLocaleDateString()}</span>
                    </div>
                    <h2 className="text-lg font-black text-slate-900">{t(app.scheme_name || app.scheme_code)}</h2>
                    <p className="text-xs text-slate-500">
                      {t('Requested Loan Quantum')}: <strong className="text-emerald-700 font-black">₹{Number(app.loan_amount || 0).toLocaleString('en-IN')}</strong>
                    </p>
                  </div>

                  <div className="flex items-center gap-3">
                    {getStatusBadge(app.status)}
                  </div>
                </div>

                {/* Transparency 4-Stage Visual Stepper */}
                <div className="grid grid-cols-2 md:grid-cols-4 gap-3 bg-slate-50 p-4 rounded-2xl border border-slate-200/60">
                  <div className="space-y-1">
                    <span className="text-[10px] font-bold uppercase text-slate-400 tracking-wider block">{t('Stage 1')}</span>
                    <span className="text-xs font-black text-emerald-800 flex items-center gap-1">
                      <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" /> {t('Profile & AI Match')}
                    </span>
                    <span className="text-[10px] text-slate-500 block">{t('Rules 100% Passed')}</span>
                  </div>

                  <div className="space-y-1">
                    <span className="text-[10px] font-bold uppercase text-slate-400 tracking-wider block">{t('Stage 2')}</span>
                    <span className="text-xs font-black text-emerald-800 flex items-center gap-1">
                      <ShieldCheck className="w-3.5 h-3.5 text-emerald-600" /> {t('OCR Verification')}
                    </span>
                    <span className="text-[10px] text-slate-500 block">{t('Mandatory Docs Clear')}</span>
                  </div>

                  <div className="space-y-1">
                    <span className="text-[10px] font-bold uppercase text-slate-400 tracking-wider block">{t('Stage 3')}</span>
                    <span className={`text-xs font-black flex items-center gap-1 ${
                      app.invitation_status === 'ACCEPTED' || app.status === 'PARTNER_ASSIGNED'
                        ? 'text-emerald-800'
                        : 'text-indigo-800'
                    }`}>
                      {app.invitation_status === 'ACCEPTED' ? <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" /> : <Send className="w-3.5 h-3.5 text-indigo-600" />}
                      {primaryInvite ? primaryInvite.partner_name : t('Branch Invitation')}
                    </span>
                    <span className="text-[10px] text-slate-500 block">
                      {primaryInvite?.ifsc_code ? `IFSC: ${primaryInvite.ifsc_code}` : t('Dispatched to Nodal Branch')}
                    </span>
                  </div>

                  <div className="space-y-1">
                    <span className="text-[10px] font-bold uppercase text-slate-400 tracking-wider block">{t('Stage 4')}</span>
                    <span className={`text-xs font-black flex items-center gap-1 ${
                      app.status === 'SANCTIONED' ? 'text-green-800' : 'text-slate-600'
                    }`}>
                      {app.status === 'SANCTIONED' ? <Award className="w-3.5 h-3.5 text-green-600" /> : <Clock className="w-3.5 h-3.5 text-slate-400" />}
                      {app.status === 'SANCTIONED' ? t('Loan Sanctioned') : t('Sanction Processing')}
                    </span>
                    <span className="text-[10px] text-slate-500 block">
                      {app.status === 'PARTNER_ASSIGNED' ? t('Nodal Officer Assigned') : t('Awaiting Formal Approval')}
                    </span>
                  </div>
                </div>

                {/* Interactive Simulated Partner Reviewer Controls */}
                {app.status !== 'PARTNER_ASSIGNED' && app.status !== 'SANCTIONED' && (
                  <div className="bg-emerald-50/70 border border-emerald-200/80 rounded-2xl p-4 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                    <div className="space-y-0.5">
                      <span className="text-xs font-black text-emerald-950 block">
                        🏛️ {t('Simulate Partner Bank Reviewer Action')}
                      </span>
                      <p className="text-[11px] text-emerald-800">
                        {t('Test the end-to-end transparency lifecycle by triggering bank acceptance or clarification.')}
                      </p>
                    </div>

                    <div className="flex items-center gap-2 shrink-0">
                      <button
                        onClick={() => handlePartnerAction(app.id, 'ACCEPT')}
                        disabled={actionLoadingId === app.id}
                        className="px-3 py-1.5 bg-emerald-600 hover:bg-emerald-700 text-white font-black text-xs rounded-xl shadow-sm transition-all flex items-center gap-1"
                      >
                        {actionLoadingId === app.id ? <RefreshCw className="w-3 h-3 animate-spin" /> : <Check className="w-3 h-3" />}
                        <span>{t('Bank Accept Application')}</span>
                      </button>
                    </div>
                  </div>
                )}

                {/* Expandable History Timeline Log */}
                {history.length > 0 && (
                  <div className="pt-2 border-t border-slate-100 space-y-2">
                    <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider block">
                      {t('Step Audit Log & Transparency Trail')} ({history.length} {t('Events')})
                    </span>
                    <div className="space-y-2">
                      {history.slice(-3).map((item, hIdx) => (
                        <div key={hIdx} className="flex items-start gap-3 text-xs bg-slate-50/80 p-2.5 rounded-xl border border-slate-100">
                          <div className="w-2 h-2 rounded-full bg-emerald-500 mt-1.5 shrink-0" />
                          <div className="flex-1">
                            <span className="font-bold text-slate-800 block">{t(item.title || item.step)}</span>
                            <span className="text-slate-600 text-[11px]">{t(item.detail)}</span>
                          </div>
                          <span className="text-[10px] text-slate-400 shrink-0 font-mono">
                            {new Date(item.timestamp || Date.now()).toLocaleTimeString()}
                          </span>
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
