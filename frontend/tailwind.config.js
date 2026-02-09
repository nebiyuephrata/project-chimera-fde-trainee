/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#0f172a",
        fog: "#eef2ff",
        ember: "#f97316",
        moss: "#0f766e",
      },
      fontFamily: {
        display: ["Space Grotesk", "sans-serif"],
        body: ["IBM Plex Sans", "sans-serif"],
      },
      boxShadow: {
        glow: "0 0 24px rgba(15, 118, 110, 0.35)",
      },
    },
  },
  plugins: [],
};
