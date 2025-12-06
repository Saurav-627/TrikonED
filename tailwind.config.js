/** @type {import('tailwindcss').Config} */
module.exports = {
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
        // ===== CENTRALIZED THEME COLORS =====
        // Change these values to update colors across the entire system

        // Primary Color - Main brand color
        primary: {
          DEFAULT: "#ff9900", // Change this to update primary color everywhere
          light: "#FFF8E1",
          base: "#FFF3B0",
          5: "rgba(255, 153, 0, 0.05)",
          10: "rgba(255, 153, 0, 0.1)",
          20: "rgba(255, 153, 0, 0.2)",
          30: "rgba(255, 153, 0, 0.3)",
          40: "rgba(255, 153, 0, 0.4)",
          50: "rgba(255, 153, 0, 0.5)",
        },

        // Secondary Color - Complementary color
        secondary: {
          DEFAULT: "#01764e", // Change this to update secondary color everywhere
          5: "rgba(1, 118, 78, 0.05)",
          10: "rgba(1, 118, 78, 0.1)",
          20: "rgba(1, 118, 78, 0.2)",
          30: "rgba(1, 118, 78, 0.3)",
          40: "rgba(1, 118, 78, 0.4)",
          50: "rgba(1, 118, 78, 0.5)",
        },

        // Accent Color - For highlights and special elements
        accent: {
          DEFAULT: "#febd08", // Change this to update accent color everywhere
          green: "#2DD4BF",
          orange: "#FB923C",
          5: "rgba(254, 189, 8, 0.05)",
          10: "rgba(254, 189, 8, 0.1)",
          20: "rgba(254, 189, 8, 0.2)",
          30: "rgba(254, 189, 8, 0.3)",
          40: "rgba(254, 189, 8, 0.4)",
          50: "rgba(254, 189, 8, 0.5)",
        },

        // Background Colors
        background: {
          DEFAULT: "#f8f7f5",
          light: "#f8f7f5",
          card: "#FFFFFF",
          alt: "#1a1307",
        },

        // Border Colors
        border: {
          DEFAULT: "#e7e2da",
          light: "#e7e2da",
          medium: "#3a2d1b",
        },

        // Neutral Colors
        neutral: {
          white: "#FFFFFF",
          light: "#F8FAFC",
        },

        // Text Colors
        text: {
          DEFAULT: "#181510",
          primary: "#181510",
          secondary: "#8d7a5e",
          muted: "#a19077",
        },

        // Status Colors
        success: "#10B981",
        warning: "#F59E0B",
        error: "#EF4444",
        info: "#3B82F6",
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
