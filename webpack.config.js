const path = require('path');

module.exports = {
  entry: './src/index',
  output: {
    path: path.resolve(__dirname,
      './resources/templates/themes/devth/js/'),
    filename: 'dist.js'
  },

  module: {
    rules: [
      {
        test: /\.css$/i,
        use: ['style-loader', 'css-loader'],
      },
      {
        test: /\.s[ac]ss$/i,
        use: [
          // Creates `style` nodes from JS strings
          'style-loader',
          // Translates CSS into CommonJS
          'css-loader',
          // Compiles Sass to CSS
          'sass-loader',
        ],
      },

    ],
  },

  resolve: {
  }
}
