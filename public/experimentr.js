experimentr = function() {
  var experimentr = {
    version: "0.0.1"
  };

  var sequence;

  experimentr.start = function() {
    console.log('starting experiment sequence: ' + sequence);
    var mainDiv = d3.select('body').append('div')
      .attr('id', 'experimentr');
    var expDiv = mainDiv.selectAll('.experimentr-section')
      .data(sequence)
      .enter().append('div')
      .classed('experimentr-section', true)
      .each(loadHTML);
    function loadHTML() {
      var div = d3.select(this);
      d3.html(div.datum(), function(err, d) {
        if(err) console.log(err);
        div.node().appendChild(d);
      });
    }
  };

  experimentr.sequence = function(x) {
    if(!arguments.length) return sequence;
    sequence = x;
    return experimentr;
  }

  return experimentr;
}();
