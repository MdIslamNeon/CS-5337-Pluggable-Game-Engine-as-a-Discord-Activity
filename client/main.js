import { DiscordSDK } from '@discord/embedded-app-sdk';
import './style.css';
import rocketLogo from '/rocket.png';

const clientId = import.meta.env.VITE_DISCORD_CLIENT_ID;
const discordSdk = new DiscordSDK(clientId);

function render(message) {
  document.querySelector('#app').innerHTML = `
    <div>
      <img src="${rocketLogo}" class="logo" alt="Discord" />
      <h1>Hello, World!</h1>
      <p>${message}</p>
    </div>
  `;
}

async function setupDiscordSdk() {
  // Wait until Discord is ready to talk to the Activity
  await discordSdk.ready();

  // 1. Ask the user to authorize the app (this is the prompt in Step 7)
  const { code } = await discordSdk.commands.authorize({
    client_id: clientId,
    response_type: 'code',
    state: '',
    prompt: 'none',
    scope: ['identify', 'guilds'],
  });

  // 2. Our server swaps the code for an access token (server/server.js)
  const response = await fetch('/api/token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ code }),
  });
  const { access_token } = await response.json();

  // 3. Sign in to the Discord client with that token
  const auth = await discordSdk.commands.authenticate({ access_token });
  if (!auth) throw new Error('Authenticate command failed');
  return auth;
}

render('Connecting to Discord…');

setupDiscordSdk()
  .then((auth) => render(`Signed in as ${auth.user.username}`))
  .catch((err) => {
    console.error(err);
    render(`Sign-in failed: ${err.message}. Check that .env matches your dev app.`);
  });