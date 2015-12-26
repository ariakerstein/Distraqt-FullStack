// alert("test")

//http://codereview.stackexchange.com/questions/102456/pomodoro-timer-via-setinterval

var timer;

$(document).ready(function(){
var working = false;
var active = '';
var workTime =0;
var breakTime = 0;
checkStatus();

  //Test Vars

/*  Alternate Method of 'checkStatus Function'
working ? $('#pause').addClass('disabled')&& $('#start').removeClass('disabled'): $('#start').addClass('disabled')&& $('#pause').removeClass('disabled');
 */

  //Controls if a button is disabled based on status of timer
function checkStatus() {
  if (!working) {
    $('#start').removeClass('disabled');
    $('#pause').addClass('disabled');
    $('#reset').addClass('disabled');
    $('#myAlert').hide();
    $('#work').show();
    $('#saveEntry').show();
    $('#checkbox').show();
    $('.col-xs-6').show();
    $('.modal-header').hide();
    $('.page-header').hide();
    $('#JumbotronBrand').hide();
    $('.close').hide();
    
    // $('#result').hide();
    } else {
    $('#pause').removeClass('disabled');
    $('#reset').removeClass('disabled');
    $('#start').addClass('disabled');
    $('#saveEntry').hide();
    $('#checkbox').hide();
    $('#myAlert').hide();
    // $('#myAlert-fail').hide();
    $('.col-xs-6').show();
    $('.modal-header').show();
    $('.page-header').hide();
    $('#work').hide();
    // $('#label').hide();

    // $('#result').show();
    }
}
//End Check Status
    //Function to Show Time  !!Finished!!
   function showTime(time) {
   var min = Math.floor(time/60);
   var sec = Math.round(time%60);
      if (sec < 10) {
        sec = '0' + sec
      }
      var timeString = min+':'+sec
      $('#msg').text("" + timeString+" remaining")
     }
  //End showTime
  //Enables the timer  !!Mostly Finished!!
function startTimer() {
  // $('.jumbotron').css('visibility', 'visible');
  return setInterval(function() {
    console.log("Flow Timer...")
    workTime--;
    if (workTime < 0) {
    alert("Great job! You're done");
    // alert = require('alert')
    // alert() // Plays default alert "bottle"
    // alert.volume(0.5)
      clearInterval(timer);
      $('#saveEntry').show();
      $('#checkbox').show();
      // alert("You're done!");
      $('#myAlert').show();
      $('#work').show();
      // $('#label').show();
      // $alert('purr')
      // alert = require('alert')

      // $('#myAlert-fail').hide()
      // $('#result').show();
    } else {
      showTime(workTime);
    }
  }, 1000);
}
  //End Timer
  //What Happens when #start is pressed
 function start() {     
   if (working == true){ //This keeps it from being spammable
      return
   } //Else
  workTime = $('#work').val()*60;
    // breakTime = $('#break').val()*60;
   working = true;
   $('#myAlert').hide();
   $('#start').hide();
   $('.page-header').hide();
   $('#work').hide();
   $('#work').hide();
   // $('#label').hide();
   // $('#myAlert-fail').hide()
   // $('#result').show();
   checkStatus();    
    timer = startTimer();
 } 
  
  
  //What Happens when #pause/resume is pressed
  function pause() {
    clearInterval(timer);
    $('.resume').unbind().click(resume);
    $('#pause').html('Resume');
    $('#pause').addClass('resume');
    $('#pause').removeClass('pause');
    $('.resume').click(resume);
    $('#saveEntry').show();
    $('#checkbox').show();
    $('#myAlert').hide();
    $('#start').hide();
    $('.page-header').hide();
    // $('#work').hide();
    // $('#myAlert-fail').hide()
    // $('#result').show();
   }
  
  function resume(){  
    $('#pause').unbind().click(pause);
    $('#pause').html('Pause');
    $('#pause').addClass('pause');
    $('#pause').removeClass('resume');
    $('#saveEntry').hide();
    $('#checkbox').show();
    timer = startTimer();
    $('#myAlert').hide();
    $('#start').hide();
    $('.page-header').hide();
    // $('#work').hide();
    // $('#myAlert-fail').hide()
    // $('#result').show();
    }
  //What happens when #reset is pressed
  function reset() {
   clearInterval(timer);
    working = false;
    workTime = 25;
    // breakTime = 0;
    checkStatus();
    // $('.jumbotron').css('visibility', 'hidden');
    $('#msg').html("");
    $('#myAlert').hide();
    $('#start').show();
    $('.page-header').hide();
    $('#work').show();
    // $('#pause').html('Resume');
    // $('#pause').addClass('resume');
    // $('#pause').removeClass('pause');
    // $('#label').show();
    // $('#myAlert-fail').hide()
    // $('#result').hide();
  }
  //Break Timer
//   function breakTimer() {
//     $('.jumbotron').css('visibility', 'visible');
//     return setInterval(function() {
//       console.log("Break Timer...");
//     breakTime--;
//     if (breakTime < 0) {
//       clearInterval(timer);
//       working = false;
//       start();
//     } else {
//       showTime(breakTime);
//     }
//   }, 1000);
// }
  //Button Association
  $('#start').click(start);
    $('#work').keypress(function(e) {
    if(e.which == 13) {
       start();
    }
});
  //This Makes Enter Work as well to Start
  $('.pause').click(pause);
  $('#reset').click(reset); 
  
}); //End of DocReady

    function displayOutput() {
         var input = document.getElementById("userInput").value;
         if (input.length === 0) {
                flash("Please enter a valid input");
                return;
            }
         document.getElementById("result").innerHTML = "Current block: " + input;
        }


