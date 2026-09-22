document.getElementById('grabToken').addEventListener('click', () => {
  chrome.runtime.sendMessage({ action: 'grabToken' });
});
