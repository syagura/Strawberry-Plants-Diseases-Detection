/** @type {import('tailwindcss').Config} */
module.exports = {
	content: [
			"./templates/**/*.html",
			"./static/src/**/*.js",
			"./node_modules/flowbite/**/*.js"
	],
	theme: {
		extend: {
			colors: {
				primary: '#003C43',
				secondary: '#135D66',
				third: '#77B0AA',
				fourth: '#E3FEF7',
				text: '#F5F5F5',
				// text2: '#190482',
				// text: '#190482',
			},
			fontFamily: {
				raleway: ["Raleway", 'sans-serif'],
				pacifio: ["Pacifico", 'cursive'],
				vibur: ['Vibur', 'cursive'],
				montserrat: ['Montserrat', 'sans-serif'],
			},
		},
	},
	plugins: [
		require("flowbite/plugin")
	],
}