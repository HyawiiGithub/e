const express = require('express');
const request = require('request');
const app = express();

app.get('/proxy', (req, res) => {
  const url = req.query.url;
  request.get({ url, json: true }, (error, response, body) => {
    if (error) {
      res.status(500).send(error);
    } else {
      res.jsonp(body);
    }
  });
});

app.listen(3000, () => {
  console.log('JSONP proxy server listening on port 3000');
});
