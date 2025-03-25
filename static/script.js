console.log("Username from localStorage:", localStorage.getItem("username"));

let button = document.querySelector("button");
let text = document.getElementById("text");
let reactionForm = document.getElementById("reactionForm")
let reactionTimeInput = document.getElementById("reactionTimeInput")
let state = "start";
let startTime;

function updateState(newState) {
    state = newState;
    console.log("State changed to:", state);
    
    switch (state) {
        case "start":
           button.style.backgroundColor = "";
           text.innerText = "Click the button to start.";
           button.addEventListener("click", waitFunction, { once: true });
           break;

         case "waiting":
           text.innerText = "Wait for the button to turn green!"
           let delay = Math.random()*3000 + 2000     
           setTimeout(switchGreen, delay);
           break;

         case "testing":
           break;

         case "restart":
           button.addEventListener("click", function () {
               button.style.backgroundColor = "red";
               updateState("waiting");
            }, { once: true });
    }
}


function waitFunction() {
    button.style.backgroundColor = "red";
    updateState("waiting");
}

function switchGreen() {
    startTime = performance.now();
    button.style.backgroundColor = "green";
    text.innerText = "CLICK!";
    state = "testing";
    button.addEventListener("click", testFunction);
}

function testFunction() {
    if (state !== "testing") return;
    button.style.backgroundColor = "";

    let reactionTime = (performance.now() - startTime)/1000;
    text.innerText = `Your reaction time is ${reactionTime.toFixed(3)} s. Click the button to try again.`;

    let username = localStorage.getItem("username");
    if (!username) {
        console.error("Username not found in localStorage");
        return;
    }


    fetch('/save_reaction_time', {
        method: "POST",
        body: JSON.stringify({
            username: username,
            reactionTime: reactionTime
        }),
        headers: { "Content-type": "application/json" }
    })
    .then(response => response.json())
    .then(data => console.log("Server response:", data))
    .catch(error => console.error("Fetch Error:", error));

    updateState("restart");
}

updateState("start");
   
