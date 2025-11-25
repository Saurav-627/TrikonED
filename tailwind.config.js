/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: "class",
  content: [
    "./templates/**/*.html",
    "./core/templates/**/*.html",
    "./universities/templates/**/*.html",
    "./programs/templates/**/*.html",
    "./students/templates/**/*.html",
    "./applications/templates/**/*.html",
  ],
  theme: {
    extend: {
      colors: {
        // Original theme colors
        "primary-light": "#FFF8E1",
        "primary-base": "#FFF3B0",
        "accent-green": "#2DD4BF",
        "accent-orange": "#FB923C",
        "neutral-white": "#FFFFFF",
        "neutral-light": "#F8FAFC",
        "text-primary": "#0F172A",
        "text-secondary": "#475569",
        "text-muted": "#94A3B8",
        success: "#10B981",
        warning: "#F59E0B",
        error: "#EF4444",
        info: "#3B82F6",
        // Landing page theme colors
        primary: "#ff9900",
        "background-light": "#f8f7f5",
        "background-dark": "#231b0f",
        highlight: "#FFC107",
      },
      fontFamily: {
        display: ["Inter", "Poppins", "sans-serif"],
        body: ["Inter", "Lato", "system-ui", "sans-serif"],
      },
      borderRadius: {
        DEFAULT: "0.25rem",
        lg: "0.5rem",
        xl: "0.75rem",
        "2xl": "1.5rem",
        full: "9999px",
      },
      boxShadow: {
        card: "0 4px 12px rgba(0, 0, 0, 0.08)",
        "card-hover": "0 8px 24px rgba(0, 0, 0, 0.12)",
      },
    },
  },
  plugins: [require("@tailwindcss/forms"), require("@tailwindcss/typography")],
};
