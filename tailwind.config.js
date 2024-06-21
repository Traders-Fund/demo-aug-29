/** @type {import('tailwindcss').Config} */

import colors from "tailwind-colors";
// console.log(colors.red[500]); // #ed8936

module.exports = {
  content: ["./src/templates/**/*.{html,js}",
     "./node_modules/flowbite/**/*.js"
  ],
  theme: {
    extend: {
      colors: {
        // Include all Tailwind CSS colors
        ...colors,
      },
    },
  },
  plugins: [
    require('flowbite/plugin')
  ],
};