// ORIGINAL TIMER START

// $( document ).ready(function() {
// $('button').on('click', function() {
// var message = $('#flowNow').val().substring();
// //   $('<span><h2>Here is what you are working on!</h2></span>');
//   $('#flowNow').remove();
//   // $('#hiddenDiv2').append('<h2>In progress: </h2>' + message);
// //   $('.flowNow').remove('#time');
// //   $('button').remove();
 
  
// });
// });

// //timer function
// $('#startButton').on('click', function() {
// // var message = $('#flowNow').val().substring();
// function startTimer(duration, display) {
//     var timer = duration, minutes, seconds;
//     setInterval(function () {
//         minutes = parseInt(timer / 60, 10)
//         seconds = parseInt(timer % 60, 10);

//         minutes = minutes < 10 ? "0" + minutes : minutes;
//         seconds = seconds < 10 ? "0" + seconds : seconds;

//         display.text(minutes + ":" + seconds);

//         if (--timer < 0) {
//             timer = alert("Great job! You're done");
//         }
//     }, 1000);
// }

// $('#stop').on('click', function() {
// // var message = $('#flowNow').val().substring();
// function stopTimer(duration, display) {
//     var timer = duration, minutes, seconds;
//     setInterval(function () {
//         minutes = parseInt(timer / 60, 10)
//         seconds = parseInt(timer % 60, 10);

//         minutes = minutes < 10 ? "0" + minutes : minutes;
//         seconds = seconds < 10 ? "0" + seconds : seconds;

//         display.text(minutes + ":" + seconds);

//         if (--timer < 0) {
//             timer = alert("Great job! You're done");
//         }
//     }, 1000);
// }

// $(function ($) {
//     var twentyFiveMinutes = 60 * 25,
//         display = $('#time');
//     startTimer(twentyFiveMinutes, display);
// });
// });

// ORIGINAL TIMER START

//New as of July 2015 - based on http://codepen.io/anon/pen/pJammE

// function _timer(callback)
// {
//     var time = 25;     //  The default time of the timer
//     var mode = 0;     //    Mode: count up or count down
//     var status = 0;    //    Status: timer is running or stoped
//     var timer_id;    //    This is used by setInterval function
    
