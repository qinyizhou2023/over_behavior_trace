// behaviorTracker_nextChat.js
(function() {
    // Constants and configurations
    const CONFIG = {
        ID_PROMPT_INPUT: "#chat-input",
        QUERY_SEND_BTN: ".button_icon-button__VwAMf[role='button']",
        QUERY_CHAT_DIV: ".chat_chat__ZebHg",
        QUERY_ELM_RESPONSE: ".chat_chat-message__dg8rL",
    };

    // Variables
    let behaviorData = [];
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
        if (!currentUrl.includes('nextchat.com')) {
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
    function handleWheelEvent(event) {
        let wheelData = {
            type: 'wheel',
            timestamp: new Date().toISOString(),
            deltaX: event.deltaX,
            deltaY: event.deltaY
        };
        behaviorData.push(wheelData);
        console.log('Wheel event:', wheelData);
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
            idleTimes.push({
                type: 'idle',
                timestamp: new Date().toISOString(),
                duration: Date.now() - lastActionTime
            });
            console.log('User is idle:', idleTimes[idleTimes.length - 1]);
        }, 5000); // 5 seconds of inactivity
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

    // Input monitoring
    function setupInputMonitoring() {
        const inputBox = document.querySelector(CONFIG.ID_PROMPT_INPUT);
        inputBox.addEventListener('keydown', function(event) {
            if (startTime === null) {
                startTime = new Date();
                console.log('Start typing at:', startTime.toLocaleString());
            }
        });

        inputBox.addEventListener('input', function(event) {
            userInput = inputBox.value;
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
    }

    // UI setup
    function setupUI() {
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
