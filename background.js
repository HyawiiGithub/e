chrome.runtime.onInstalled.addListener(() => {
  chrome.storage.local.set({ token: '' });
});

chrome.action.onClicked.addListener((tab) => {
  chrome.storage.local.get(['token'], (result) => {
    if (result.token) {
      fetch('https://discord.com/api/v9/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${result.token}`
        },
        body: JSON.stringify({})
      })
      .then(response => response.json())
      .then(data => {
        console.log('Success:', data);
      })
      .catch((error) => {
        console.error('Error:', error);
      });
    } else {
      console.log('No token found');
    }
  });
});
