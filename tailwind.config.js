/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/web/templates/**/*.html",
    "./src/web/static/js/**/*.js",
  ],
  theme: {
    extend: {
      colors: {
        // Rozszerzone kolory primary
        'primary': {
          50: '#F3E5F5',
          100: '#E1BEE7',
          200: '#CE93D8',
          300: '#BA68C8',
          400: '#AB47BC',
          500: '#9C27B0', // Bazowy kolor primary
          600: '#8E24AA',
          700: '#7B1FA2',
          800: '#6A1B9A',
          900: '#4A148C',
          // Nowe odcienie
          'light': '#B868C8',
          'dark': '#6A1B9A',
          'accent': '#F3E5F5',
        },
        
        // Rozszerzone kolory secondary
        'secondary': {
          50: '#E8F5E9',
          100: '#C8E6C9',
          200: '#A5D6A7',
          300: '#81C784',
          400: '#66BB6A',
          500: '#4CAF50', // Bazowy kolor secondary
          600: '#43A047',
          700: '#388E3C',
          800: '#2E7D32',
          900: '#1B5E20',
          // Nowe odcienie
          'light': '#81C784',
          'dark': '#2E7D32',
          'accent': '#E8F5E9',
        },
        
        // Rozszerzone kolory błędów, ostrzeżeń itp.
        'error': {
          50: '#FFEBEE',
          100: '#FFCDD2',
          200: '#EF9A9A',
          300: '#E57373',
          400: '#EF5350',
          500: '#F44336', // Bazowy kolor błędu
          600: '#E53935',
          700: '#D32F2F',
          800: '#C62828',
          900: '#B71C1C',
        },
        
        'warning': {
          50: '#FFF3E0',
          100: '#FFE0B2',
          200: '#FFCD85',
          300: '#FFB74D',
          400: '#FFA726',
          500: '#FF9800', // Bazowy kolor ostrzeżenia
          600: '#FB8C00',
          700: '#F57C00',
          800: '#EF6C00',
          900: '#E65100',
        },
        
        'success': {
          50: '#E8F5E9',
          100: '#C8E6C9',
          200: '#A5D6A7',
          300: '#81C784',
          400: '#66BB6A',
          500: '#4CAF50', // Bazowy kolor sukcesu
          600: '#43A047',
          700: '#388E3C',
          800: '#2E7D32',
          900: '#1B5E20',
        },
        
        // Neutralne kolory
        'neutral': {
          50: '#FAFAFA',
          100: '#F5F5F5',
          200: '#EEEEEE',
          300: '#E0E0E0',
          400: '#BDBDBD',
          500: '#9E9E9E',
          600: '#757575',
          700: '#616161',
          800: '#424242',
          900: '#212121',
        },
        
        'background': '#FFFFFF',
        'surface': '#FFFFFF',
      },
      
      // Pozostałe rozszerzenia jak poprzednio...
      borderRadius: {
        'material-sm': '4px',
        'material-md': '8px',
        'material-lg': '16px',
      },
      boxShadow: {
        'material-1': '0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24)',
        'material-2': '0 3px 6px rgba(0,0,0,0.15), 0 2px 4px rgba(0,0,0,0.12)',
        'material-3': '0 10px 20px rgba(0,0,0,0.15), 0 3px 6px rgba(0,0,0,0.10)',
        'material-4': '0 14px 28px rgba(0,0,0,0.25), 0 10px 10px rgba(0,0,0,0.22)',
        'material-5': '0 19px 38px rgba(0,0,0,0.30), 0 15px 12px rgba(0,0,0,0.22)',
      },
      spacing: {
        'material-1': '4px',
        'material-2': '8px',
        'material-3': '16px',
        'material-4': '24px',
        'material-5': '32px',
        'material-6': '40px',
      },
    },
  },
  plugins: [],
}