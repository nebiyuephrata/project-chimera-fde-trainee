/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        ink: "#0b1120",
        fog: "#e2e8f0",
        ember: "#f97316",
        moss: "#10b981",
        sun: "#facc15"
      },
      fontFamily: {
        display: ["Space Grotesk", "sans-serif"],
        body: ["IBM Plex Sans", "sans-serif"]
      },
      boxShadow: {
        soft: "0 16px 40px rgba(15, 23, 42, 0.45)",
        glow: "0 0 30px rgba(16, 185, 129, 0.25)"
      }
    }
  },
  plugins: []
};
