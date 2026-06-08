/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./app/**/*.{js,jsx,ts,tsx}", "./src/**/*.{js,jsx,ts,tsx}"],
  presets: [require("nativewind/preset")],
  theme: {
    extend: {
      colors: {
        primary: {
          50:  "#fff3ee",
          100: "#ffe4d5",
          200: "#ffc5a8",
          300: "#ff9d70",
          400: "#ff6b35",  // Brand orange
          500: "#ff4d12",
          600: "#f03208",
          700: "#c72209",
          800: "#9e1e10",
          900: "#7f1c11",
        },
        neutral: {
          50:  "#f8f8f8",
          100: "#f0f0f0",
          200: "#e4e4e4",
          300: "#d1d1d1",
          400: "#b4b4b4",
          500: "#9a9a9a",
          600: "#818181",
          700: "#6a6a6a",
          800: "#3d3d3d",
          900: "#1a1a1a",
        },
        agree:    "#22c55e",
        disagree: "#ef4444",
        metoo:    "#3b82f6",
      },
      fontFamily: {
        sans: ["System"],
      },
    },
  },
  plugins: [],
};
