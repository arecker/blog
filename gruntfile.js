module.exports = function(grunt){
    grunt.initConfig({
	jshint: {
	    all: [
		'./static/js/app.js',
		'./*/static/*/scripts/*'
	    ],
	    options: {
		curly: true,
		eqeqeq: true,
		eqnull: true,
		camelcase: true,
		forin: true,
		funcscope: true,
		latedef: true,
		maxparams: 5,
		futurehostile: true
	    }
	}
    });
    grunt.loadNpmTasks('grunt-contrib-jshint');
    grunt.registerTask('default', ['jshint']);
};
