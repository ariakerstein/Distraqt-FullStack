


var timer;

$(document).ready(function(){
var working = false;
var active = '';
var workTime =0;
var breakTime = 0;
checkStatus();


  //Controls if a button is disabled based on status of timer
function checkStatus() {
  if (!working) {
    $('#start').removeClass('disabled');
    $('#pause').addClass('disabled');
    $('#reset').addClass('disabled');
    $('#myAlert').hide();
    $('#work').show();
    $('#saveEntry').addClass('disabled');
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
    $('#saveEntry').removeClass('disabled');
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
      $('#saveEntry').addClass('disabled');
      $('#checkbox').show();
      // alert("You're done!");
      $('#myAlert').show();
      $('#work').show();
      $('#saveEntry').removeClass('disabled');
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
    $('#saveEntry').removeClass('disabled');
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
    // $('#saveEntry').addClass('disabled');
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
    $('#saveEntry').addClass('disabled');


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

