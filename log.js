
function printLog(logBoard, logMessage) {
    const logElement = document.createElement("li");
    logElement.innerText = logMessage;
    logBoard.append(logElement)
}

export {printLog};
