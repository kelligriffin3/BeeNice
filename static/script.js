// 
// Handlers for BeeNice.html
//
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

// Routes to settings page when button clicked
function goToSettings() {
    window.location.href = "/settings";
  };

//
// Handlers for Settings.html
//

// Event listener for when a slider element is changed
// Will continuously display the slider value
document.addEventListener('DOMContentLoaded', function () {
  // Get all slider elements
  var sliders = document.querySelectorAll('input[type="range"]');
  var checkboxes = document.querySelectorAll('input[type="checkbox"]');

  // Loop through each slider
  sliders.forEach(function (slider) {
      // Get the display element corresponding to the slider
      var display = slider.nextElementSibling;

      // Check if there's a saved value for this slider
      var savedValue = localStorage.getItem(slider.id);
      if (savedValue) {
          slider.value = savedValue;
          display.textContent = savedValue;
      }

      // Add event listener for input event
      slider.addEventListener('input', function () {
          // Update the display with the current slider value
          display.textContent = slider.value;
          // Save the value to localStorage
          localStorage.setItem(slider.id, slider.value);
      });
  });

  // Loop through each checkbox
  checkboxes.forEach(function (checkbox) {
      // Check if there's a saved state for this checkbox
      var savedState = localStorage.getItem(checkbox.id);
      if (savedState === 'true') {
          checkbox.checked = true;
      }

      // Add event listener for change event
      checkbox.addEventListener('change', function () {
          // Save the state to localStorage
          localStorage.setItem(checkbox.id, checkbox.checked);
      });
  });
});

function saveSettings() {
  var settings = {}; // Initialize an empty object to store settings

  // Get all checkboxes
  var checkboxes = document.querySelectorAll('input[type="checkbox"]');

  // Loop through each checkbox
  checkboxes.forEach(function (checkbox) {
      // If checkbox is checked, find the corresponding slider and get its value
      if (checkbox.checked) {
          var sliderId = checkbox.id.replace("Checkbox", "Slider");
          var slider = document.getElementById(sliderId);
          settings[checkbox.value] = slider.value;
      }
  });

  // You can perform additional operations with the 'settings' object here
  console.log(settings);

  // Save new settings to Flask
  var xhr = new XMLHttpRequest();
  xhr.open("POST", "/set_thresholds", true);
  xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
  xhr.send(JSON.stringify(settings));
  xhr.onreadystatechange = function() {
    if (xhr.readyState === XMLHttpRequest.DONE) {
      if (xhr.status !== 200) {
        //location.reload(); // Reload the page
        console.error('Failed to save settings');
      } else{
        console.log("Settings saved");
        var response = JSON.parse(xhr.responseText);
        console.log("Message:", response.message);
        console.log("New Threshold:", response.new_threshold);
        // Post message on screen letting user know about success
        document.getElementById('saveMessage').textContent = "Settings Saved!";
      }
    }
  }; 
}

// Routes back to home page when button clicked
function goHome() {
  window.location.href = "/";
};
