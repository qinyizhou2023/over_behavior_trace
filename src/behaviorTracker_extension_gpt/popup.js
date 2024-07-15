document.getElementById('injectScript').addEventListener('click', function() {
    chrome.runtime.sendMessage({ action: "injectScript" });
});
