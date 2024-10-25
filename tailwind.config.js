/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{html,js,jsx,ts,tsx}",
    "./node_modules/tw-elements/js/**/*.js",
  ],
  theme: {
    extend: {
      fontFamily: {
        bai: ["Bai Jamjuree", "sans-serif"],
      },
    },
  },
  darkMode: "class",
  plugins: [
    require("tw-elements/plugin.cjs"),
    require("@tailwindcss/typography"),
  ],
};
