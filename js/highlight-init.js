(function() {
    var codeBlocks = document.getElementsByTagName('pre'),
	i, cur, classes;

    for (i=0; i<codeBlocks.length ; i++) {
	cur = codeBlocks[i];
	classes = cur.className.split(' ').filter(function(i) {
	    return i.indexOf('src-') !== -1;
	}).map(function(i) {
	    return i.split('src-')[1];
	});
	cur.className += classes.join(' ');
	hljs.highlightBlock(cur);
    }
}());
