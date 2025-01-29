# Twitch-and-toot

A Python-based tool that posts to Mastodon, Twitter, and Bluesky when you go live on Twitch. Run it on any system - from a Raspberry Pi to AWS Lambda.

## Features

- 🎮 Twitch stream detection
- 🦣 Mastodon integration
- 🐦 Optional Twitter support
- 🦋 Optional Bluesky support
- 🔄 Customizable check intervals
- 📝 Configurable message templates
- 🐳 Docker support

## Requirements

- Python 3.8+
- Twitch Developer account
- Mastodon account
- (Optional) Twitter Developer account
- (Optional) Bluesky account

## Installation

1. Clone the Github repository to your device: `git clone https://github.com/ChiefGyk3D/twitch-and-toot.git`
2. Install the required packages: `pip install -r requirements.txt`
3. Set up configuration: rename .env.template to .env and edit it with your credentials
4. Run the script: `python main.py`

## Configuration

configure your settings:

1. Rename `.env.template` to `.env`
2. Edit `.env` with your credentials and settings
3. Customize message templates in `messages.txt` and `end_messages.txt`

The `.env` file supports these variables:

```env
TWITCH_CLIENT_ID=your_client_id
TWITCH_CLIENT_SECRET=your_client_secret 
TWITCH_USER_LOGIN=your_username

MASTODON_CLIENT_ID=your_client_id
MASTODON_CLIENT_SECRET=your_client_secret
MASTODON_ACCESS_TOKEN=your_access_token
MASTODON_API_BASE_URL=your_instance_url

# Optional Twitter settings
TWITTER_API_KEY=your_api_key
TWITTER_API_SECRET=your_api_secret
TWITTER_ACCESS_TOKEN=your_access_token
TWITTER_ACCESS_SECRET=your_access_secret

# Optional Bluesky settings 
BLUESKY_USERNAME=your_username
BLUESKY_PASSWORD=your_app_password

# Optional AWS/Vault settings
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
VAULT_TOKEN=your_vault_token

# Intervals (in minutes)
CHECK_INTERVAL=5
POST_INTERVAL=60
```

## Message Templates

Configure stream notifications in `messages.json`. The file supports multiple message templates for both stream start and end notifications:

```json
{
  "messages": {
    "live": [
      "I'm now live on Twitch! Playing: {stream_title}. Watch here: https://twitch.tv/{twitch_user_login}",
      "Join me on Twitch as I play {stream_title}! https://twitch.tv/{twitch_user_login}"
    ],
    "end": [
      "Stream's over! Thanks everyone for joining. Follow me at https://twitch.tv/{twitch_user_login}",
      "Just wrapped up my Twitch stream! Thanks for watching."
    ]
  }
}
```

Available variables:
- `{stream_title}`: Your stream title
- `{twitch_user_login}`: Your Twitch username


## Twitter Integration

While Twitch-and-toot is fundamentally a Mastodon-first project, we understand that some users may also want to post updates on Twitter. As of the current version, we have incorporated optional Twitter functionality. This feature allows users to post live stream updates not only on Mastodon but also on Twitter.

**Please note, as of the current version, Twitter functionality has not been added to the Docker version yet.**

# Requirements for Twitter Integration

To use the Twitter feature, you would need:

    Twitter API keys (API key & secret, Access token & secret). You can obtain these from the Twitter Developer Dashboard.

  ## Platform Setup

  ### Twitch
  1. Create a Twitch Developer account
  2. Create a new application
  3. Get Client ID and Client Secret
  4. Add them to .env

  ### Mastodon
  1. Go to your instance's settings
  2. Create new application
  3. Get access token
  4. Add credentials to .env

  ### Twitter (Optional)
  1. Create Twitter Developer account
  2. Create new project and app
  3. Generate keys and tokens
  4. Set TWITTER_ENABLE_POSTING=true in .env

  ### Bluesky (Optional)
  1. Create Bluesky account
  2. Generate app password
  3. Add credentials to .env
  4. Set BLUESKY_ENABLE_POSTING=true

### Caution

As stated before, placing secrets directly into the config.ini file is not a recommended practice for production environments. We are currently working on supporting secure storage and retrieval of Twitter API keys with AWS Secrets Manager and HashiCorp Vault. Please stay tuned for updates.

Moreover, please remember that this is an optional feature and Mastodon remains the primary focus of Twitch-and-toot. The addition of Twitter is intended to offer greater flexibility to our users and is not a shift from our Mastodon-first philosophy. If you experience any issues with the Twitter integration, please feel free to report them.

## AWS Secrets Manager Integration

The script supports optional integration with AWS Secrets Manager for secure storage and retrieval of Twitch and Mastodon API keys. To use this feature, store the credentials as secrets in AWS Secrets Manager and provide the secret names in the config.ini file.

**Please note that this feature is still in testing and any issues should be reported.**

## HashiCorp Vault Integration

The script also supports optional integration with HashiCorp Vault for secure storage and retrieval of Twitch and Mastodon API keys. To use this feature, store the credentials in Vault and provide the necessary Vault information in the config.ini file.

**Please note that this feature is still in testing and any issues should be reported.**

# Docker 

Twitch-and-toot is also available to be run in a Docker container. This can make the setup process easier and more consistent across different environments. It also allows for better scalability if you are running the bot for multiple Twitch channels.

## Requirements and Prerequisites for Docker

- Docker installed on your device.
- Docker Compose installed on your device (optional, only needed for docker-compose).

## Docker Installation

1. Navigate to the Docker directory in the project: `cd twitch-and-toot/Docker`
2. Build the Docker image: `docker build -t twitch-and-toot .`

If you are using Docker Compose, you can instead run:

`docker-compose up --build`

This will build and start the Docker container in one command.

## Docker Configuration

Configuration in Docker is done using environment variables instead of a config.ini file. These can be passed into the Docker container using the `-e` option with `docker run`:

`docker run -d --env-file .env twitch-and-toot`

For Docker Compose, Make sure your .env file is in the same directory as your docker-compose.yml file. The env_file directive will automatically load all environment variables from .env into the container.

You can then start the container with:

```bash
docker-compose up -d
```

Please note: If you are using a secrets manager with Docker, you will need to set up a network that allows the Docker container to access the secrets manager.

Remember to replace the necessary values with your actual data.

## Future plans

- Add support for more streaming platforms.

## Donations and Tips

If you would like to support the development of Twitch-and-toot, you can donate through the following links: [Donate](https://links.chiefgyk3d.com)

You can also tip the author with the following cryptocurrency addresses:

- Bitcoin: bc1q5grpa7ramcct4kjmwexfrh74dvjuw9wczn4w2f
- Monero: 85YxVz8Xd7sW1xSiyzUC5PNqSjYLYk4W8FMERVkvznR38jGTBEViWQSLCnzRYZjmxgUkUKGhxTt2JSFNpJuAqghQLhHgPS5
- PIVX: DS1CuBQkiidwwPhkfVfQAGUw4RTWPnBXVM
- Ethereum: 0x2a460d48ab404f191b14e9e0df05ee829cbf3733

## Authors

- ChiefGyk3D is the author of Twitch-and-toot
- [ChiefGyk3D's Mastodon Account](https://social.chiefgyk3d.com/@chiefgyk3d)
- Reviewed by Marc Gauthier [marcgauthier0.bsky.social]
- ChatGPT, an AI developed by OpenAI, helped build and reorganize the project.