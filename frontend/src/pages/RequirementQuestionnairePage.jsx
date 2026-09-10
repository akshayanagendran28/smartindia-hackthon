import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Sparkles, Sliders, CheckCircle, ArrowRight } from 'lucide-react';
import api from '../services/api';

export default function RequirementQuestionnairePage() {
  const navigate = useNavigate();
  const [form, setForm] = useState({
    social_category: 'SC',
    gender: 'female',
    age: 28,
    state: 'Maharashtra',
    area_type: 'rural',
    business_type: 'manufacturing',
    business_stage: 'new',
    required_loan: 1000000,
    has_skill_training: true,
    has_udyam_registration: true
  });
  const [loading, setLoading] = useState(false);

  const handleEvaluate = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await api.post('/matching/evaluate', form);
      navigate('/results', { state: { evaluationResult: res.data, profileData: form } });
    } catch (err) {
      console.error(err);
      navigate('/results', { state: { profileData: form } });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto py-8 px-4">
      <div className="bg-white p-8 rounded-2xl border border-slate-200 shadow-sm space-y-6">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-100 text-emerald-800 text-xs font-bold mb-2">
            <Sliders className="w-3.5 h-3.5" />
            <span>Fast Analyzer</span>
          </div>
          <h1 className="text-2xl font-extrabold text-slate-900">Rapid Requirement Questionnaire</h1>
          <p className="text-xs text-slate-500 mt-1">Directly adjust financial parameters to see scheme eligibility recalculate instantly.</p>
        </div>

        <form onSubmit={handleEvaluate} className="space-y-4">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Target Category</label>
              <select
                value={form.social_category}
                onChange={(e) => setForm({ ...form, social_category: e.target.value })}
                className="w-full px-3 py-2 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500"
              >
                <option value="SC">Scheduled Caste (SC)</option>
                <option value="ST">Scheduled Tribe (ST)</option>
                <option value="Minority">Minority Community</option>
                <option value="Women/Special">Women / Special Category</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Gender</label>
              <select
                value={form.gender}
                onChange={(e) => setForm({ ...form, gender: e.target.value })}
                className="w-full px-3 py-2 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500"
              >
                <option value="female">Woman</option>
                <option value="male">Male</option>
                <option value="transgender">Transgender</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Business Nature</label>
              <select
                value={form.business_type}
                onChange={(e) => setForm({ ...form, business_type: e.target.value })}
                className="w-full px-3 py-2 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500"
              >
                <option value="manufacturing">Manufacturing</option>
                <option value="service">Service</option>
                <option value="trading">Trading</option>
                <option value="street_vendor">Street Vending</option>
                <option value="artisan">Artisan</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Location Setting</label>
              <select
                value={form.area_type}
                onChange={(e) => setForm({ ...form, area_type: e.target.value })}
                className="w-full px-3 py-2 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500"
              >
                <option value="rural">Rural (Higher Subsidy)</option>
                <option value="urban">Urban</option>
              </select>
            </div>
          </div>

          <div>
            <div className="flex justify-between text-xs font-semibold text-slate-700 mb-1">
              <span>Required Loan Amount</span>
              <span className="font-bold text-emerald-600">₹{(form.required_loan / 100000).toFixed(1)} Lakh</span>
            </div>
            <input
              type="range"
              min="10000"
              max="10000000"
              step="50000"
              value={form.required_loan}
              onChange={(e) => setForm({ ...form, required_loan: Number(e.target.value) })}
              className="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-emerald-600"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full py-3 bg-emerald-600 hover:bg-emerald-700 text-white font-bold rounded-xl text-sm shadow transition-all flex items-center justify-center gap-2"
          >
            <Sparkles className="w-4 h-4" />
            <span>{loading ? 'Evaluating...' : 'Run Real-Time Scheme Compatibility'}</span>
          </button>
        </form>
      </div>
    </div>
  );
}
