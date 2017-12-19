(function() {
  var data    = {}
    , workers = null;

  init();

  function init() {

    experimentr.hideNext();

    // load previous workers file
    d3.json('modules/consent/blocked-workers.json', function(err, d) {
      workers = d;
      d3.select('#workerId').attr('disabled', null);
    });

    d3.selectAll('#workerId')
      .on('keypress', function() { data.workerId = this.value; })
      .on('blur', function() { data.workerId = this.value; });

    d3.select('#consentYes').on('click', function(){
      if (browser.name == "Firefox" || browser.name == "Chrome"){
        experimentr.startTimer('s1')
        data.browser_s1 = JSON.stringify(browser)
        data.complete_s1 = false
        data.complete_s2 = false
        experimentr.addData(data);
        experimentr.next()
      } else {
        d3.select('#invalidBrowser').style('display', 'inline');
      }
    });

    d3.select('#checkId').on('click', validate);
  }

  function validate() {
    // This check will probably not be necessary in the future.
    if( data.workerId ) {
      // experimentr.addData(data);

      if( workers.indexOf(data.workerId) == -1 ) {
        d3.select('#consentYes').attr('disabled', null);
      } else {
        d3.select('#invalidMessage').style('display', 'inline');
      }
    }
  }

  let browser = experimentr.get_browser_info();

}());
