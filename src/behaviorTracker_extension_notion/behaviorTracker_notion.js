
// behaviorTracker_notion.js
(function() {

let behaviorData = [];
let copyCount = 0;

// 添加点击监听器
document.addEventListener('click', function(event) {
    let clickData = {
        type: 'click', e: 'click',
        timestamp: new Date().toISOString(),
        target: event.target.tagName,
        x: event.clientX,
        y: event.clientY
    };
    behaviorData.push(clickData);
    console.log('Click event:', clickData);
});

// 监听mousewheel事件
window.addEventListener('wheel', function(event) {
    // 创建一个滚动事件对象
    let mousewheelData = {
        type: 'mousewheel',
        timestamp: new Date().toISOString(),
        deltaY: event.deltaY
    };

    // 将滚动事件对象添加到 behaviorData 数组中
    behaviorData.push(mousewheelData);

    // 输出滚动事件到控制台
    console.log('Scroll event:', mousewheelData);
});

// 添加鼠标移动监听器
let totalMouseMovement = 0;
document.addEventListener('mousemove', function(event) {
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
});


// 添加滚动监听器
let timer;  // 定义一个计时器变量

// 创建一个函数来处理滚轮事件
function handleWheelEvent(event) {
    // 取消之前设置的计时器
    clearTimeout(timer);

    // 设置一个新的计时器，在500毫秒后执行滚轮事件处理函数
    timer = setTimeout(() => {
        let scrollEventData = {
            type: 'scroll',
            timestamp: new Date().toISOString(),
            deltaY: event.deltaY,
        };

        // 将滚动事件数据存入行为数据数组
        behaviorData.push(scrollEventData);

        // 输出调试信息
        console.log('Scroll event data:', scrollEventData);
    }, 500);  // 这里的500毫秒可以根据需要调整
}

// 添加一个事件监听器，监听document上的wheel事件
document.addEventListener('wheel', handleWheelEvent);




// 添加复制监听器
let lastCopiedText = ''; // 用于存储上次复制的文本，以便判断是否是重复复制
let totalCopyCount = 0;

document.addEventListener('copy', function(event) {
    // 获取复制的文本内容
    let copiedText = window.getSelection().toString().trim();

    // 只有当复制的文本不为空且与上次复制的不同才增加计数
    if (copiedText && copiedText !== lastCopiedText) {
        totalCopyCount++;
        lastCopiedText = copiedText; // 更新上次复制的文本内容

        // 创建复制事件数据
        let copyData = {
            type: 'copy',
            timestamp: new Date().toISOString(),
            text: copiedText,
            textLength: copiedText.length
        };

        // 将复制事件数据存入行为数据数组
        behaviorData.push(copyData);

        // 输出调试信息
        console.log('Copy event:', copyData);
        console.log('Total copy count:', totalCopyCount);
        console.log('Copied text length:', copiedText.length);
    }
});

// 添加粘贴监听器
let lastPastedText = ''; // 用于存储上次粘贴的文本，以便判断是否是重复粘贴
let totalPasteCount = 0;

document.addEventListener('paste', function(event) {
    // 获取粘贴的文本内容
    let pastedText = (event.clipboardData || window.clipboardData).getData('text').trim();

    // 只有当粘贴的文本不为空且与上次粘贴的不同才增加计数
    if (pastedText && pastedText !== lastPastedText) {
        totalPasteCount++;
        lastPastedText = pastedText; // 更新上次粘贴的文本内容

        // 创建粘贴事件数据对象
        let pasteData = {
            type: 'paste',
            timestamp: new Date().toISOString(),
            text: pastedText,
            textLength: pastedText.length
        };

        // 将粘贴事件数据存入行为数据数组
        behaviorData.push(pasteData);

        // 输出调试信息
        console.log('Paste event:', pasteData);
        console.log('Total paste count:', totalPasteCount);
        console.log('Pasted text length:', pastedText.length);
    }
});

// 监听删除动作（Delete和Backspace）
document.addEventListener('keydown', function(event) {
    if (event.key === 'Delete' || event.key === 'Backspace') {
        // 记录删除动作
        let deleteEventData = {
            type: 'deleteAction',
            timestamp: new Date().toISOString(),
            key: event.key
        };
        behaviorData.push(deleteEventData);
        console.log('Delete action event:', deleteEventData);
    }
});

// 添加键盘按键监听器
document.addEventListener('keypress', function(event) {
    // 记录键盘按键行为
    let keyPressData = {
        type: 'keypress',
        timestamp: new Date().toISOString(),
        key: event.key,
        keyCode: event.keyCode,
        target: event.target.tagName
    };
    behaviorData.push(keyPressData);
    console.log('Keypress event:', keyPressData);
});

// 添加高亮监听器
document.addEventListener('mouseup', function(event) {
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
});

// 添加发呆监听器
let idleTimer; // 定义一个变量用于存放计时器
let lastActionTime = Date.now(); // 记录上一次用户操作的时间戳

// 初始化存储空闲时间的数组
let idleTimes = [];

function resetIdleTimer() {
    clearTimeout(idleTimer); // 清除之前的计时器
    idleTimer = setTimeout(function() {
        // 这里是超过2000毫秒没有操作的处理逻辑
        let currentTime = Date.now();
        let idleDuration = currentTime - lastActionTime;

        // 记录空闲时间，并包含类型信息
        let idleData = {
            type: 'idle',
            timestamp: new Date().toISOString(),
            duration: idleDuration
        };
        idleTimes.push(idleData); // 将空闲时间记录存入数组
        console.log(`距离上次操作已经过去 ${idleDuration} 毫秒`);
        behaviorData.push(idleData);
    }, 2000); // 设置超过2000毫秒触发
}

// 监听用户的鼠标移动、键盘输入和滚动等操作
function handleUserAction() {
    lastActionTime = Date.now(); // 更新最后一次操作时间
    resetIdleTimer();
}

document.addEventListener('mousemove', handleUserAction);
document.addEventListener('keypress', handleUserAction);
document.addEventListener('scroll', handleUserAction);

// 初始化页面时开始计时
resetIdleTimer();

// 分割：下面是导出设置

// 添加导出按钮
let exportButton = document.createElement('button');
exportButton.innerText = 'Finish';
exportButton.style.position = 'fixed';
exportButton.style.top = '10px';
exportButton.style.right = '10px';
exportButton.style.zIndex = 1000;
document.body.appendChild(exportButton);

// 添加清除按钮
let clearButton = document.createElement('button');
clearButton.innerText = 'Start';
clearButton.style.position = 'fixed';
clearButton.style.top = '50px';
clearButton.style.right = '10px';
clearButton.style.zIndex = 1000;
document.body.appendChild(clearButton);

// 创建并添加倒计时显示器
let timerDisplay = document.createElement('div');
timerDisplay.style.position = 'fixed';
timerDisplay.style.top = '90px';
timerDisplay.style.right = '10px';
timerDisplay.style.zIndex = 1000;
timerDisplay.style.fontSize = '20px';
timerDisplay.style.fontWeight = 'bold';
document.body.appendChild(timerDisplay);

let countdown; // 倒计时变量
let timeLeft = 15 * 60; // 初始时间设为15分钟，单位为秒


// 清除按钮点击事件处理
clearButton.addEventListener('click', function() {
    // 清空行为数据数组和相关变量
    behaviorData = [];
    copyCount = 0; // 如果有其他计数器或变量也要重置，在此处添加代码

    // 重置倒计时
    timeLeft = 15 * 60;
    clearInterval(countdown);
    startCountdown();

    // 输出调试信息
    console.log('Behavior data cleared.');
});



// 导出行为数据为JSON文件
exportButton.addEventListener('click', function() {
    clearInterval(countdown);
    exportBehaviorData();
});

// 导出行为数据的函数
function exportBehaviorData() {
    let dataStr = JSON.stringify(behaviorData, null, 2);
    let blob = new Blob([dataStr], { type: 'application/json' });
    let url = URL.createObjectURL(blob);
    let a = document.createElement('a');
    a.href = url;
    a.download = 'tasksheet_data.json';
    a.click();
    URL.revokeObjectURL(url);
    console.log('Behavior data exported:', dataStr);
}

// 启动倒计时的函数
function startCountdown() {
    countdown = setInterval(function() {
        if (timeLeft <= 0) {
            clearInterval(countdown);
            timerDisplay.innerText = 'Time is up!';
            exportBehaviorData();
        } else {
            let minutes = Math.floor(timeLeft / 60);
            let seconds = timeLeft % 60;
            timerDisplay.innerText = `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
            timeLeft--;
        }
    }, 1000);
}

})();
