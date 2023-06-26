
$(document).on("click", function(e) {
  if (!$(e.target).closest(".container").length) {
    $("ul").removeClass("open");
  }
});

$("i").click(function() {
  $("ul").toggleClass("open");
});

