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
const autre_card = document.getElementById("autre_card");
// Fetch JSON data
let pidData;
let autreData;
fetch('pid.json')
  .then(response => response.json())
  .then(data => appendPID(data));
fetch('autre.json')
  .then(response => response.json())
  .then(data => appendAutre(data));

function appendPID(data){
  console.log(data);
  pidData = data;
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
      const paramMarkup = inputMarkup(key, element["data"][key], 
                                      element["name"]+"_"+key);

      // Create element
      const paramDiv = document.createElement("div");
      paramDiv.innerHTML = paramMarkup
      pid_card.appendChild(paramDiv);
    }
  })
  // -------------------------------------------------------------------------
  // -- Submit button
  const submit = 
    `<br><button class="text--bold" type="submit" id="submit_pid">Submit</button>`;
  const submitDiv = document.createElement("div");
  submitDiv.style = "text-align: center;";
  submitDiv.innerHTML = submit;
  pid_card.appendChild(submitDiv);

  // -- Load listeners
  loadListenersPid(data);
}

function appendAutre(data){
  console.log(data);
  autreData = data;
  // -------------------------------------------------------------------------
  // -- Axis container
  data.forEach((element) => {
    // -----------------------------------------------------------------------
    // -- Title
    const title = `<br><p class="text--bold"> ${element["name"]}</p><br>`;
    const titleDiv = document.createElement("div");
    titleDiv.innerHTML = title;
    autre_card.appendChild(titleDiv);
    
    // -----------------------------------------------------------------------
    // -- Input and increment buttons
    for (var key in element["data"]) {
      // Markup
      const paramMarkup = inputMarkup(key, element["data"][key], 
                                      element["name"]+"_"+key);

      // Create element
      const paramDiv = document.createElement("div");
      paramDiv.innerHTML = paramMarkup
      autre_card.appendChild(paramDiv);
    }
  })
  // -------------------------------------------------------------------------
  // -- Submit button
  const submit = 
    `<br><button style="background-color: #5ca8ff;" class="text--bold" type="submit" id="submit_autre">Submit</button>`;
  const submitDiv = document.createElement("div");
  submitDiv.style = "text-align: center;";
  submitDiv.innerHTML = submit;
  autre_card.appendChild(submitDiv);

  // -- Load listeners
  loadListenersAutre(data);
}

function inputMarkup(label, value, id){
  return `<div class="property-container">
            <label class="text--medium" style="display:inline-block; width:10%;">
              ${label} </label>
            <input class="card_input" type="text" value=${value} 
              id="${id}">
            <button class="button_up text--bold" type="increment" 
              id="${id}_up"> ∧ </button>
            <button class="button_down text--bold" type="increment" 
              id="${id}_down"> ∨ </button>
          </div>`;
}

// ---------------------------------------------------------------------------
// Event listeners after the window has loaded
// ---------------------------------------------------------------------------
function loadListenersPid(data){
  
  // -------------------------------------------------------------------------
  // Button listeners
  // Used to increment the text boxes up and down
  pidData.forEach((element) => {
    for (var key in element["data"]) {
      const butName = element["name"] + "_" + key;
      document.getElementById(butName + "_up").addEventListener("click", function() {
        const textBox = document.getElementById(butName);
        let floatVal = parseFloat(textBox.value) + 0.1;
        floatVal = floatVal.toPrecision(5);
        textBox.value = floatVal.toString();
      });
      document.getElementById(butName + "_down").addEventListener("click", function() {
        const textBox = document.getElementById(butName);
        let floatVal = parseFloat(textBox.value) - 0.1;
        floatVal = floatVal.toPrecision(5);
        textBox.value = floatVal.toString();
      });
    }
  })

  // -------------------------------------------------------------------------
  // Submit button listener
  document.getElementById("submit_pid").addEventListener("click", function() {
    // Read each of the text boxes
    pidData.forEach((element) => {
      for (var key in element["data"]) {
        element["data"][key] = 
          document.getElementById(element["name"]+"_"+key).value;
      }
    })
    console.log(pidData);

    // POST the JSON file to the server
    fetch("/pid", {
      method: "post",
      headers: {
        'Content-Type': 'application/json'
      },
      //make sure to serialize your JSON body
      body: JSON.stringify(pidData)
    })
  });
}

// ---------------------------------------------------------------------------
// Event listeners after the window has loaded
// ---------------------------------------------------------------------------
function loadListenersAutre(data){
  
  // -------------------------------------------------------------------------
  // Button listeners
  // Used to increment the text boxes up and down
  autreData.forEach((element) => {
    for (var key in element["data"]) {
      const butName = element["name"] + "_" + key;
      document.getElementById(butName + "_up").addEventListener("click", function() {
        const textBox = document.getElementById(butName);
        let floatVal = parseFloat(textBox.value) + 0.1;
        floatVal = floatVal.toPrecision(5);
        textBox.value = floatVal.toString();
      });
      document.getElementById(butName + "_down").addEventListener("click", function() {
        const textBox = document.getElementById(butName);
        let floatVal = parseFloat(textBox.value) - 0.1;
        floatVal = floatVal.toPrecision(5);
        textBox.value = floatVal.toString();
      });
    }
  })

  // -------------------------------------------------------------------------
  // Submit button listener
  document.getElementById("submit_autre").addEventListener("click", function() {
    // Read each of the text boxes
    autreData.forEach((element) => {
      for (var key in element["data"]) {
        element["data"][key] = 
          document.getElementById(element["name"]+"_"+key).value;
      }
    })
    console.log(autreData);

    // POST the JSON file to the server
    fetch("/autre", {
      method: "post",
      headers: {
        'Content-Type': 'application/json'
      },
      //make sure to serialize your JSON body
      body: JSON.stringify(autreData)
    })
  });
}
