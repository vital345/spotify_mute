import tekore as tk
from pycaw.pycaw import AudioUtilities 
import time

client_id = '7cfedd8d098e4c0999279f490724b0c9'
client_secret = '85ae732f98c74c0bb62b584647df7156'
redirect_uri = 'https://example.com/callback/'


# function for muting spotify 
def muteSpotifyTab(mute):
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        volume = session.SimpleAudioVolume
        if session.Process and session.Process.name() == 'Spotify.exe':
            if mute :
                volume.SetMute(1, None)
            else :
                volume.SetMute(0, None)

# Creating the access token with scopes for authentication and getting the track status 
def setting_spotify_Object(client_id, client_secret, redirect_uri):
    user_token = tk.prompt_for_user_token(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope=tk.scope.every
    )

    print('-'*100,'\n\n')

    spotify = tk.Spotify(user_token)
    print(spotify.playback_currently_playing())
    return spotify

# is_ad = spotify.playback_currently_playing()

spotify = setting_spotify_Object(client_id, client_secret, redirect_uri)


def mute_If_AD():
    global spotify # to use global variable spotify 
    try :
        is_ad = spotify.playback_currently_playing()  # if token is not expired
    except :
        print('Token expired')
        spotify = setting_spotify_Object(client_id, client_secret, redirect_uri)
        is_ad = spotify.playback_currently_playing() 

    try:
        if is_ad.currently_playing_type == 'ad':
            muteSpotifyTab(True)
        else :
            muteSpotifyTab(False)

    except Exception as e :
        print(e)


if __name__ == "__main__":
    while True:
        mute_If_AD()
        time.sleep(0.1)




