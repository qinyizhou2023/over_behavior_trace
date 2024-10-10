(function() {
    // Constants and configurations
    const CONFIG = {
        KEYWORD_STREAMING: "result-streaming",
        ID_PROMPT_INPUT: "#chat-input",
        QUERY_SEND_BTN: ".button_icon-button__VwAMf[role='button']",
        QUERY_CHAT_DIV: ".chat_chat__ZebHg",
        QUERY_ELM_RESPONSE: ".chat_chat-message__dg8rL",
    };

    // Variables
    let behaviorData = [];
    let lastMessageSentTime = null;
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
    let startTime = null;
    let userInput = '';
    let textLength = 0;
    let countdownTimer;
    let timeLeft = 18 * 60; // 18 minutes in seconds
    let timerDisplay;
    let warningDisplay;

    // Helper functions
    function checkValidPage() {
        const currentUrl = window.location.href;
        if (!currentUrl.includes('vercel.app')) {
            alert("Reminder: You should activate the extension on the NextChat website!");
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
        window.addEventListener('mousewheel', handleWheelEvent);
        document.addEventListener('copy', handleCopyEvent);
        document.addEventListener('paste', handlePasteEvent);
        document.addEventListener('keydown', handleKeydownEvent);
        document.addEventListener('keypress', handleKeyPressEvent);
        document.addEventListener('mouseup', handleHighlightEvent);
        document.addEventListener('mousemove', handleUserAction);
        document.addEventListener('keypress', handleUserAction);
        document.addEventListener('scroll', handleUserAction);
        document.addEventListener('visibilitychange', handleVisibilityChangeEvent);
    }

    // Event handlers

    function handleVisibilityChangeEvent() {
        let visibilityData = {
            type: 'visibilityChange',
            timestamp: formatTimestamp(Date.now()),
            isHidden: document.hidden
        };
        behaviorData.push(visibilityData);
        console.log('Visibility change event:', visibilityData);
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

    function handleHighlightEvent(event) {
        let selectedText = window.getSelection().toString().trim();
        if (selectedText) {
            let highlightData = {
                type: 'highlight',
                timestamp: new Date().toISOString(),
                text: selectedText
            };
            behaviorData.push(highlightData);
            console.log('Highlight event:', highlightData);
        }
    }

    function handleUserAction(event) {
        lastActionTime = Date.now();
        clearTimeout(idleTimer);
        idleTimer = setTimeout(() => {
             idleData = {
                type: 'idle',
                timestamp: new Date().toISOString(),
                duration: Date.now() - lastActionTime
            }
            idleTimes.push(idleData);
            behaviorData.push(idleData);
            console.log('User is idle:', idleTimes[idleTimes.length - 1]);
        }, 3000); // 3 seconds of inactivity
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
    
    let firstTimeNotNull = null;
    
    function recordMessageSentTime() {
        const currentTime = new Date();
        if (firstTimeNotNull === null) {
            firstTimeNotNull = currentTime;
            const firstNotNullData = {
                type: 'firstNotNull',
                time: firstTimeNotNull.toLocaleString()
            };
            behaviorData.push(firstNotNullData);
            console.log('First time that lastMessageSentTime becomes not null:', firstTimeNotNull.toLocaleString());
        }
        if (lastMessageSentTime !== null) {
            const timeInterval = currentTime - lastMessageSentTime;
            const messageIntervalData = {
                type: 'messageInterval',
                startTime: lastMessageSentTime.toLocaleString(),
                endTime: currentTime.toLocaleString(),
                duration: timeInterval
            };
            behaviorData.push(messageIntervalData);
            console.log('Message interval (ms):', timeInterval);
        } 
            
        lastMessageSentTime = currentTime;
    }


    // Input monitoring
    function setupInputMonitoring() {
        const inputBox = document.querySelector(CONFIG.ID_PROMPT_INPUT);
        inputBox.addEventListener('keydown', function(event) {
            if (startTime === null) {
                startTime = new Date();
                console.log('Start typing at:', startTime.toLocaleString());
            }
            // Check if user pressed ctrl+enter
            if (event.ctrlKey && event.key === 'Enter') {
                recordMessageSentTime();
            }
        });

        inputBox.addEventListener('input', function(event) {
            userInput = inputBox.value;
        });

        let button = document.querySelector('.button_icon-button__VwAMf.undefined.undefined.chat_chat-input-send__GFQZo.clickable.button_primary__dwYZ6');
        let lastClickTime = null;

        button.addEventListener('click', function() {
            let currentTime = new Date();
            if (lastClickTime !== null) {
                let interval = currentTime - lastClickTime;
                console.log(`Interval between clicks: ${interval} ms`);
            }
            lastClickTime = currentTime;
            recordMessageSentTime(); // Ensure data recording is triggered
        });
    }



    function recordAndExportData() {
        if (startTime !== null) {
            const endTime = new Date();
            console.log('End typing at:', endTime.toLocaleString());
            const duration = endTime - startTime;
            textLength = userInput.length;
            console.log('Typing duration (ms):', duration);
            console.log('Input text length:', textLength);
            console.log('User input:', userInput);
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
            userInput = '';
            textLength = 0;
        }
        // Record the time of the last message sent
        recordMessageSentTime();
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

        let startButton1 = document.createElement('button');
        startButton1.innerText = 'Start';
        startContainer.appendChild(startButton1);

        let finishButton = document.createElement('button');
        finishButton.innerText = 'Finish';
        finishContainer.appendChild(finishButton);

        startButton1.addEventListener('click', function() {
            behaviorData = [];
            copyCount = 0;
            console.log('Behavior data cleared.');
            alert('Start Now！');
            startTimer();
            startContainer.style.display = 'none';
        });

        finishButton.addEventListener('click', function() {
            clearInterval(countdownTimer);
            exportBehaviorData();
            startContainer.style.display = 'block';
        });

    // shen
        createTimerDisplay();
        const startButton = document.querySelector(CONFIG.QUERY_SEND_BTN);
        startButton.addEventListener('click', function() {
            behaviorData = [];
            console.log('Behavior data cleared.');
            alert('Start Now!');
            startTimer();
            recordAndExportData(); // Ensure data recording is triggered
        });
    }

function exportBehaviorData() {
        let dataStr = JSON.stringify(behaviorData, null, 2);
        let blob = new Blob([dataStr], { type: 'application/json' });
        let url = URL.createObjectURL(blob);
        let a = document.createElement('a');
        a.href = url;
        a.download = 'gpt_data.json';
        a.click();
        URL.revokeObjectURL(url);
        console.log('Behavior data exported:', dataStr);
    }

    // Main initialization function
    function init() {
        if (!checkValidPage()) {
            return;
        }
        addEventListeners();
        setupInputMonitoring();
        setupUI();
    }

    // Start the script
    init();

})();
