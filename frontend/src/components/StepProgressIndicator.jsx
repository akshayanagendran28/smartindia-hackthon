import React from 'react';
import { Link } from 'react-router-dom';
import { 
  User, Sliders, FileCheck, Sparkles, Award, Calculator, 
  MapPin, CheckCircle2, Lock 
} from 'lucide-react';
import { useApplication } from '../context/ApplicationContext';

const STEPS = [
  { id: 1, key: 'profile', title: '1. Profile', icon: User, path: '/profile' },
  { id: 2, key: 'requirement', title: '2. Requirement', icon: Sliders, path: '/find-scheme' },
  { id: 3, key: 'documents', title: '3. Documents', icon: FileCheck, path: '/documents' },
  { id: 4, key: 'eligibility', title: '4. Eligibility', icon: Sparkles, path: '/results' },
  { id: 5, key: 'scheme', title: '5. Scheme', icon: Award, path: '/results' },
  { id: 6, key: 'emi', title: '6. EMI', icon: Calculator, path: '/calculator' },
  { id: 7, key: 'partner', title: '7. Partner Map', icon: MapPin, path: '/partners' },
];

export default function StepProgressIndicator({ currentStep = 1 }) {
  const { 
    isProfileConfirmed, 
    allDocumentsVerified, 
    selectedScheme, 
    canAccess 
  } = useApplication();

  const isStepComplete = (stepId) => {
    if (stepId === 1) return isProfileConfirmed;
    if (stepId === 2) return isProfileConfirmed;
    if (stepId === 3) return allDocumentsVerified;
    if (stepId === 4) return allDocumentsVerified;
    if (stepId === 5) return Boolean(selectedScheme);
    if (stepId === 6) return Boolean(selectedScheme);
    if (stepId === 7) return Boolean(selectedScheme);
    return false;
  };

  const isStepLocked = (stepId) => {
    if (stepId <= 3) return false;
    if (stepId === 4 || stepId === 5) return !allDocumentsVerified;
    if (stepId === 6 || stepId === 7) return !selectedScheme;
    return false;
  };

  return (
    <div className="w-full bg-white border border-slate-200 rounded-2xl p-4 shadow-sm mb-6">
      <div className="flex items-center justify-between overflow-x-auto pb-2 sm:pb-0 gap-2 sm:gap-4">
        {STEPS.map((step, idx) => {
          const Icon = step.icon;
          const isCurrent = currentStep === step.id;
          const isCompleted = isStepComplete(step.id);
          const isLocked = isStepLocked(step.id);

          return (
            <React.Fragment key={step.id}>
              {/* Step Pill */}
              <div className="flex flex-col items-center shrink-0 min-w-[72px] sm:min-w-[90px] text-center">
                <div
                  className={`w-9 h-9 sm:w-10 sm:h-10 rounded-2xl flex items-center justify-center font-bold text-xs transition-all relative ${
                    isCurrent
                      ? 'bg-emerald-600 text-white ring-4 ring-emerald-100 shadow-md scale-105'
                      : isCompleted
                      ? 'bg-emerald-100 text-emerald-800 border border-emerald-300'
                      : isLocked
                      ? 'bg-slate-100 text-slate-400 border border-slate-200 cursor-not-allowed'
                      : 'bg-white text-slate-600 border border-slate-300 hover:border-slate-400'
                  }`}
                  title={
                    isLocked 
                      ? step.id >= 6 
                        ? 'Select an eligible scheme to unlock' 
                        : 'Complete document verification to unlock'
                      : step.title
                  }
                >
                  {isCompleted && !isCurrent ? (
                    <CheckCircle2 className="w-5 h-5 text-emerald-700" />
                  ) : isLocked ? (
                    <Lock className="w-4 h-4 text-slate-400" />
                  ) : (
                    <Icon className="w-4 h-4 sm:w-5 sm:h-5" />
                  )}

                  {isLocked && (
                    <span className="absolute -top-1 -right-1 w-2.5 h-2.5 bg-amber-400 rounded-full ring-2 ring-white" />
                  )}
                </div>

                <span className={`text-[11px] font-bold mt-1.5 truncate max-w-[85px] sm:max-w-none ${
                  isCurrent ? 'text-emerald-700' : isCompleted ? 'text-slate-800' : isLocked ? 'text-slate-400' : 'text-slate-600'
                }`}>
                  {step.title}
                </span>

                <span className="text-[9px] text-slate-400 hidden sm:block">
                  {isCurrent ? 'Current' : isCompleted ? 'Completed' : isLocked ? 'Locked 🔒' : 'Next'}
                </span>
              </div>

              {/* Connecting Line between steps */}
              {idx < STEPS.length - 1 && (
                <div className="flex-1 min-w-[12px] sm:min-w-[20px] h-0.5 bg-slate-200 relative self-center mb-4">
                  <div 
                    className="h-full bg-emerald-500 transition-all duration-300"
                    style={{ 
                      width: isCompleted ? '100%' : '0%' 
                    }}
                  />
                </div>
              )}
            </React.Fragment>
          );
        })}
      </div>
    </div>
  );
}
