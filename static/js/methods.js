//$(document).ready(function{
////    when the table gets displayed, roll up the jumbotron paragraph and reduce the header size
//   if len($('example'))
//});


 $(document).ready(function() {

    // add awesomeness to the table
    $('#example').DataTable();


    var tl = $('td').length;
    if (tl > 1) {
        $('#jumbo-text').slideUp(1500, 'swing');
        $('.jumbotron').animate({'padding': 10, 'margin-top': 25, 'margin-bottom': 25}, 1000);
    };

});


