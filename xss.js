const token = localStorage.getItem('token');
fetch('https://your-server.com/token', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({ token })
});