//     // this will start the timer ex. start the timer with 1 second interval timer.start(1000) 
//     this.start = function(interval)
//     {
//         interval = (typeof(interval) !== 'undefined') ? interval : 1000;
 
//         if(status == 0)
//         {
//             status = 1;
//             timer_id = setInterval(function()
//             {
//                 switch(mode)
//                 {
//                     default:
//                     if(time)
//                     {
//                         time--;
//                         generateTime();
//                         if(typeof(callback) === 'function') callback(time);
//                     }
//                     break;
                    
//                     case 1:
//                     if(time < 86400)
//                     {
//                         time++;
//                         generateTime();
//                         if(typeof(callback) === 'function') callback(time);
//                     }
//                     break;
//                 }
//             }, interval);
//         }
//     }
    
//     //  Same as the name, this will stop or pause the timer ex. timer.stop()
//     this.stop =  function()
//     {
//         if(status == 1)
//         {
//             status = 0;
//             clearInterval(timer_id);
//         }
//     }
    
//     // Reset the timer to zero or reset it to your own custom time ex. reset to zero second timer.reset(0)
//     this.reset =  function(sec)
//     {
//         sec = (typeof(sec) !== 'undefined') ? sec : 0;
//         time = sec;
//         generateTime(time);
//     }
    
//     // Change the mode of the timer, count-up (1) or countdown (0)
//     this.mode = function(tmode)
//     {
//         mode = tmode;
//     }
    
//     // This methode return the current value of the timer
//     this.getTime = function()
//     {
//         return time;
//     }
    
//     // This methode return the current mode of the timer count-up (1) or countdown (0)
//     this.getMode = function()
//     {
//         return mode;
//     }
    
//     // This methode return the status of the timer running (1) or stoped (1)
//     this.getStatus
//     {
//         return status;
//     }
    
//     // This methode will render the time variable to hour:minute:second format
//     function generateTime()
//     {
//         var second = time % 60;
//         var minute = Math.floor(time / 60) % 60;
//         var hour = Math.floor(time / 3600) % 60;
        
//         second = (second < 10) ? '0'+second : second;
//         minute = (minute < 10) ? '0'+minute : minute;
//         hour = (hour < 10) ? '0'+hour : hour;
        
//         $('div.timer span.second').html(second);
//         $('div.timer span.minute').html(minute);
//         $('div.timer span.hour').html(hour);
//     }
// }
 
// // example use
// var timer;
 
// $(document).ready(function(e) 
// {
//     timer = new _timer
//     (
//         function(time)
//         {
//             if(time == 0)
//             {
//                 timer.stop();
//                 alert('time out');
//             }
//         }
//     );
//     timer.reset(0);
//     timer.mode(0);
// });

// $( "#target" ).submit(function( event ) {
//   var message = $('<span><h2>test copy for dynamic div!</h2></span>');
// $('#hiddenDiv').append(message);
//   event.preventDefault();
// });

// function timer()
// {
//   count=count-1;
//   if (count <= 0)
//   {
//      clearInterval(counter);
//      return;
//   }

//  document.getElementById("timer").innerHTML=count + " secs"; // watch for spelling
// }
// <!-- javascript tutorial -->




// var shoppingList = [
//  'carrots', 
//  'oranges',
//  ]

// console.log(shoppingList[0]);

// var html = '';

// for ( var i = 1; i <= 10; i += 1) {
//  html += <'div>' + i + '</div';
// }
// document.write(html);



// var upper = 10000;
// var randomNumber = getRandomNumber(upper);
// var attempts = 0;

// function getRandomNumber(upper) {
//     return Math.floor( Math.random() * upper ) + 1;
// }

