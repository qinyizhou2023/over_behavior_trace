// behaviorTracker_gpt.js
(function() {
    // Constants
    const CONFIG = {
        KEYWORD_STREAMING: "result-streaming",
        ID_PROMPT_INPUT: "prompt-textarea",
        QUERY_SEND_BTN: "[data-testid=\"send-button\"]",
        QUERY_CHAT_DIV: "[role=\"presentation\"]",
        QUERY_ELM_RESPONSE: "[data-message-author-role=\"assistant\"]",
        ID_TEXTBOX_PROMPT: "prompt-textarea",
        URL_ICON: "assets/icon48.png",
        QUERY_TOOLBAR: "[class=\"items-center justify-start rounded-xl p-1 flex\"]"
    };

    // Variables
    let behaviorData = [];
    let copyCount = 0;
    let totalMouseMovement = 0;
    let idleTimer;
    let lastActionTime = Date.now();
    let idleTimes = [];
    let lastCopiedText = '';
    let totalCopyCount = 0;
    let lastPastedText = '';
    let totalPasteCount = 0;
    let _isStreaming = false;
    let _observerNewResponse;
    let _sessionEntry = {};
    let startTime = null;
    let endTime = null;
    let userInput = '';
    let textLength = 0;
    let countdownTimer;
    let timeLeft = 18 * 60; // 18 minutes in seconds
    let timerDisplay;
    let warningDisplay;

    // Helper functions
    function checkValidPage() {
        const currentUrl = window.location.href;
        if (!currentUrl.includes('chatgpt.com')) {
            if (currentUrl.includes('docs.google.com/forms')) {
                alert("Reminder: This extension should not be activated on the gpt (Google Form) website. Please activate it on the GPT website!");
            } else {
                alert("Reminder: You should activate the extension on the GPT website!");
            }
            return false;
        }
        return true;
    }

    function formatTimestamp(timestamp) {
        return new Date(timestamp).toISOString();
    }

    function time() {
        return new Date().getTime();
    }

    // Timer functions
   function startTimer() {
        timeLeft = 18 * 60; // Reset time to 18 minutes
        updateTimerDisplay();
        countdownTimer = setInterval(updateTimer, 1000);
    }

    function stopTimer() {
        clearInterval(countdownTimer);
        countdownTimer = null;
        warningDisplay.textContent = "";
    }

    let centerMessageDisplay;

function createCenterMessageDisplay() {
    centerMessageDisplay = document.createElement('div');
    centerMessageDisplay.style.position = 'fixed';
    centerMessageDisplay.style.top = '50%';
    centerMessageDisplay.style.left = '50%';
    centerMessageDisplay.style.transform = 'translate(-50%, -50%)';
    centerMessageDisplay.style.backgroundColor = 'rgba(0, 0, 0, 0.8)';
    centerMessageDisplay.style.color = 'white';
    centerMessageDisplay.style.padding = '20px';
    centerMessageDisplay.style.borderRadius = '10px';
    centerMessageDisplay.style.fontSize = '24px';
    centerMessageDisplay.style.fontWeight = 'bold';
    centerMessageDisplay.style.zIndex = '10000';
    centerMessageDisplay.style.display = 'none';
    document.body.appendChild(centerMessageDisplay);
}

function showCenterMessage(message) {
    centerMessageDisplay.textContent = message;
    centerMessageDisplay.style.display = 'block';
}

function hideCenterMessage() {
    centerMessageDisplay.style.display = 'none';
}

function updateTimer() {
    timeLeft--;
    updateTimerDisplay();

    if (timeLeft <= 120 && timeLeft > 0) {
        warningDisplay.textContent = "Warning: Time is almost up.";
    } else if (timeLeft <= 0) {
        stopTimer();
        warningDisplay.textContent = "Time's up! Click 'Finish' to save your data.";
        showCenterMessage("Time is out, click 'Finish' and download the file");
    }
}


    function updateTimerDisplay() {
        let minutes = Math.floor(timeLeft / 60);
        let seconds = timeLeft % 60;
        timerDisplay.textContent = `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
    }

    function createTimerDisplay() {
        timerDisplay = document.createElement('div');
        timerDisplay.style.position = 'fixed';
        timerDisplay.style.top = '90px';
        timerDisplay.style.right = '10px';
        timerDisplay.style.zIndex = 1000;
        document.body.appendChild(timerDisplay);

        warningDisplay = document.createElement('div');
        warningDisplay.style.position = 'fixed';
        warningDisplay.style.top = '110px';
        warningDisplay.style.right = '10px';
        warningDisplay.style.zIndex = 1000;
        warningDisplay.style.color = 'red';
        document.body.appendChild(warningDisplay);
    }

    // Event listeners
    function addEventListeners() {
        window.addEventListener('focus', handleFocusEvent);
        window.addEventListener('blur', handleBlurEvent);
        document.addEventListener('click', handleClickEvent);
        document.addEventListener('mousemove', handleMouseMoveEvent);
        window.addEventListener('wheel', handleWheelEvent);
        document.addEventListener('copy', handleCopyEvent);
        document.addEventListener('paste', handlePasteEvent);
        document.addEventListener('keydown', handleKeydownEvent);
        document.addEventListener('keypress', handleKeyPressEvent);
        document.addEventListener('mouseup', handleHighlightEvent);
        document.addEventListener('mousemove', handleUserAction);
        document.addEventListener('keypress', handleUserAction);
        document.addEventListener('scroll', handleUserAction);
    }

    // Event handlers
    function handleFocusEvent() {
        let focusData = {
            type: 'focus',
            timestamp: formatTimestamp(Date.now()),
            status: 1
        };
        behaviorData.push(focusData);
        console.log('Focus event:', focusData);
    }

    function handleBlurEvent() {
        let blurData = {
            type: 'blur',
            timestamp: formatTimestamp(Date.now()),
            status: 0
        };
        behaviorData.push(blurData);
        console.log('Blur event:', blurData);
    }

    function handleClickEvent(event) {
        let clickData = {
            type: 'click',
            timestamp: new Date().toISOString(),
            target: event.target.tagName,
            x: event.clientX,
            y: event.clientY
        };
        behaviorData.push(clickData);
        console.log('Click event:', clickData);
    }

    function handleMouseMoveEvent(event) {
        if (event.movementX || event.movementY) {
            totalMouseMovement += Math.sqrt(event.movementX ** 2 + event.movementY ** 2);
            let mouseMovementData = {
                type: 'mouseMovement',
                timestamp: new Date().toISOString(),
                totalMouseMovement: totalMouseMovement
            };
            behaviorData.push(mouseMovementData);
            console.log('Total Mouse Movement:', totalMouseMovement);
        }
    }

    function handleWheelEvent(event) {
        let mousewheelData = {
            type: 'mousewheel',
            timestamp: new Date().toISOString(),
            deltaY: event.deltaY
        };
        behaviorData.push(mousewheelData);
        console.log('Scroll event:', mousewheelData);
    }

    function handleCopyEvent(event) {
        let copiedText = window.getSelection().toString().trim();
        if (copiedText && copiedText !== lastCopiedText) {
            totalCopyCount++;
            lastCopiedText = copiedText;
            let copyData = {
                type: 'copy',
                timestamp: new Date().toISOString(),
                text: copiedText,
                textLength: copiedText.length
            };
            behaviorData.push(copyData);
            console.log('Copy event:', copyData);
            console.log('Total copy count:', totalCopyCount);
            console.log('Copied text length:', copiedText.length);
        }
    }

    function handlePasteEvent(event) {
        let pastedText = (event.clipboardData || window.clipboardData).getData('text').trim();
        if (pastedText && pastedText !== lastPastedText) {
            totalPasteCount++;
            lastPastedText = pastedText;
            let pasteData = {
                type: 'paste',
                timestamp: new Date().toISOString(),
                text: pastedText,
                textLength: pastedText.length
            };
            behaviorData.push(pasteData);
            console.log('Paste event:', pasteData);
            console.log('Total paste count:', totalPasteCount);
            console.log('Pasted text length:', pastedText.length);
        }
    }

    function handleKeydownEvent(event) {
        if ((event.key === 'Delete' || event.key === 'Backspace' || (event.ctrlKey && event.key === 'x'))) {
            let deleteEventData = {
                type: 'deleteAction',
                timestamp: new Date().toISOString(),
                key: event.key
            };
            behaviorData.push(deleteEventData);
            console.log('Delete action event:', deleteEventData);
        }
    }

    function handleKeyPressEvent(event) {
        let keyPressData = {
            type: 'keypress',
            timestamp: new Date().toISOString(),
            key: event.key,
            keyCode: event.keyCode,
            target: event.target.tagName
        };
        behaviorData.push(keyPressData);
        console.log('Keypress event:', keyPressData);
    }

    function handleHighlightEvent(event) {
        let highlightedText = window.getSelection().toString().trim();
        if (highlightedText) {
            let highlightEventData = {
                type: 'highlight',
                timestamp: new Date().toISOString(),
                highlightedText: highlightedText,
                highlightedTextLength: highlightedText.length
            };
            behaviorData.push(highlightEventData);
            console.log('Highlight event:', highlightEventData);
            resetIdleTimer();
        }
    }

    function handleUserAction() {
        lastActionTime = Date.now();
        resetIdleTimer();
    }

    // Idle timer
    function resetIdleTimer() {
        clearTimeout(idleTimer);
        idleTimer = setTimeout(function() {
            let currentTime = Date.now();
            let idleDuration = currentTime - lastActionTime;
            let idleData = {
                type: 'idle',
                timestamp: new Date().toISOString(),
                duration: idleDuration
            };
            idleTimes.push(idleData);
            console.log(`距离上次操作已经过去 ${idleDuration} 毫秒`);
            behaviorData.push(idleData);
        }, 2000);
    }

    // Streaming observer
    function initObserver() {
        const targetNode = document.querySelector(CONFIG.QUERY_CHAT_DIV);
        const config = { childList: true, subtree: true };
        _observerNewResponse = new MutationObserver(callbackNewResponse);
        _observerNewResponse.observe(targetNode, config);
    }

    function callbackNewResponse(mutationsList, observer) {
        for (const mutation of mutationsList) {
            if (mutation.type === 'childList') {
                mutation.addedNodes.forEach(node => {
                    if (node.className != undefined && typeof node.className.includes == "function" && node.className.includes(CONFIG.KEYWORD_STREAMING)) {
                        _observerNewResponse.disconnect();
                        console.log("streaming starts");
                        _isStreaming = true;
                        _sessionEntry.timeStreamingStarted = time();
                        let streamingStartData = {
                            type: 'streaming_start',
                            timestamp: formatTimestamp(Date.now()),
                            status: 1
                        };
                        behaviorData.push(streamingStartData);
                        monitorStreaming();
                        return;
                    }
                });
            }
        }
    }

    function monitorStreaming() {
        setTimeout(() => {
            var elements = document.querySelectorAll('[class*="' + CONFIG.KEYWORD_STREAMING + '"]');
            if (elements.length > 0) {
                monitorStreaming();
            } else {
                console.log("streaming ends");
                _isStreaming = false;
                _sessionEntry.timeStreamingEnded = time();
                console.log(_sessionEntry);
                let streamingEndData = {
                    type: 'streaming_end',
                    timestamp: formatTimestamp(Date.now()),
                    status: 0
                };
                behaviorData.push(streamingEndData);
                initObserver();
            }
        }, 1000);
    }

    // Input monitoring
    function setupInputMonitoring() {
        const inputBox = document.querySelector("#prompt-textarea");
        inputBox.addEventListener('keydown', function(event) {
            if (startTime === null) {
                startTime = new Date();
                console.log('开始输入时间:', startTime.toLocaleString());
            }
        });

        inputBox.addEventListener('input', function(event) {
            userInput = inputBox.value;
        });
    }

    function recordAndExportData() {
        if (startTime !== null) {
            endTime = new Date();
            console.log('结束输入时间:', endTime.toLocaleString());
            const duration = endTime - startTime;
            textLength = userInput.length;
            console.log('输入时长（毫秒）:', duration);
            console.log('输入字数长度:', textLength);
            console.log('用户输入内容:', userInput);
            const inputData = {
                type: 'keyboardInput',
                startTime: startTime.toLocaleString(),
                endTime: endTime.toLocaleString(),
                duration: duration,
                userInputLength: textLength,
                userInputContent: userInput
            };
            behaviorData.push(inputData);
            startTime = null;
            endTime = null;
            userInput = '';
            textLength = 0;
        }
    }


        // UI setup
    function setupUI() {
        // Start button container
        let startContainer = document.createElement('div');
        startContainer.style.position = 'fixed';
        startContainer.style.top = '10px';
        startContainer.style.right = '10px';
        startContainer.style.zIndex = 1000;
        startContainer.style.backgroundColor = '#f0f0f0';
        startContainer.style.border = '1px solid #ccc';
        startContainer.style.borderRadius = '5px';
        startContainer.style.padding = '5px';
        startContainer.style.boxShadow = '0 2px 5px rgba(0,0,0,0.1)';
        document.body.appendChild(startContainer);

        // Finish button container
        let finishContainer = document.createElement('div');
        finishContainer.style.position = 'fixed';
        finishContainer.style.top = '50px';
        finishContainer.style.right = '10px';
        finishContainer.style.zIndex = 1000;
        finishContainer.style.backgroundColor = '#f0f0f0';
        finishContainer.style.border = '1px solid #ccc';
        finishContainer.style.borderRadius = '5px';
        finishContainer.style.padding = '5px';
        finishContainer.style.boxShadow = '0 2px 5px rgba(0,0,0,0.1)';
        document.body.appendChild(finishContainer);

        let startButton = document.createElement('button');
        startButton.innerText = 'Start';
        startContainer.appendChild(startButton);

        let finishButton = document.createElement('button');
        finishButton.innerText = 'Finish';
        finishContainer.appendChild(finishButton);

        startButton.addEventListener('click', function() {
            behaviorData = [];
            copyCount = 0;
            console.log('Behavior data cleared.');
            alert('Start Now！');
            startTimer();
            startContainer.style.display = 'none';
            chrome.storage.local.set({isTracking: true});
        });

        finishButton.addEventListener('click', function() {
            clearInterval(countdownTimer);
            exportBehaviorData();
            startContainer.style.display = 'block';
            chrome.storage.local.set({isTracking: false});
        });

        // Check if tracking is already in progress
        chrome.storage.local.get('isTracking', function(result) {
            if (result.isTracking) {
                startContainer.style.display = 'none';
            }
        });
    }

  // Function to save data to Chrome storage
    function saveToStorage() {
        chrome.storage.local.set({behaviorData: behaviorData}, function() {
            console.log('Data saved to Chrome storage');
        });
    }

    // Modify all functions that update behaviorData to save to storage
    function updateBehaviorData(newData) {
        behaviorData.push(newData);
        saveToStorage();
    }

  // Replace all instances of behaviorData.push(...) with updateBehaviorData(...)
    // For example:
    function handleFocusEvent() {
        let focusData = {
            type: 'focus',
            timestamp: formatTimestamp(Date.now()),
            status: 1
        };
        updateBehaviorData(focusData);
        console.log('Focus event:', focusData);
    }
    function handleBlurEvent() {
        let blurData = {
            type: 'blur',
            timestamp: formatTimestamp(Date.now()),
            status: 0
        };
        updateBehaviorData(blurData);
        console.log('Blur event:', blurData);
    }

    function handleClickEvent(event) {
        let clickData = {
            type: 'click',
            timestamp: new Date().toISOString(),
            target: event.target.tagName,
            x: event.clientX,
            y: event.clientY
        };
        updateBehaviorData(clickData);
        console.log('Click event:', clickData);
    }

    function handleMouseMoveEvent(event) {
        if (event.movementX || event.movementY) {
            totalMouseMovement += Math.sqrt(event.movementX ** 2 + event.movementY ** 2);
            let mouseMovementData = {
                type: 'mouseMovement',
                timestamp: new Date().toISOString(),
                totalMouseMovement: totalMouseMovement
            };
            updateBehaviorData(mouseMovementData);
            console.log('Total Mouse Movement:', totalMouseMovement);
        }
    }

    function handleWheelEvent(event) {
        let mousewheelData = {
            type: 'mousewheel',
            timestamp: new Date().toISOString(),
            deltaY: event.deltaY
        };
        updateBehaviorData(mousewheelData);
        console.log('Scroll event:', mousewheelData);
    }

    function handleCopyEvent(event) {
        let copiedText = window.getSelection().toString().trim();
        if (copiedText && copiedText !== lastCopiedText) {
            totalCopyCount++;
            lastCopiedText = copiedText;
            let copyData = {
                type: 'copy',
                timestamp: new Date().toISOString(),
                text: copiedText,
                textLength: copiedText.length
            };
            updateBehaviorData(copyData);
            console.log('Copy event:', copyData);
            console.log('Total copy count:', totalCopyCount);
            console.log('Copied text length:', copiedText.length);
        }
    }

    function handlePasteEvent(event) {
        let pastedText = (event.clipboardData || window.clipboardData).getData('text').trim();
        if (pastedText && pastedText !== lastPastedText) {
            totalPasteCount++;
            lastPastedText = pastedText;
            let pasteData = {
                type: 'paste',
                timestamp: new Date().toISOString(),
                text: pastedText,
                textLength: pastedText.length
            };
            updateBehaviorData(pasteData);
            console.log('Paste event:', pasteData);
            console.log('Total paste count:', totalPasteCount);
            console.log('Pasted text length:', pastedText.length);
        }
    }

    function handleKeydownEvent(event) {
        if ((event.key === 'Delete' || event.key === 'Backspace' || (event.ctrlKey && event.key === 'x'))) {
            let deleteEventData = {
                type: 'deleteAction',
                timestamp: new Date().toISOString(),
                key: event.key
            };
            updateBehaviorData(deleteEventData);
            console.log('Delete action event:', deleteEventData);
        }
    }

    function handleKeyPressEvent(event) {
        let keyPressData = {
            type: 'keypress',
            timestamp: new Date().toISOString(),
            key: event.key,
            keyCode: event.keyCode,
            target: event.target.tagName
        };
        updateBehaviorData(keyPressData);
        console.log('Keypress event:', keyPressData);
    }

    function handleHighlightEvent(event) {
        let highlightedText = window.getSelection().toString().trim();
        if (highlightedText) {
            let highlightEventData = {
                type: 'highlight',
                timestamp: new Date().toISOString(),
                highlightedText: highlightedText,
                highlightedTextLength: highlightedText.length
            };
            updateBehaviorData(highlightEventData);
            console.log('Highlight event:', highlightEventData);
            resetIdleTimer();
        }
    }
    // ... [Update all other event handlers similarly]

    function exportBehaviorData() {
        chrome.storage.local.get('behaviorData', function(result) {
            let dataStr = JSON.stringify(result.behaviorData, null, 2);
            let blob = new Blob([dataStr], { type: 'application/json' });
            let url = URL.createObjectURL(blob);
            let a = document.createElement('a');
            a.href = url;
            a.download = 'gpt_data.json';
            a.click();
            URL.revokeObjectURL(url);
            console.log('Behavior data exported:', dataStr);
        });
    }

    // ... [Rest of the code remains unchanged]

    // Main initialization function
     function init() {
        if (!checkValidPage()) {
            return;
        }

        addEventListeners();
        initObserver();
        setupInputMonitoring();
        setupUI();
        createCenterMessageDisplay();
        createTimerDisplay(); // Create timer display elements
        resetIdleTimer();


        // Set up periodic saving to Chrome storage
        setInterval(saveToStorage, 5000); // Save every 5 seconds
    }

    // Start the script
    init();

})();
