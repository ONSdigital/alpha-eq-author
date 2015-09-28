$(function() { // dom is ready

  /* toggle the password from cleartext to obscured */

  $(".pwd-toggle").click(function() {
    $('#password').togglePassword();
    $('.pwd-toggle span').html($('.pwd-toggle span').text() === 'Show' ?
      'Hide' : 'Show');
    $('.fa-eye, .fa-eye-slash').toggleClass("fa-eye fa-eye-slash");
  });

  /* set class based on correct/incorrect sign in */

  //$("#dosignin").submit(function(event) {
  //  if ($('#password').val() !== "password") {
  //    $('.pwd-container label').addClass("wrong");
  //    $('.signin-error').fadeIn();
  //    setTimeout(function() {
  //      $('.pwd-container label').removeClass("wrong");
  //      $('.signin-error').fadeOut();
  //      $('#password').val("").focus();
  //    }, 4000);
  //    event.preventDefault();
  //  } else if ($('#password').val() === "password") {
  //    $('.pwd-container').addClass("correct");
  //    setTimeout(function() {
  //      $('.pwd-container').removeClass("correct");
  //    }, 4000);
  //  }
  //});

  /* user settings panel */

  $("header ul.user-menu").click(function() {
    $('.user-settings, header ul.user-menu').toggleClass("open");
  });

  /* create new survey check we have a survey selected */

  //$("#id_survey_list").change(function() {
  //  if ($("#id_survey_list").val() !== "") {
  //    $('#dosetup').prop("disabled", false);
  //  } else {
  //    $('#dosetup').prop("disabled", true);
  //  }
  //});

  $("#id_title, #id_questionnaire-id, #id_overview").blur(function() {
    if ($("#id_title").val() !== "" && $("#id_questionnaire_id").val() !== "" && $(
        "#id_overview").val() !== "") {
      $('#dosetup').prop("disabled", false);
    } else {
      $('#dosetup').prop("disabled", true);
    }
  });

  $(".user-prompt").click(function() {
    if ($('#dosetup').prop("disabled") === true) {
      alert('Make sure all fields are complete');
    }
  });



});
