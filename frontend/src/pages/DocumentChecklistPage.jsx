import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { 
  FileCheck, CheckCircle2, AlertCircle, ArrowRight, Printer, 
  Download, Clock, ShieldCheck, GraduationCap, Building2, Store
} from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import { useApplication } from '../context/ApplicationContext';
import { documentsAPI } from '../services/api';

export default function DocumentChecklistPage() {
  const { t } = useLanguage();
  const { application, purposeType, verifiedDocKeys, setAllDocumentsVerified } = useApplication();
  const [userVerifiedDocs, setUserVerifiedDocs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [verifying, setVerifying] = useState(false);

  const effPurpose = (purposeType || application.purpose_type || 'EDUCATION').toUpperCase();

  const loadUserDocs = async () => {
    try {
      const res = await documentsAPI.getUserDocuments();
      const docs = res.data || [];
      const verifiedTypes = docs
        .filter(d => strStatus(d.verification_status))
        .map(d => (d.document_type || '').toLowerCase());
      
      // Merge with session verifiedDocKeys
      const sessionKeys = (verifiedDocKeys || []).map(k => String(k).toLowerCase());
      setUserVerifiedDocs([...new Set([...verifiedTypes, ...sessionKeys])]);
    } catch (err) {
      console.warn('Could not fetch user documents:', err);
      const sessionKeys = (verifiedDocKeys || []).map(k => String(k).toLowerCase());
      setUserVerifiedDocs(sessionKeys);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadUserDocs();
  }, [verifiedDocKeys]);

  const handleAutoVerifyChecklist = async () => {
    try {
      setVerifying(true);
      await documentsAPI.verifyAllMandatory({ purpose_type: effPurpose });
      if (setAllDocumentsVerified) {
        setAllDocumentsVerified(true);
      }
      await loadUserDocs();
    } catch (err) {
      console.error('Failed to auto-verify documents:', err);
    } finally {
      setVerifying(false);
    }
  };

  const strStatus = (st) => {
    const s = String(st || '').toUpperCase();
    return s === 'VERIFIED' || s === 'SUCCESS';
  };

  // Purpose-specific dynamic document requirement list
  const getDocumentRequirements = () => {
    if (effPurpose === 'EDUCATION') {
      return [
        { 
          key: 'aadhaar', 
          name: t('docAadhaar', 'Aadhaar Card'), 
          mandatory: true, 
          desc: t('Identity & Address proof with UIDAI Verhoeff checksum validation', 'Identity & Address proof with UIDAI Verhoeff checksum validation'),
          authority: 'UIDAI'
        },
        { 
          key: 'pan', 
          name: t('docPan', 'PAN Card'), 
          mandatory: true, 
          desc: t('Permanent Account Number for banking and financial KYC compliance', 'Permanent Account Number for banking and financial KYC compliance'),
          authority: 'Income Tax Department (ITD)'
        },
        { 
          key: '10th', 
          name: t('doc10th', '10th Standard Marksheet / Certificate'), 
          mandatory: true, 
          desc: t('Age proof & foundational academic merit verification', 'Age proof & foundational academic merit verification'),
          authority: 'State Board / CBSE / ICSE'
        },
        { 
          key: '12th', 
          name: t('doc12th', '12th Standard Marksheet / Diploma'), 
          mandatory: true, 
          desc: t('Higher secondary qualification for college admission', 'Higher secondary qualification for college admission'),
          authority: 'HSC Board / State Technical Board'
        },
        { 
          key: 'income', 
          name: t('docIncome', 'Annual Family Income Certificate'), 
          mandatory: true, 
          desc: t('Required for CSIS 100% full interest subsidy (Income <= Rs. 4.5 Lakh)', 'Required for CSIS 100% full interest subsidy (Income <= Rs. 4.5 Lakh)'),
          authority: 'Tahsildar / Revenue Authority'
        },
        { 
          key: 'caste', 
          name: t('docCaste', 'Community / Caste Certificate'), 
          mandatory: true, 
          desc: t('Mandatory for NSFDC / NBCFDC / NMDFC concessional rates', 'Mandatory for NSFDC / NBCFDC / NMDFC concessional rates'),
          authority: 'e-District / Revenue Dept'
        }
      ];
    } else if (effPurpose === 'SELF_EMPLOYMENT') {
      return [
        { 
          key: 'aadhaar', 
          name: t('docAadhaar', 'Aadhaar Card'), 
          mandatory: true, 
          desc: t('Identity & Address proof with mobile OTP linkage', 'Identity & Address proof with mobile OTP linkage'),
          authority: 'UIDAI'
        },
        { 
          key: 'business_proof', 
          name: t('Vending Certificate / Letter of Recommendation (LoR)', 'Vending Certificate / Letter of Recommendation (LoR)'), 
          mandatory: true, 
          desc: t('Urban Local Body (ULB) vending survey identity card or PM Vishwakarma verification', 'Urban Local Body (ULB) vending survey identity card or PM Vishwakarma verification'),
          authority: 'Municipal Corporation / ULB'
        },
        { 
          key: 'bank', 
          name: t('docBank', 'Bank Passbook / Statement'), 
          mandatory: true, 
          desc: t('Account for micro-credit disbursement and digital UPI cashback', 'Account for micro-credit disbursement and digital UPI cashback'),
          authority: 'Bank Branch'
        },
        { 
          key: 'income', 
          name: t('docIncome', 'Income Certificate / Ration Card'), 
          mandatory: false, 
          desc: t('BPL verification for priority subventions', 'BPL verification for priority subventions'),
          authority: 'Civil Supplies Dept'
        }
      ];
    } else {
      return [
        { 
          key: 'docAadhaar', 
          name: t('docAadhaar', 'Aadhaar Card'), 
          mandatory: true, 
          desc: t('Identity & Address proof with mobile OTP linkage and UIDAI Verhoeff checksum validation', 'Identity & Address proof with mobile OTP linkage and UIDAI Verhoeff checksum validation'),
          authority: 'UIDAI'
        },
        { 
          key: 'docPan', 
          name: t('docPan', 'PAN Card'), 
          mandatory: true, 
          desc: t('Permanent Account Number required for commercial bank loan sanction and financial KYC compliance', 'Permanent Account Number required for commercial bank loan sanction and financial KYC compliance'),
          authority: 'Income Tax Department (ITD)'
        },
        { 
          key: 'docDpr', 
          name: t('docDpr', 'Detailed Project Report (DPR)'), 
          mandatory: true, 
          desc: t('Project cost breakdown, machinery quotation, and 3-year financial viability model', 'Project cost breakdown, machinery quotation, and 3-year financial viability model'),
          authority: 'Chartered Engineer / DIC'
        },
        { 
          key: 'docIncome', 
          name: t('docIncome', 'Annual Family Income Certificate'), 
          mandatory: true, 
          desc: t('Official revenue proof to verify family income compliance with statutory subsidy caps', 'Official revenue proof to verify family income compliance with statutory subsidy caps'),
          authority: 'Tahsildar / Revenue Authority'
        },
        { 
          key: 'docCaste', 
          name: t('docCaste', 'Caste / Category Certificate'), 
          mandatory: true, 
          desc: t('Required for 25%-35% Special Category Subsidy under PMEGP & Stand-Up India', 'Required for 25%-35% Special Category Subsidy under PMEGP & Stand-Up India'),
          authority: 'State e-District Portal'
        },
        { 
          key: 'docUdyam', 
          name: t('docUdyam', 'Udyam MSME Registration Certificate'), 
          mandatory: true, 
          desc: t('Official Government of India MSME recognition and priority sector status', 'Official Government of India MSME recognition and priority sector status'),
          authority: 'Ministry of MSME'
        }
      ];
    }
  };

  const requirements = getDocumentRequirements();
  
  // Calculate real verified vs pending count
  const isDocVerified = (docKey) => {
    const k = docKey.toLowerCase().replace(/^doc/, '');
    return userVerifiedDocs.some(vk => {
      const v = String(vk).toLowerCase().replace(/^doc/, '');
      return v.includes(k) || k.includes(v);
    });
  };

  const verifiedCount = requirements.filter(r => isDocVerified(r.key)).length;
  const pendingCount = requirements.length - verifiedCount;
  const mandatoryRemaining = requirements.filter(r => r.mandatory && !isDocVerified(r.key)).length;

  return (
    <div className="max-w-4xl mx-auto py-8 px-4 sm:px-6 space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-100 text-emerald-800 text-xs font-bold mb-2">
            {effPurpose === 'EDUCATION' ? <GraduationCap className="w-3.5 h-3.5" /> : effPurpose === 'SELF_EMPLOYMENT' ? <Store className="w-3.5 h-3.5" /> : <Building2 className="w-3.5 h-3.5" />}
            <span>{t('Track:')} {t(effPurpose === 'EDUCATION' ? 'Education & Student Loans' : effPurpose === 'SELF_EMPLOYMENT' ? 'Self-Employment & Artisans' : 'Business & Enterprise Setup')}</span>
          </div>
          <h1 className="text-2xl font-black text-slate-900">{t('docChecklistTitle', 'Mandatory Document Verification Checklist')}</h1>
          <p className="text-xs text-slate-500 mt-1">
            {effPurpose === 'EDUCATION'
              ? t('Official academic documents, fee schedules, and income certificates required for CSIS & education loan sanction.')
              : t('Statutory documents required by lending banks under official gazette guidelines.')}
          </p>
        </div>

        <div className="flex gap-2">
          <button
            onClick={handleAutoVerifyChecklist}
            disabled={verifying}
            className="px-4 py-2 bg-emerald-600 hover:bg-emerald-700 disabled:opacity-50 text-white font-semibold text-xs rounded-xl flex items-center gap-1.5 cursor-pointer shadow-sm transition-all"
          >
            <ShieldCheck className="w-3.5 h-3.5" />
            <span>{verifying ? t('Verifying...') : t('1-Click Verify All')}</span>
          </button>
          <button
            onClick={() => window.print()}
            className="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 font-semibold text-xs rounded-xl flex items-center gap-1.5 cursor-pointer"
          >
            <Printer className="w-3.5 h-3.5" />
            <span>{t('Print Checklist', 'Print Checklist')}</span>
          </button>
        </div>
      </div>

      {/* Verification Status Summary Card */}
      <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="p-4 bg-emerald-50 rounded-xl border border-emerald-200">
          <span className="text-[11px] font-bold text-emerald-800 uppercase tracking-wider block">{t('Verified Documents')}</span>
          <span className="text-2xl font-black text-emerald-700 mt-1 block">{verifiedCount} / {requirements.length}</span>
          <p className="text-[10px] text-emerald-600 mt-0.5">{verifiedCount === 0 ? t('No documents verified yet') : t('Documents validated by OCR')}</p>
        </div>
        <div className="p-4 bg-amber-50 rounded-xl border border-amber-200">
          <span className="text-[11px] font-bold text-amber-800 uppercase tracking-wider block">{t('Mandatory Pending')}</span>
          <span className="text-2xl font-black text-amber-700 mt-1 block">{mandatoryRemaining}</span>
          <p className="text-[10px] text-amber-600 mt-0.5">{mandatoryRemaining === 0 ? t('All mandatory documents complete!') : t('Required before bank submission')}</p>
        </div>
        <div className="p-4 bg-blue-50 rounded-xl border border-blue-200 flex flex-col justify-between">
          <div>
            <span className="text-[11px] font-bold text-blue-800 uppercase tracking-wider block">{t('Verification Action')}</span>
            <p className="text-xs font-semibold text-blue-950 mt-1">{t('Upload documents or test 1-click synthetic samples')}</p>
          </div>
          <Link
            to="/documents"
            className="mt-2 inline-flex items-center justify-center gap-1.5 px-3 py-1.5 bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs rounded-lg shadow-sm transition-all"
          >
            <span>{t('Go to Document Assistant (OCR)')}</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </div>
      </div>

      {/* Dynamic Checklist Items */}
      <div className="bg-white rounded-2xl border border-slate-200 overflow-hidden shadow-sm">
        <div className="divide-y divide-slate-100">
          {requirements.map((doc, idx) => {
            const verified = isDocVerified(doc.key);
            return (
              <div key={idx} className="p-5 flex flex-col sm:flex-row sm:items-center justify-between gap-3 hover:bg-slate-50/50">
                <div className="space-y-1 flex-1">
                  <div className="flex items-center gap-2">
                    <span className="font-bold text-slate-900 text-sm">{doc.name}</span>
                    {doc.mandatory ? (
                      <span className="text-[10px] font-bold text-red-700 bg-red-50 border border-red-200 px-2 py-0.5 rounded">
                        {t('mandatoryTag', 'Mandatory')}
                      </span>
                    ) : (
                      <span className="text-[10px] font-bold text-slate-600 bg-slate-100 px-2 py-0.5 rounded">
                        {t('optional', 'Optional')}
                      </span>
                    )}
                    <span className="text-[10px] text-slate-400 font-mono">({doc.authority})</span>
                  </div>
                  <p className="text-xs text-slate-500 leading-relaxed">{doc.desc}</p>
                </div>

                <div className="flex items-center gap-3 shrink-0">
                  <span className={`px-3 py-1 rounded-full text-xs font-bold flex items-center gap-1.5 ${
                    verified ? 'bg-emerald-100 text-emerald-800' : 'bg-amber-100 text-amber-800'
                  }`}>
                    {verified ? <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" /> : <Clock className="w-3.5 h-3.5 text-amber-600" />}
                    <span>{verified ? t('verified', 'Verified') : t('pending', 'Pending')}</span>
                  </span>
                  
                  <Link
                    to="/documents"
                    className="px-3 py-1.5 bg-slate-100 hover:bg-emerald-50 hover:text-emerald-700 text-slate-700 text-xs font-bold rounded-lg transition-colors"
                  >
                    {verified ? t('View Hash') : t('Upload / Verify')}
                  </Link>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
