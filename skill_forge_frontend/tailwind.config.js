import plugin from 'tailwindcss/plugin'

/** @type {import('tailwindcss').Config} */
const withOpacity = (variable) => {
  return ({ opacityValue }) => {
    if (opacityValue !== undefined) {
      return `rgba(var(${variable}), ${opacityValue})`
    }
    return `rgb(var(${variable}))`
  }
}

export default {
    content: [
      './index.html',
      './src/**/*.{js,ts,jsx,tsx}'
    ],
    theme: {
      extend: {
        colors: {
            primary: withOpacity('#145DA0'),
            secondary: withOpacity('#0C2D48'),
            accent: withOpacity('#2E8BC0'),
            text: withOpacity('#00f8fd'),
        },
        fontFamily: {
          inter: 'Inter',
          fira: "'Fira Code', monospace",
        }
      },
    },
    plugins: [
      require('@tailwindcss/typography'),
      ],
  }