import os

base = "C:/Users/aksha/.gemini/antigravity/scratch/scheme-sathi/frontend"

def save(rel_path, content):
    full_path = os.path.join(base, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created: {rel_path}")

# vite.config.js
save("vite.config.js", """import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true
      },
      '/uploads': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true
      }
    }
  }
})
""")

# tailwind.config.js
save("tailwind.config.js", """/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        gov: {
          blue: '#0B4F8A',
          darkblue: '#07335C',
          light: '#F0F6FC',
          accent: '#FF9933', // Saffron
          green: '#138808',  // India Green
          border: '#D0D7DE'
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'Segoe UI', 'Roboto', 'sans-serif']
      }
    },
  },
  plugins: [],
}
""")

# postcss.config.js
save("postcss.config.js", """export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
""")

# index.html
save("index.html", """<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%230B4F8A'><path d='M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5'/></svg>" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>SCHEME SATHI | AI-Driven Scheme Discovery for Marginalized Entrepreneurs</title>
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <!-- Leaflet CSS -->
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin="" />
  </head>
  <body class="bg-slate-50 text-slate-900 antialiased font-sans min-h-screen">
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
""")

# src/index.css
save("src/index.css", """@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  body {
    @apply bg-slate-50 text-slate-900 selection:bg-gov-blue selection:text-white;
  }
}

/* Custom Scrollbar */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}
::-webkit-scrollbar-track {
  background: #f1f5f9;
}
::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

/* Leaflet Map Fixes */
.leaflet-container {
  width: 100%;
  height: 100%;
  border-radius: 0.75rem;
  z-index: 10;
}
""")

# src/services/api.js
save("src/services/api.js", """import axios from 'axios';

const API_BASE = '/api';

const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Attach JWT token to requests if present
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('scheme_sathi_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const authAPI = {
  login: (credentials) => api.post('/auth/login', credentials),
  register: (userData) => api.post('/auth/register', userData),
  getMe: () => api.get('/auth/me'),
};

export const profileAPI = {
  getProfile: () => api.get('/profile'),
  updateProfile: (data) => api.put('/profile', data),
};

export const schemesAPI = {
  getAll: (params) => api.get('/schemes', { params }),
  getById: (id) => api.get(`/schemes/${id}`),
};

export const matchingAPI = {
  analyze: (data) => api.post('/matching/analyze', data),
  checkEligibility: (schemeId, data) => api.post(`/matching/eligibility/check/${schemeId}`, data),
};

export const financeAPI = {
  calculateEmi: (data) => api.post('/finance/emi', data),
};

export const documentsAPI = {
  upload: (formData) => api.post('/documents/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }),
  getUserDocuments: () => api.get('/documents'),
  getSchemeChecklist: (schemeId) => api.get(`/documents/scheme/${schemeId}/checklist`),
};

export const partnersAPI = {
  getAll: (params) => api.get('/partners', { params }),
  getRecommended: (params) => api.get('/partners/recommended', { params }),
};

export const chatAPI = {
  sendMessage: (data) => api.post('/chat/message', data),
};

export const notificationsAPI = {
  getAll: () => api.get('/notifications'),
  markAsRead: (id) => api.put(`/notifications/${id}/read`),
};

export const adminAPI = {
  getDashboard: () => api.get('/admin/dashboard'),
  createScheme: (data) => api.post('/admin/schemes', data),
  updateScheme: (id, data) => api.put(`/admin/schemes/${id}`, data),
  deleteScheme: (id) => api.delete(`/admin/schemes/${id}`),
  createRule: (data) => api.post('/admin/rules', data),
  createPartner: (data) => api.post('/admin/partners', data),
  getUsers: () => api.get('/admin/users'),
};

export default api;
""")

print("Frontend core files created successfully!")
