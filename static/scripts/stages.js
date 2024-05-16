// Get the modal
var modal = document.getElementById("myModal");

// Get the button that opens the modal
var btn = document.getElementById("openModal");

// Get the element to close the modal
var span = document.getElementsByClassName("close")[0];

// Function to open the modal
btn.onclick = function() {
  modal.style.display = "block";
}

// Function to close the modal
span.onclick = function() {
  modal.style.display = "none";
}

// Close the modal when the user clicks outside of it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}

// Get the close button inside the modal
var closeButton = document.getElementById("closeModal");

// Function to close the modal when the button is clicked
closeButton.onclick = function() {
  modal.style.display = "none";
}

// Close the modal initially
modal.style.display = "none";
