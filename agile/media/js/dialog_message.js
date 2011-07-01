$(function() {
  
  /**
   * This function displays a floating message to inform the user about
   * an event that either occured, succeeded or failed.
   * 
   * @param {Number} message: The message to display.
   * @param {Number} delay: The optional time the message will delay on screen.
   * @param {String} type: The type of format the message will get.
   */
  var openMessage = function(message, delay, type) {
    if(typeof delay == undefined) {
      delay = 3;
    }
    if(typeof type == undefined) {
      type = 'info';
    }
    $('#agile-error-message').removeClass('agile*')
        .addClass('agile-'+type+'-message');
    $('#agile-message').html(message);
    $('#agile-error-message').fadeIn(800);
    setTimeout(closeMessage, delay*1000);
  }
  
  
  /**
   * This function displays a message indicating an action succeeded.
   * 
   * @param {Number} message: The message to display.
   * @param {Number} delay: The optional time the message will delay on screen.
   */
  var showSuccessMessage = function(message, delay) {
    openMessage(message, delay, 'success');
  }
  
  
  /**
   * This function displays a message indicating something happened.
   * 
   * @param {Number} message: The message to display.
   * @param {Number} delay: The optional time the message will delay on screen.
   */
  var showInformationMessage = function(message, delay) {
    openMessage(message, delay, 'info');
  }
  
  
  /**
   * This function displays a message indicating an action failed.
   * 
   * @param {Number} message: The message to display.
   * @param {Number} delay: The time the message will delay on screen.
   */
  var showErrorMessage = function(message, delay) {
    openMessage(message, delay, 'error');
  }
  
  
  /**
   * This function hides the floating message.
   */
  var closeMessage = function() {
    $('#agile-error-message').fadeOut(800);
    $('#agile-message').html('');
  }
});