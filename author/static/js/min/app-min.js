$(function(){$(".pwd-toggle").click(function(){$("#password").togglePassword(),$(".pwd-toggle span").html("Show"===$(".pwd-toggle span").text()?"Hide":"Show"),$(".fa-eye, .fa-eye-slash").toggleClass("fa-eye fa-eye-slash")}),$("header ul.user-menu").click(function(){$(".user-settings, header ul.user-menu").toggleClass("open")}),$("#surveylist").change(function(){""!==$("#surveylist").val()?$("#dosetup").prop("disabled",!1):$("#dosetup").prop("disabled",!0)}),$("#q-title, #q-id, #q-overview").blur(function(){""!==$("#q-title").val()&&""!==$("#q-id").val()&&""!==$("#q-overview").val()?$("#dosetup").prop("disabled",!1):$("#dosetup").prop("disabled",!0)}),$(".user-prompt").click(function(){$("#dosetup").prop("disabled")===!0&&alert("Make sure all fields are complete")}),$(".add-text-field").click(function(){$.get("/static/form-snippets/text.html",function(e){$(".question-container").slideUp(),$(".question-list").append(e).hide().fadeIn(1e3)},"text"),$(".question")?($(".splash").fadeOut(),$(".form-canvas").addClass("active")):$(".question")||$(".splash").fadeIn()}),$("body").on("click",".close",function(){$(this).closest(".question").fadeOut()}),$("body").on("click",".duplicate",function(){$(this).closest(".question").clone().insertBefore($(this).closest(".question"))}),$("#q-intro").html($(".q-intro").html()),$("body").on("keyup, keydown, focus",".q-intro",function(){var e=$(".q-intro").html();$("#q-intro").html(e)}),$(".clear").click(function(){$("#q-intro, .q-intro").html($(".q-intro").text())}),$("body").on("click",".question-toolbar",function(){$(this).closest(".question").find(".question-container").slideToggle()}),$(".question-list").sortable().disableSelection(),$("body").on("keyup","#q-title-auth",function(){var e=$(this).val();$(this).closest(".question").find(".order").text(e)})});