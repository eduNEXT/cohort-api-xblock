/* Javascript for CohortAPIXblock.

   After successfully calling the JSONHandler `get_user_cohort` an event is emitted with
   the cohort information.

   For now, we provide:
    - cohort_name

   This can be accessed by listening to the event `cohort_obtained`.

*/
function CohortAPIXblock(runtime, element) {
  function successHandler(result) {
    var detail = result.cohort_name
      ? {
          cohort_name: result.cohort_name,
        }
      : {};
    var event = new CustomEvent("cohort_obtained", {
      detail: detail,
    });
    document.dispatchEvent(event);
  }

  var handlerUrl = runtime.handlerUrl(element, "get_user_cohort");

  /* Here's where you'd do things on page load. */
  $(function ($) {
    $.ajax({
      type: "POST",
      url: handlerUrl,
      data: JSON.stringify({}),
      success: successHandler,
    });
  });
}
