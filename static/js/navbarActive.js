$(document).ready(function() {
    var currentURL = window.location.pathname;
  
    $('#navbar a').each(function() {
      var linkURL = $(this).attr('href');
  
      if (currentURL === linkURL) {
        $(this).addClass('active');
      }
    });
  
    $('#navbar a').click(function() {
      $('#navbar a').removeClass('active');
      $(this).addClass('active');
    });
  });
  