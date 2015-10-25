
$( document ).ready(function() {
$('button').on('click', function() {
var message = $('#flowNow').val().substring();
//   $('<span><h2>Here is what you are working on!</h2></span>');
  $('#flowNow').remove();
  $('#hiddenDiv2').append('<h2>In progress: </h2>' + message);
//   $('.flowNow').remove('#time');
//   $('button').remove();
 
  
});
});

//timer function
$('#startButton').on('click', function() {
// var message = $('#flowNow').val().substring();
function startTimer(duration, display) {
    var timer = duration, minutes, seconds;
    setInterval(function () {
        minutes = parseInt(timer / 60, 10)
        seconds = parseInt(timer % 60, 10);

        minutes = minutes < 10 ? "0" + minutes : minutes;
        seconds = seconds < 10 ? "0" + seconds : seconds;

        display.text(minutes + ":" + seconds);

        if (--timer < 0) {
            timer = alert("Great job! You're done");
        }
    }, 1000);
}

$(function ($) {
    var twentyFiveMinutes = 60 * 25,
        display = $('#time');
    startTimer(twentyFiveMinutes, display);
});
});
