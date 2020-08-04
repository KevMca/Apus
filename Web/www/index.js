const pid_card = document.getElementById("pid_card");
var names = ["Pitch", "Roll", "Yaw"];
fetch('pid.json')
    .then(response => response.json())
    .then(data => appendPID(data));

function appendPID(data){
    console.log(data);
    // Run for pitch, roll and yaw
    for (var i = 0; i < data.length; i++) {
        var _br = document.createElement("br");
        // Title
        var title = document.createElement("p");
        title.class = "text--bold";
        title.innerHTML = names[i];
        // Labels
        var label_prop = document.createElement("label");
        label_prop.style = "display:inline-block; width:10%;";
        label_prop.class = "text--medium";
        var label_integ = label_prop.cloneNode(true);
        var label_deriv = label_prop.cloneNode(true);
        label_prop.innerHTML = "P";
        label_integ.innerHTML = "I";
        label_deriv.innerHTML = "D";
        // Inputs
        var prop = document.createElement("input");
        prop.type = "text";
        prop.class = "card_input";
        var integ = prop.cloneNode(true);
        var deriv = prop.cloneNode(true);
        prop.id = names[i] + "_p";
        integ.id = names[i] + "_i";
        deriv.id = names[i] + "_d";
        prop.value = data[i].p;
        integ.value = data[i].i;
        deriv.value = data[i].d;
        // Increments
        var prop_up = document.createElement("button");
        prop_up.type = "increment";
        prop_up.className = "button_up text--bold";
        prop_up.innerHTML = "∧";
        var prop_down = prop_up.cloneNode(true);
        prop_down.className = "button_down text--bold";
        prop_down.innerHTML = "∨";
        var integ_up = prop_up.cloneNode(true);
        var integ_down = prop_down.cloneNode(true);
        var deriv_up = prop_up.cloneNode(true);
        var deriv_down = prop_down.cloneNode(true);
        prop_up.id = names[i] + "_but_p_up";
        prop_down.id = names[i] + "_but_p_d";
        integ_up.id = names[i] + "_but_i_up";
        integ_down.id = names[i] + "_but_i_d";
        deriv_up.id = names[i] + "_but_d_up";
        deriv_down.id = names[i] + "_but_d_d";

        // Assign values to inputs
        pid_card.appendChild(_br.cloneNode(true));
        pid_card.appendChild(title);
        pid_card.appendChild(_br.cloneNode(true));

        pid_card.appendChild(label_prop);
        pid_card.appendChild(prop);
        pid_card.appendChild(prop_up.cloneNode(true));
        pid_card.appendChild(prop_down.cloneNode(true));
        pid_card.appendChild(_br.cloneNode(true));

        pid_card.appendChild(label_integ);
        pid_card.appendChild(integ);
        pid_card.appendChild(integ_up.cloneNode(true));
        pid_card.appendChild(integ_down.cloneNode(true));
        pid_card.appendChild(_br.cloneNode(true));

        pid_card.appendChild(label_deriv);
        pid_card.appendChild(deriv);
        pid_card.appendChild(deriv_up.cloneNode(true));
        pid_card.appendChild(deriv_down.cloneNode(true));

        pid_card.appendChild(_br.cloneNode(true));
    }
    var submit = document.createElement("button");
    submit.className = "text--bold";
    submit.type = "submit";
    submit.innerHTML = "Submit";
    submit.id = "submit_btn";
    var submit_contain = document.createElement("div");
    submit_contain.style = "text-align: center;";
    submit_contain.appendChild(submit);
    pid_card.appendChild(_br.cloneNode(true));
    pid_card.appendChild(submit_contain);
}
window.onload = function(){
    // Submit button listener
    // Should read all of the text boxes and save to pid.json
    document.getElementById("submit_btn").addEventListener("click", function() {
        // Placeholder to test
        console.log(document.getElementById("Pitch_p").value);
    });
    for (var i = 0; i < names.length; i++) {
        // Button listeners
        // Used to increment the text boxes up and down
        /*document.getElementById("submit_btn").addEventListener("click", function() {
            console.log(document.getElementById(names[i] + "but_p_up").value);
        });*/
        // Input listeners
        
    }
}