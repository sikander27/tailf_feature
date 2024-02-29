
function printLog(logBoard, logMessage) {
    const logElement = document.createElement("p");
    logElement.innerText = logMessage;
    logBoard.append(logElement)
}

export {printLog};
