import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Sparkles, Sliders, CheckCircle, ArrowRight } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import api from '../services/api';

export default function RequirementQuestionnairePage() {
  const { t } = useLanguage();
  const navigate = useNavigate();
  const [form, setForm] = useState({
    social_category: 'SC',
    gender: 'female',
    age: 28,
    state: 'Tamil Nadu',
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
            <span>{t('Fast Analyzer', 'Fast Analyzer')}</span>
          </div>
          <h1 className="text-2xl font-extrabold text-slate-900">{t('rapid requirement questionnaire')}</h1>
          <p className="text-xs text-slate-500 mt-1">{t('directly adjust financial parameters to see scheme eligibility recalculate instantly.')}</p>
        </div>

        <form onSubmit={handleEvaluate} className="space-y-4">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">{t('target marginalized category')}</label>
              <select
                value={form.social_category}
                onChange={(e) => setForm({ ...form, social_category: e.target.value })}
                className="w-full px-3 py-2 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500"
              >
                <option value="SC">{t('scheduled caste (sc)')}</option>
                <option value="ST">{t('scheduled tribe (st)')}</option>
                <option value="OBC">{t('other backward classes (obc)')}</option>
                <option value="Minority">{t('minority community')}</option>
                <option value="Women/Special">{t('women entrepreneur / special category')}</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">{t('gender')}</label>
              <select
                value={form.gender}
                onChange={(e) => setForm({ ...form, gender: e.target.value })}
                className="w-full px-3 py-2 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500"
              >
                <option value="female">{t('female')}</option>
                <option value="male">{t('male')}</option>
                <option value="transgender">{t('transgender')}</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">{t('business nature')}</label>
              <select
                value={form.business_type}
                onChange={(e) => setForm({ ...form, business_type: e.target.value })}
                className="w-full px-3 py-2 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500"
              >
                <option value="manufacturing">{t('manufacturing')}</option>
                <option value="service">{t('service')}</option>
                <option value="trading">{t('trading')}</option>
                <option value="street_vendor">{t('street vendor / hawkers')}</option>
                <option value="artisan">{t('artisan / handicrafts')}</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">{t('location setting')}</label>
              <select
                value={form.area_type}
                onChange={(e) => setForm({ ...form, area_type: e.target.value })}
                className="w-full px-3 py-2 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500"
              >
                <option value="rural">{t('rural')}</option>
                <option value="urban">{t('urban')}</option>
              </select>
            </div>
          </div>

          <div>
            <div className="flex justify-between text-xs font-semibold text-slate-700 mb-1">
              <span>{t('required loan amount (₹)')}</span>
              <span className="font-bold text-emerald-600">₹{(form.required_loan / 100000).toFixed(1)} {t('unitLakh')}</span>
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
            className="w-full py-3 bg-emerald-600 hover:bg-emerald-700 text-white font-bold rounded-xl text-sm shadow transition-all flex items-center justify-center gap-2 cursor-pointer"
          >
            <Sparkles className="w-4 h-4" />
            <span>{loading ? t('evaluating...') : t('run real-time scheme compatibility')}</span>
          </button>
        </form>
      </div>
    </div>
  );
}
