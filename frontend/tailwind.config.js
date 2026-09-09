/** @type {import('tailwindcss').Config} */
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