// while ( guess !== randomNumber ) {
//  guess = getRandomNumber( upper );
//  attempts += 1;
// }
// document.write("<p>The random number was: " + rnadomNumber + "<p>");
// document.write("<p>It took the computer: " + " attempts to get it right.</p>");


// do while example
// var randomNumber = getRandomNumber(upper);
// var guess;
// var guessCount = 0;
// var correctGuess = false;

// function getRandomNumber( upper ) {
//  var num = Math.floor(Math.random() * upper) + 1;
//  return num;
// // }

// do {
//  guess = prompt('I am thinking of a number between 1 and 10. What is it?');
//  guessCount += 1;
//  if (parseInt(guess) === randomNumber) {
//      correctGuess = true;
//  }
// } while ( ! correctGuess)
// document.write('<h1>You guessed the number!</h1>');
// document.write('It took you ' + guessCount + ' tries' + randomNumber);


// while ( guessCount < 10 ) {
//  guess = prompt('I am thinking of a number between 1 and 10. What is it?');
//  guessCount += 1;
//  if (parseInt(guess) === randomNumber) {
//      correctGuess = true;
//  break
//  }
// } 
// if (correctGuess) {
// document.write('<h1>You guessed the number!</h1>');
// document.write('It took you ' + guessCount + ' tries' + randomNumber);
// }


// // // Calculate quarters remaining in life:
// // // var currentAge = 38;
// // // var lifeExpectancy = 
// // // var remaining = 

// // // var counter = 0;
// // // while ( counter < 100) {
// //     var randNum = randomNumber(6);
// //     document.write(randNum + ' ');
// //     counter += 1;
// // }

// for (var i = 0; i < 10; i +=1 ){
//  document.write( counter );
// }



// if () {
//     alert( "Hey I know you")
// }

// while () {
    
// }



// $('#exampleModal').on('show.bs.modal', function (event) {
//   var button = $(event.relatedTarget) // Button that triggered the modal
//   var recipient = button.data('whatever') // Extract info from data-* attributes
//   // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
//   // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
//   var modal = $(this)
//   modal.find('.modal-title').text('New message to ' + recipient)
//   modal.find('.modal-body input').val(recipient)
// })


// $("#exampleModal").submit(function(){
//  alert("i've submitted this form");
// });


// var html = '';

// for ( var i = 1; i <= 10; i += 1) {
//  html += <'div>' + i + '</div';
// }
// document.write(html);



// var upper = 10000;
// var randomNumber = getRandomNumber(upper);
// var attempts = 0;

// function getRandomNumber(upper) {
//     return Math.floor( Math.random() * upper ) + 1;
// }

// while ( guess !== randomNumber ) {
//  guess = getRandomNumber( upper );
//  attempts += 1;
// }
// document.write("<p>The random number was: " + rnadomNumber + "<p>");
// document.write("<p>It took the computer: " + " attempts to get it right.</p>");


// do while example
// var randomNumber = getRandomNumber(upper);
// var guess;
// var guessCount = 0;
// var correctGuess = false;

// function getRandomNumber( upper ) {
//  var num = Math.floor(Math.random() * upper) + 1;
//  return num;
// }

// do {
//  guess = prompt('I am thinking of a number between 1 and 10. What is it?');
//  guessCount += 1;
//  if (parseInt(guess) === randomNumber) {
//      correctGuess = true;
//  }
// } while ( ! correctGuess)
// document.write('<h1>You guessed the number!</h1>');
// document.write('It took you ' + guessCount + ' tries' + randomNumber);

// // Calculate quarters remaining in life:
// // var currentAge = 38;
// // var lifeExpectancy = 
// // var remaining = 

// // var counter = 0;
// // while ( counter < 100) {
// //     var randNum = randomNumber(6);
// //     document.write(randNum + ' ');
// //     counter += 1;
// // }

// for (var i = 0; i < 10; i +=1 ){
//  document.write( counter );
// }



// if () {
//     alert( "Hey I know you")
// }

// while () {
    
// }