{
  "manifest_version": 3,
  "name": "Behavior Tracker",
  "version": "1.0",
  "description": "Track user behaviors on any web page.",
  "permissions": [
    "activeTab",
    "scripting"
  ],
  "action": {
    "default_popup": "popup.html"
  },
  "background": {
    "service_worker": "background.js"
  }
}
