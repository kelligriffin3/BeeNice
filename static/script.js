function postComment() {
    var commentInput = document.getElementById("commentInput").value;
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/add_comment", true);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.send(JSON.stringify({ comment: commentInput }));
    xhr.onload = function () {
      if (xhr.status === 200) {
        location.reload(); // Reload the page to display updated comments
      }
    };
  }

function clearComments() {
    var xhr = new XMLHttpRequest();
    xhr.open("DELETE", "/clear_comments", true);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.send(JSON.stringify({ comment: "clear" }));
    xhr.onload = function () {
      if (xhr.status === 200) {
        location.reload(); // Reload the page to display updated comments
      }
    };
  }

function summarizeComments() {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/summarize_comments", true);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.send(JSON.stringify({ comment: "summarize" }));
    xhr.onload = function () {
      if (xhr.status === 200) {
        location.reload(); // Reload the page to display the summary
      }
    };
  }

  document.addEventListener('DOMContentLoaded', function () {
    // Get the slider element
    var slider = document.getElementById('sentimentSlider');
    // Get the display element
    var display = document.getElementById('sliderValueDisplay');

    // Update the display initially
    display.textContent = slider.value;

    // Add event listener for input event
    slider.addEventListener('input', function () {
        // Update the display with the current slider value
        display.textContent = slider.value;
    });
});

