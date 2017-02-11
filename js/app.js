var blog = (function (apiURL) {

  var api = {},

      getRandomImageElement = function() {
	return document.getElementById('randomImage');
      },

      displayLoadingImage = function() {
	getRandomImageElement().src = '/images/loading.gif';
      },

      toImgSrc = function(base64) {
	return 'data:image/png;base64,' + base64.replace(/["]+/g, '');
      },

      displayRandomImage = function() {
	var request = new XMLHttpRequest();

	request.onreadystatechange = function() {
	  if (request.readyState == XMLHttpRequest.DONE) {
	    getRandomImageElement().src = toImgSrc(request.responseText);
	  }
	};

	request.open('GET', apiURL, true);
	request.send()
      };

  api.cycleRandomImage = function() {
    displayLoadingImage();
    displayRandomImage();
  };

  return api;

}('https://ndgz5xamgb.execute-api.us-west-2.amazonaws.com/dev/'));
