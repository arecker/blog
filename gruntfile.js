module.exports = function(grunt){
    grunt.initConfig({
        
	jshint: {
	    all: [
                './static/scripts/*.js',
		'./*/static/*/scripts/*.js',
                './*/jasmine/*.js'
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
	},
        
        jasmine: {
            pivotal: {
                src: [
                    './static/scripts/*.js',
                    './*/static/*/scripts/*.js',
                ],
                options: {
                    specs: './*/jasmine/*.js',
                    vendor: [
                        'bower/bower_components/angular/angular.js',
                        'bower/bower_components/ngInfiniteScroll/build/ng-infinite-scroll.min.js',
                        'bower/bower_components/angular-route/angular-route.js',
                        'bower/bower_components/angular-mocks/angular-mocks.js'
                    ]
                }
            }
        }
        
    });
    
    grunt.loadNpmTasks('grunt-contrib-jshint');
    grunt.loadNpmTasks('grunt-contrib-jasmine');
    grunt.registerTask('default', ['jshint', 'jasmine']);
};
