import time
import random
import os
from dotenv import load_dotenv
import json
from initializer import SocialMediaServices

def main():
    # Load environment variables and config
    load_dotenv()
    with open('messages.json') as f:
        config = json.load(f)

    print("Initializing social media services...")
    services = SocialMediaServices()
    twitch, mastodon, twitter_api, bluesky = services.get_services()

    def is_user_live(user_login):
        """Check if user is live on Twitch"""
        try:
            user_info = twitch.get_users(logins=[user_login])
            user_id = user_info['data'][0]['id']
            streams = twitch.get_streams(user_id=user_id)
            live_streams = [stream for stream in streams['data'] if stream['type'] == 'live']
            return live_streams[0]['title'] if live_streams else None
        except Exception as e:
            print(f"Error checking stream status: {e}")
            return None

    def post_message(message, stream_title=None, twitch_user_login=None):
        """Post message to all enabled social media platforms with rich content when available"""
        # Post to Mastodon if enabled
        if os.getenv('MASTODON_ENABLE_POSTING', 'true').lower() == 'true':
            try:
                mastodon.toot(message)
                print(f"Posted to Mastodon: {message}")
            except Exception as e:
                print(f"Failed to post to Mastodon: {e}")

        # Post to Twitter if enabled
        if os.getenv('TWITTER_ENABLE_POSTING', 'false').lower() == 'true':
            try:
                twitter_api.update_status(message)
                print(f"Posted to Twitter: {message}")
            except Exception as e:
                print(f"Failed to post to Twitter: {e}")

        # Post to Bluesky with external card if enabled
        if os.getenv('BLUESKY_ENABLE_POSTING', 'false').lower() == 'true':
            try:
                if stream_title and twitch_user_login:
                    # Create rich card for live stream
                    stream_url = f"https://twitch.tv/{twitch_user_login}"
                    description = f"Live now: {stream_title}"
                    # You can optionally add a thumbnail preview from Twitch
                    # thumbnail_url = f"https://static-cdn.jtvnw.net/previews-ttv/live_user_{twitch_user_login}-320x180.jpg"
                    
                    bluesky.post_with_link(
                        message=message,
                        title=stream_title,
                        uri=stream_url,
                        description=description,
                        # image_url=thumbnail_url  # Uncomment if you want to include thumbnail
                    )
                else:
                    # Fallback to regular post if no stream info
                    bluesky.post(message)
            except Exception as e:
                print(f"Failed to post to Bluesky: {e}")

        was_live = False

        while True:
            print("Checking if user is live...")
            stream_title = is_user_live(os.getenv('TWITCH_USER_LOGIN'))
            
            if stream_title is not None:
                print(f"User is live, playing: {stream_title}")
                if not was_live:
                    # Select and format random live message
                    message = random.choice(config['messages']['live']).format(
                        stream_title=stream_title, 
                        twitch_user_login=os.getenv('TWITCH_USER_LOGIN')
                    )
                    # Pass stream info for rich cards
                    post_message(
                        message,
                        stream_title=stream_title,
                        twitch_user_login=os.getenv('TWITCH_USER_LOGIN')
                    )
                    was_live = True
                            
                # Wait for configured interval before next check
                sleep_time = int(os.getenv('POST_INTERVAL_HOURS', 6)) * 60 * 60
                print(f"Waiting for {sleep_time//3600} hours before checking again...")
                time.sleep(sleep_time)
            else:
                # Handle end of stream message if enabled
                if was_live:
                    should_post_end = False
                    # Check platform-specific end stream message settings
                    if os.getenv('MASTODON_END_STREAM_MESSAGE', 'true').lower() == 'true' or \
                    os.getenv('TWITTER_END_STREAM_MESSAGE', 'false').lower() == 'true' or \
                    os.getenv('BLUESKY_END_STREAM_MESSAGE', 'true').lower() == 'true':
                        should_post_end = True

                    if should_post_end:
                        message = random.choice(config['messages']['end']).format(
                            twitch_user_login=os.getenv('TWITCH_USER_LOGIN')
                        )
                        post_message(message)
                    was_live = False

                # Wait for configured check interval
                check_interval = int(os.getenv('CHECK_INTERVAL_MINUTES', 10)) * 60
                print(f"User is not live, checking again in {check_interval//60} minutes...")
                time.sleep(check_interval)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nShutting down gracefully...")
    except Exception as e:
        print(f"Fatal error: {e}")