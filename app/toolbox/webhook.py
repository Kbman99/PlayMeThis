import os
from app import app
from app.toolbox import albumdetails

def temp_token():
    '''Generates Webhook Verify Token to work until server is killed'''
    import binascii
    temp_token = binascii.hexlify(os.urandom(24))
    return temp_token.decode('utf-8')


def setup_token():
    '''
    Sets the severs Webhook Verify Token if it doesn't exist in the environment variables
    :param app: The main app
    :return: Adds verifications token to config
    '''

    if app.config["WEBHOOK_VERIFY_TOKEN"] is None:
        print('WEBHOOK_VERIFY_TOKEN has not been set in the environment.\nGenerating random token...')
        token = temp_token()
        print('Token: {}'.format(token))
        app.config["WEBHOOK_VERIFY_TOKEN"] = token


def process_webhook(request, pusher_client, pl):
    content = request.json
    song_url = content["message"]
    # Add code to check if song is playing now
    pl.entries.append(song_url)
    details = albumdetails.get_song_details(song_url)
    artwork_url = details["song_artwork_url"]
    pusher_client.trigger('my-channel', 'new_song', {'message': details})
    pl.get_next_entry()
