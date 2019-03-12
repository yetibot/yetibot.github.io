const path = require('path');

module.exports = {
  entry: './src/index',
  output: {
    path: path.resolve(__dirname,
      './resources/templates/themes/devth/js/'),
    filename: 'dist.js'
  },
  resolve: {
    alias: {
      "react": "preact-compat",
      "react-dom": "preact-compat"
    }
  }
}
