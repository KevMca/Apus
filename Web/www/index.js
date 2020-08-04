const pid_card = document.getElementById("pid_card");
let json_data;
fetch('pid.json')
    .then(response => response.json())
    .then(data => appendPID(data));

function appendPID(data){
    json_data = data;
    // -- Axis container
    data.forEach((element) => {
        // -- Title
        const title = `<br><p class="text--bold">${element["name"]}</p><br>`;
        const titleDiv = document.createElement("div");
        titleDiv.innerHTML = title;
        pid_card.appendChild(titleDiv);
        
        // -- Input and increment buttons
        for (var key in element["data"]) {
            // Markup
            const paramMarkup = 
                `<div class="property-container">
                    <label class="text--medium" style="display:inline-block; width:10%;">${key}</label>
                    <input class="card_input" type="text" value=${element["data"][key]}>
                    <button class="button_up text--bold" type="increment"> ∧ </button>
                    <button class="button_down text--bold" type="increment"> ∨ </button>
                </div>`;

            // Create element
            const paramDiv = document.createElement("div");
            paramDiv.innerHTML = paramMarkup
            pid_card.appendChild(paramDiv);
        }
    })
    // -- Submit button
    const submit = 
        `<button class="text--bold" type="submit">Submit</button>`;
    const submitDiv = document.createElement("div");
    submitDiv.style = "text-align: center;";
    submitDiv.innerHTML = submit;
    pid_card.appendChild(submitDiv);
}
// This is the bit that I'm currently working on
window.onload = function(){
    // Submit button listener
    // Should read all of the text boxes and save to pid.json
    document.getElementById("submit_btn").addEventListener("click", function() {
        // Placeholder to test
        json_data[0].p = document.getElementById("Pitch_p").value;
        json_data[0].i = document.getElementById("Pitch_i").value;
        json_data[0].d = document.getElementById("Pitch_d").value;
        json_data[1].p = document.getElementById("Roll_p").value;
        json_data[1].i = document.getElementById("Roll_i").value;
        json_data[1].d = document.getElementById("Roll_d").value;
        json_data[2].p = document.getElementById("Yaw_p").value;
        json_data[2].i = document.getElementById("Yaw_i").value;
        json_data[2].d = document.getElementById("Yaw_d").value;
        console.log(json_data);

        fetch("/pid", {
            method: "post",
            headers: {
                'Content-Type': 'application/json'
            },
            //make sure to serialize your JSON body
            body: JSON.stringify(json_data)
        })
    });
    
    // Button listeners
    // Used to increment the text boxes up and down
    
    document.getElementById("Pitch_but_p_up").addEventListener("click", function() {
        document.getElementById("Pitch_p").value = 
            (parseFloat(document.getElementById("Pitch_p").value) + 1).toString();
    });
    document.getElementById("Pitch_but_p_down").addEventListener("click", function() {
        document.getElementById("Pitch_p").value = 
            (parseFloat(document.getElementById("Pitch_p").value) - 1).toString();
    });
    document.getElementById("Pitch_but_i_up").addEventListener("click", function() {
        document.getElementById("Pitch_i").value = 
            (parseFloat(document.getElementById("Pitch_i").value) + 1).toString();
    });
    document.getElementById("Pitch_but_i_down").addEventListener("click", function() {
        document.getElementById("Pitch_i").value = 
            (parseFloat(document.getElementById("Pitch_i").value) - 1).toString();
    });
    document.getElementById("Pitch_but_d_up").addEventListener("click", function() {
        document.getElementById("Pitch_d").value = 
            (parseFloat(document.getElementById("Pitch_d").value) + 1).toString();
    });
    document.getElementById("Pitch_but_d_down").addEventListener("click", function() {
        document.getElementById("Pitch_d").value = 
            (parseFloat(document.getElementById("Pitch_d").value) - 1).toString();
    });

    document.getElementById("Roll_but_p_up").addEventListener("click", function() {
        document.getElementById("Roll_p").value = 
            (parseFloat(document.getElementById("Roll_p").value) + 1).toString();
    });
    document.getElementById("Roll_but_p_down").addEventListener("click", function() {
        document.getElementById("Roll_p").value = 
            (parseFloat(document.getElementById("Roll_p").value) - 1).toString();
    });
    document.getElementById("Roll_but_i_up").addEventListener("click", function() {
        document.getElementById("Roll_i").value = 
            (parseFloat(document.getElementById("Roll_i").value) + 1).toString();
    });
    document.getElementById("Roll_but_i_down").addEventListener("click", function() {
        document.getElementById("Roll_i").value = 
            (parseFloat(document.getElementById("Roll_i").value) - 1).toString();
    });
    document.getElementById("Roll_but_d_up").addEventListener("click", function() {
        document.getElementById("Roll_d").value = 
            (parseFloat(document.getElementById("Roll_d").value) + 1).toString();
    });
    document.getElementById("Roll_but_d_down").addEventListener("click", function() {
        document.getElementById("Roll_d").value = 
            (parseFloat(document.getElementById("Roll_d").value) - 1).toString();
    });

    document.getElementById("Yaw_but_p_up").addEventListener("click", function() {
        document.getElementById("Yaw_p").value = 
            (parseFloat(document.getElementById("Yaw_p").value) + 1).toString();
    });
    document.getElementById("Yaw_but_p_down").addEventListener("click", function() {
        document.getElementById("Yaw_p").value = 
            (parseFloat(document.getElementById("Yaw_p").value) - 1).toString();
    });
    document.getElementById("Yaw_but_i_up").addEventListener("click", function() {
        document.getElementById("Yaw_i").value = 
            (parseFloat(document.getElementById("Yaw_i").value) + 1).toString();
    });
    document.getElementById("Yaw_but_i_down").addEventListener("click", function() {
        document.getElementById("Yaw_i").value = 
            (parseFloat(document.getElementById("Yaw_i").value) - 1).toString();
    });
    document.getElementById("Yaw_but_d_up").addEventListener("click", function() {
        document.getElementById("Yaw_d").value = 
            (parseFloat(document.getElementById("Yaw_d").value) + 1).toString();
    });
    document.getElementById("Yaw_but_d_down").addEventListener("click", function() {
        document.getElementById("Yaw_d").value = 
            (parseFloat(document.getElementById("Yaw_d").value) - 1).toString();
    });
}