import { printLog } from "./log.js";

window.addEventListener("DOMContentLoaded", () => {
    const logBoard = document.querySelector(".logs");
    // Open the WebSocket connection and register event handlers.
    console.log('making socket connection...')
    const websocket = new WebSocket("ws://localhost:8001/");
    receiveLogs(logBoard, websocket);
  });


function showMessage(message) {
    window.setTimeout(() => window.alert(message), 50);
}

function receiveLogs(logBoard, websocket) {
    websocket.addEventListener("message", ({ data }) => {
        const event = JSON.parse(data);
        console.log("sk log ", event)
        switch (event.type) {
        case "new":
            printLog(logBoard, event.message)
            break;
        case "close":
            websocket.close(1000);
            break;
        case "error":
            showMessage(event.message);
            break;
        default:
            throw new Error(`Unsupported event type: ${event.type}.`);
        }
    });
}