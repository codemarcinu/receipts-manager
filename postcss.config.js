module.exports = {
  plugins: [
    require('tailwindcss'),
    require('autoprefixer'),
    process.env.NODE_ENV === 'production' && require('cssnano')({
      preset: 'default',
    }),
    require('postcss-import'),
    require('postcss-custom-properties'),
  ].filter(Boolean)
}