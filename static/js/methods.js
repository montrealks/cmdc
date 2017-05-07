
 $(document).ready(function() {
    // add awesomeness to the table
    $('#example').DataTable();

    // Firbase connection
    var config = {
    apiKey: "AIzaSyBlYjeeJDdT2i4YkaCV6N6202pWd7s8ff0",
    authDomain: "cmdc-c7e14.firebaseapp.com",
    databaseURL: "https://cmdc-c7e14.firebaseio.com",
    projectId: "cmdc-c7e14",
    storageBucket: "cmdc-c7e14.appspot.com",
    messagingSenderId: "650723586198"
    };
    firebase.initializeApp(config);
    var database = firebase.database();

    // Firebase comment submit
    $('#feedback_submit').click(function() {
        console.log("new feedback received");

        //  Get the name and comment from the form
        var name = $('#name').val();
        var comment = $('#comment').val();

        console.log("name:" + name);

        if (!name || !comment ) {
            alert("Please provide both a name and a comment");
            return;
        }

        // push to the database
        firebase.database().ref('feedback/' + name).push({
        username: name,
        message: comment,
        date: firebase.database.ServerValue.TIMESTAMP});

        // reset the inputs
        $('#name').val('');
        $('#comment').val('');

        //  Hide the form
        $('.feedback_row').slideToggle();

        // Show feedback succesful alert
        $('#feedback_success_alert').show();
        setTimeout(function(){ $('#feedback_success_alert').hide(); }, 3000);

    });



    // Toggle feedback form
    $('#feedback').click(function(){
        console.log("toggle");
        $('.feedback_row').slideToggle();
    });

    // toggle between data table and map
    $('#table_button').click(function() {
        if (!$(this).hasClass('active')) {
            $(this).addClass('active');
            $('#map_button').removeClass('active');

            $('#results_table').slideDown('slow');
        }
    });
    $('#map_button').click(function() {
        if (!$(this).hasClass('active')) {
                $(this).addClass('active');
                $('#table_button').removeClass('active');
                $('#results_table').slideUp('slow');
                $.getScript( "https://maps.googleapis.com/maps/api/js?key=AIzaSyARltEJxYPhqjJVAcq1eR-mEveAVCZ0nKY&callback=initMap", function( data, textStatus, jqxhr ) {
                  console.log( data ); // Data returned
                  console.log( textStatus ); // Success
                  console.log( jqxhr.status ); // 200
                  console.log( "Load was performed." );
                });
        }
    });

    // Google Places Autocomplete
    var input = document.getElementById('address');
    var autocomplete = new google.maps.places.Autocomplete(input);


    // Shrink jumbotron after search
    var tl = $('td').length;
    if (tl > 1) {
        $('#jumbo-text').slideUp(1500, 'swing');
        $('.jumbotron').animate({'padding': 10, 'margin-top': 25, 'margin-bottom': 25}, 1000);
    };

});



