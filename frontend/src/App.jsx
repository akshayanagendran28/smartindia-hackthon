import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import { LanguageProvider } from './context/LanguageContext';

// Layouts
import Navbar from './layouts/Navbar';
import Footer from './layouts/Footer';
import DashboardLayout from './layouts/DashboardLayout';

// Public & User Pages
import LandingPage from './pages/LandingPage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import UserDashboard from './pages/UserDashboard';
import UserProfilePage from './pages/UserProfilePage';
import FindMySchemePage from './pages/FindMySchemePage';
import RequirementQuestionnairePage from './pages/RequirementQuestionnairePage';
import SchemeResultsPage from './pages/SchemeResultsPage';
import SchemeDetailsPage from './pages/SchemeDetailsPage';
import EligibilityExplanationPage from './pages/EligibilityExplanationPage';
import EmiCalculatorPage from './pages/EmiCalculatorPage';
import DocumentAssistantPage from './pages/DocumentAssistantPage';
import DocumentChecklistPage from './pages/DocumentChecklistPage';
import PartnerMapPage from './pages/PartnerMapPage';
import ChatAssistantPage from './pages/ChatAssistantPage';
import ApplicationReadinessPage from './pages/ApplicationReadinessPage';
import NotificationsPage from './pages/NotificationsPage';
import HistoryPage from './pages/HistoryPage';

// Admin Pages
import AdminDashboard from './pages/admin/AdminDashboard';
import AdminSchemeManagement from './pages/admin/AdminSchemeManagement';
import AdminRuleManagement from './pages/admin/AdminRuleManagement';
import AdminPartnerManagement from './pages/admin/AdminPartnerManagement';
import AdminUserManagement from './pages/admin/AdminUserManagement';
import AdminAnalyticsPage from './pages/admin/AdminAnalyticsPage';

// Protected Route Component
function ProtectedRoute({ children, roleRequired }) {
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-50">
        <div className="text-sm font-semibold text-slate-500 animate-pulse">Loading Scheme Sathi...</div>
      </div>
    );
  }

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  if (roleRequired && user.role !== roleRequired) {
    return <Navigate to="/dashboard" replace />;
  }

  return children;
}

export default function App() {
  return (
    <LanguageProvider>
      <AuthProvider>
        <BrowserRouter>
          <div className="min-h-screen flex flex-col bg-slate-50 text-slate-900 font-sans selection:bg-emerald-500 selection:text-white">
            <Navbar />
            <main className="flex-grow">
              <Routes>
                {/* Public Routes */}
                <Route path="/" element={<LandingPage />} />
                <Route path="/login" element={<LoginPage />} />
                <Route path="/register" element={<RegisterPage />} />
                <Route path="/calculator" element={<EmiCalculatorPage />} />
                <Route path="/chat" element={<ChatAssistantPage />} />
                <Route path="/find-scheme" element={<FindMySchemePage />} />
                <Route path="/questionnaire" element={<RequirementQuestionnairePage />} />
                <Route path="/results" element={<SchemeResultsPage />} />
                <Route path="/schemes" element={<SchemeResultsPage />} />
                <Route path="/scheme/:id" element={<SchemeDetailsPage />} />
                <Route path="/explanation/:id" element={<EligibilityExplanationPage />} />
                <Route path="/partners" element={<PartnerMapPage />} />
                <Route path="/documents" element={<DocumentAssistantPage />} />
                <Route path="/checklist" element={<DocumentChecklistPage />} />

                {/* Beneficiary Dashboard & Protected Routes */}
                <Route
                  path="/dashboard"
                  element={
                    <ProtectedRoute>
                      <UserDashboard />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/profile"
                  element={
                    <ProtectedRoute>
                      <UserProfilePage />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/readiness"
                  element={
                    <ProtectedRoute>
                      <ApplicationReadinessPage />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/notifications"
                  element={
                    <ProtectedRoute>
                      <NotificationsPage />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/history"
                  element={
                    <ProtectedRoute>
                      <HistoryPage />
                    </ProtectedRoute>
                  }
                />

                {/* Admin Management Suite */}
                <Route
                  path="/admin"
                  element={
                    <ProtectedRoute roleRequired="admin">
                      <AdminDashboard />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/admin/schemes"
                  element={
                    <ProtectedRoute roleRequired="admin">
                      <AdminSchemeManagement />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/admin/rules"
                  element={
                    <ProtectedRoute roleRequired="admin">
                      <AdminRuleManagement />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/admin/partners"
                  element={
                    <ProtectedRoute roleRequired="admin">
                      <AdminPartnerManagement />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/admin/users"
                  element={
                    <ProtectedRoute roleRequired="admin">
                      <AdminUserManagement />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/admin/analytics"
                  element={
                    <ProtectedRoute roleRequired="admin">
                      <AdminAnalyticsPage />
                    </ProtectedRoute>
                  }
                />

                {/* Fallback */}
                <Route path="*" element={<Navigate to="/" replace />} />
              </Routes>
            </main>
            <Footer />
          </div>
        </BrowserRouter>
      </AuthProvider>
    </LanguageProvider>
  );
}
