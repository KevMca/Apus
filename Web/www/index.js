// ---------------------------------------------------------------------------
// index.js
// 
// Author: Kevin McAndrew
// Created: 4 Aug 2020
// ---------------------------------------------------------------------------

// ---------------------------------------------------------------------------
// Create PID card
// ---------------------------------------------------------------------------
const pid_card = document.getElementById("pid_card");
// Fetch JSON data
let jsonData;
fetch('pid.json')
  .then(response => response.json())
  .then(data => appendPID(data));

function appendPID(data){
  jsonData = data;
  // -------------------------------------------------------------------------
  // -- Axis container
  data.forEach((element) => {
    // -----------------------------------------------------------------------
    // -- Title
    const title = `<br><p class="text--bold"> ${element["name"]}</p><br>`;
    const titleDiv = document.createElement("div");
    titleDiv.innerHTML = title;
    pid_card.appendChild(titleDiv);
    
    // -----------------------------------------------------------------------
    // -- Input and increment buttons
    for (var key in element["data"]) {
      // Markup
      const paramMarkup = 
        `<div class="property-container">
          <label class="text--medium" style="display:inline-block; width:10%;">
            ${key} </label>
          <input class="card_input" type="text" value=${element["data"][key]} 
            id="${element["name"]}_${key}">
          <button class="button_up text--bold" type="increment" 
            id="${element["name"]}_${key}_up"> ∧ </button>
          <button class="button_down text--bold" type="increment" 
            id="${element["name"]}_${key}_down"> ∨ </button>
        </div>`;

      // Create element
      const paramDiv = document.createElement("div");
      paramDiv.innerHTML = paramMarkup
      pid_card.appendChild(paramDiv);
    }
  })
  // -------------------------------------------------------------------------
  // -- Submit button
  const submit = 
    `<button class="text--bold" type="submit" id="submit">Submit</button>`;
  const submitDiv = document.createElement("div");
  submitDiv.style = "text-align: center;";
  submitDiv.innerHTML = submit;
  pid_card.appendChild(submitDiv);
}

// ---------------------------------------------------------------------------
// Event listeners after the window has loaded
// ---------------------------------------------------------------------------
window.onload = function(){
  
  // -------------------------------------------------------------------------
  // Submit button listener
  document.getElementById("submit").addEventListener("click", function() {
    // Read each of the text boxes
    jsonData.forEach((element) => {
      for (var key in element["data"]) {
        element["data"][key] = 
          document.getElementById(element["name"]+"_"+key).value;
      }
    })
    console.log(jsonData);

    // POST the JSON file to the server
    fetch("/pid", {
      method: "post",
      headers: {
        'Content-Type': 'application/json'
      },
      //make sure to serialize your JSON body
      body: JSON.stringify(jsonData)
    })
  });
  
  // -------------------------------------------------------------------------
  // Button listeners
  // Used to increment the text boxes up and down
  jsonData.forEach((element) => {
    for (var key in element["data"]) {
      const butName = element["name"] + "_" + key;
      document.getElementById(butName + "_up").addEventListener("click", function() {
        const textBox = document.getElementById(butName);
        textBox.value = (parseFloat(textBox.value) + 1).toString();
      });
      document.getElementById(butName + "_down").addEventListener("click", function() {
        const textBox = document.getElementById(butName);
        textBox.value = (parseFloat(textBox.value) - 1).toString();
      });
    }
  })
}
