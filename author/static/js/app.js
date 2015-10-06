  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
  }

  function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }


$(function() { // dom is ready

  /* toggle the password from cleartext to obscured */

  $(".pwd-toggle").click(function() {
    $('#password').togglePassword();
    $('.pwd-toggle span').html($('.pwd-toggle span').text() === 'Show' ?
      'Hide' : 'Show');
    $('.fa-eye, .fa-eye-slash').toggleClass("fa-eye fa-eye-slash");
  });

  /* set class based on correct/incorrect sign in */

  $("#dosignin").submit(function(event) {
    event.preventDefault();
    $.post('/login/', $('#dosignin').serialize(), function(response) {
      if (response.errors) {
        $('.pwd-container label').addClass("wrong");
        $('#password').val("")
        $('.signin-error').fadeIn();
        setTimeout(function() {
          $('.pwd-container label').removeClass("wrong");
          $('.signin-error').fadeOut();
          $('#password').focus();
        }, 4000);
      } else {
        $('.pwd-container').addClass("correct");
        setTimeout(function() {
          $('.pwd-container').removeClass("correct");
          window.location=response.success;
        }, 1000);
      }
    });

  });

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

 // $("#id_title, #id_questionnaire-id, #id_overview").blur(function() {
 //   if ($("#id_title").val() !== "" && $("#id_questionnaire_id").val() !==
 //    "" && $(
 //      "#id_overview").val() !== "") {
 //   $('#dosetup').prop("disabled", false);
 // } else {
 //     $('#dosetup').prop("disabled", true);
 //   }
 //});

 //$(".user-prompt").click(function() {
 //  if ($('#dosetup').prop("disabled") === true) {
 //   alert('Make sure all fields are complete');
 //  }
 // });

  /* add form inputs to the canvas */

  $(".add-text-field").click(function() {
    $.get('/static/form-snippets/text.html', function(data) {
      $(".question-container").slideUp();
      $(".question-list").append(data).hide().fadeIn(1000);
    }, 'text');

    if ($(".question")) {
      $(".splash").fadeOut();
      $(".form-canvas").addClass("active");
    } else if (!$(".question")) {
      $(".splash").fadeIn();
    }

  });

  /* drag/drop add to canvas */

  $(".q-types li:first-child").draggable({ /* just first one for now */
    opacity: 0.7,
    helper: "clone"
  });


  $(".form-canvas").droppable({
    hoverClass: "highlight",
    accept: ".q-types li",
    drop: function() {
      $.get('/static/form-snippets/text.html', function(data) {
        $(".question-container").slideUp();
        $(".question-list").append(data).hide().fadeIn(1000);
      }, 'text');
      if ($(".question")) {
        $(".splash").fadeOut();
        $(".form-canvas").addClass("active");
      } else if (!$(".question")) {
        $(".splash").fadeIn();
      }
    }

  });

  /* remove a question from the canvas */

  $("body").on("click", ".close", function() {
    $(this).closest(".question").fadeOut();
  });

  /* remove a question from the canvas */

  $(".reset").click(function() {
    if (confirm('Are you sure you want to remove all questions?')) {
      $(".question").remove();
    }
  });

  /* duplicate a question */

  $("body").on("click", ".duplicate", function() {
    $(this).closest(".question").clone().insertBefore($(this).closest(
      ".question"));
  });

  /* take the content from the RTE and mirror in textarea for form submission */

  $("#q-intro").html($(".q-intro").html());

  $("body").on("keyup, keydown, focus", ".q-intro", function() {
    var introtxt = $(".q-intro").html();
    $("#q-intro").html(introtxt);
  });

  $(".clear").click(function() {
    $("#q-intro, .q-intro").html($(".q-intro").text());
  });


  /* max/minimise a question */

  $("body").on("click", ".question-toolbar", function() {
    $(this).closest(".question").find(".question-container").slideToggle();
  });

  /* make the questions re-orderable */

  $(".question-list").sortable().disableSelection();

  // set the title of the toolbar

  $("body").on("keyup", "#q-title-auth", function() {
    var keyed = $(this).val();
    $(this).closest(".question").find(".order").text(keyed);
  });

  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
  });

});
