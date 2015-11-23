(function() {
  angular.module("QBuilder", [
    'QBuilderConfig',
    'ngSanitize',
    'dndLists',
    'contenteditable',
    'ephox.textboxio',
    'tabs',
    'BuilderController',
    'ngAnimate',
    'confirmdialog',
    'textQuestion',
    'numberQuestion',
    'richTextQuestion',
    'questionGroup',
    'radioQuestion',
    'setfocus',
    'checkBoxQuestion',
    'dropdownQuestion'
  ]);

  // See config.js, and controllers/*.js
})();

// unlock the questionnaire if the user leaves the page - not ideal but hey
$(window).bind('beforeunload', function() {
  var unlock = JSON.stringify({
    unlock: "true"
  });
  $.ajax({
    url: window.location,
    data: unlock,
    contentType: 'application/json',
    type: 'POST'
  })
});
