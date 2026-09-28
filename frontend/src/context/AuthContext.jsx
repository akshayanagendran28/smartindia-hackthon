import React, { createContext, useContext, useState, useEffect } from 'react';
import { authAPI, profileAPI } from '../services/api';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [profile, setProfile] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('scheme_sathi_token') || null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const initAuth = async () => {
      const storedToken = localStorage.getItem('scheme_sathi_token');
      const storedUser = localStorage.getItem('scheme_sathi_user');
      if (storedToken) {
        try {
          const res = await authAPI.getMe();
          setUser(res.data);
          const profRes = await profileAPI.getProfile();
          setProfile(profRes.data);
        } catch (err) {
          if (storedUser) {
            try {
              setUser(JSON.parse(storedUser));
            } catch (e) {}
          }
        }
      }
      setLoading(false);
    };
    initAuth();
  }, []);

  const login = async (email, password) => {
    try {
      const res = await authAPI.login({ email, password });
      const { access_token, user: loggedUser } = res.data;
      localStorage.setItem('scheme_sathi_token', access_token);
      localStorage.setItem('scheme_sathi_user', JSON.stringify(loggedUser));
      setToken(access_token);
      setUser(loggedUser);
      
      const profRes = await profileAPI.getProfile();
      setProfile(profRes.data);
      return { success: true, user: loggedUser, profile: profRes.data };
    } catch (err) {
      console.error('Login failed:', err);
      const errorMsg = err.response?.data?.detail || 'Invalid credentials or connection error';
      return { success: false, error: errorMsg };
    }
  };

  const register = async (userData) => {
    try {
      const res = await authAPI.register(userData);
      const { access_token, user: newUser } = res.data;
      localStorage.setItem('scheme_sathi_token', access_token);
      localStorage.setItem('scheme_sathi_user', JSON.stringify(newUser));
      setToken(access_token);
      setUser(newUser);
      
      try {
        const profRes = await profileAPI.getProfile();
        setProfile(profRes.data);
      } catch (pErr) {
        console.warn('Profile fetch after registration:', pErr);
      }
      return { success: true, user: newUser };
    } catch (err) {
      console.error('Registration failed:', err);
      const errorMsg = err.response?.data?.detail || 'Registration failed. Please verify your details.';
      return { success: false, error: errorMsg };
    }
  };

  const logout = () => {
    localStorage.removeItem('scheme_sathi_token');
    localStorage.removeItem('scheme_sathi_user');
    setToken(null);
    setUser(null);
    setProfile(null);
  };

  const refreshProfile = async () => {
    try {
      const profRes = await profileAPI.getProfile();
      setProfile(profRes.data);
      return profRes.data;
    } catch (err) {
      console.error('Failed to refresh profile', err);
      return null;
    }
  };

  return (
    <AuthContext.Provider value={{
      user, profile, token, loading, login, register, logout, refreshProfile, setUser, setProfile
    }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
