var timeoutId = null;
var delayTime = 5;
/**
 * This function displays a floating message to inform the user about
 * an event that either occurred, succeeded or failed.
 *
 * @param {Number} message: The message to display.
 * @param {Number} delay: The optional time the message will delay on screen.
 * @param {String} type: The type of format the message will get.
 */
var openMessage = function(message, delay, type) {
  if(!delay) {
    delay = delayTime;
  }
  if(!type) {
    type = 'info';
  }
  $('#agile-error-message, #agile-icon').removeClass()
      .addClass('agile-' + type + '-message');
  $('#agile-message').html(message);
  $('#agile-error-message').fadeIn();
  timeoutId = setTimeout(closeMessage, delay * 1000);
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
 * This function displays a message indicating something may happen happened.
 *
 * @param {Number} message: The message to display.
 * @param {Number} delay: The optional time the message will delay on screen.
 */
var showWarningMessage = function(message, delay) {
  openMessage(message, delay, 'warning');
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
  $('#agile-error-message').fadeOut();
  $('#agile-message').html('');
}


$(function() {
  $('#agile-close-message').live('click', closeMessage);

  $('#agile-error-message').mouseover(function() {
    clearTimeout(timeoutId);
  });

  $('#agile-error-message').mouseout(function() {
    timeoutId = setTimeout(closeMessage, delayTime * 1000);
  });
});
