chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "injectScript") {
        chrome.scripting.executeScript({
            target: { tabId: sender.tab.id },
            files: ["behaviorTracker.js"]
        });
    }
});
