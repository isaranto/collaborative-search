$(document).ready(function () {

  $( '#search-button' ).click( function() {
        var query = $('#search-text').val()
        window.location = '/'+query+'/1';
        
    } );
  $( ".note-expand" ).click(function() {
      $(this).next('form').toggle();
    });
  $( ".note-row" ).click(function() {
      $(this).next('.notes-content').toggle();
      $(this).next('.note-header').text('Hide Notes')
    });

 });