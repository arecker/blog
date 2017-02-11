var blog = (function () {

  var api = {},

      getRandomImageElement = function() {
	return document.getElementById('randomImage');
      },

      displayLoadingImage = function() {
	getRandomImageElement().src = '/images/loading.gif';
      },

      displayRandomImage = function() {
	var request = new XMLHttpRequest();
	request.onreadystatechange = function() {
	  if (request.readyState == XMLHttpRequest.DONE) {
	    getRandomImageElement().src = 'data:image/png;base64,' + request.responseText.replace(/["]+/g, '')
	  }
	};
	request.open('GET', 'https://ndgz5xamgb.execute-api.us-west-2.amazonaws.com/dev/', true);
	request.send()
      };

  api.cycleRandomImage = function() {
    displayLoadingImage();
    displayRandomImage();
  };

  return api;

}());
