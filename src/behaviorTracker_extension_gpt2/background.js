chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "injectScript") {
        chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
            chrome.scripting.executeScript({
                target: { tabId: tabs[0].id },
                files: ["behaviorTracker_gpt.js"]
            }, () => {
                console.log("Injected behaviorTracker_gpt.js successfully.");
            });
        });
    }
});
