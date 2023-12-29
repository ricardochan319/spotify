import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth


# Function to authenticate with Spotify and get the Spotipy object
def authenticate_spotify():
    client_id = input("Enter your Spotify client ID: ")
    client_secret = input("Enter your Spotify client secret: ")

    if not client_id or not client_secret:
        raise ValueError("Please provide both client ID and client secret.")

    redirect_uri = "http://example.com"  # Use the same redirect URI configured in your Spotify Developer application

    scope = "playlist-modify-public playlist-modify-private"

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                   client_secret=client_secret,
                                                   redirect_uri=redirect_uri,
                                                   scope=scope))
    return sp


# Set the base URL to Billboard Hot 100
base_url = "https://www.billboard.com/charts/hot-100/"

# Prompt the user to enter a date
date_input = input("Please enter a date (YYYY-MM-DD): ")

# Construct the full URL with the entered date
full_url = f"{base_url}{date_input}/"

# Send an HTTP request to the URL
response = requests.get(full_url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the song titles
    title_elements = soup.select('li > ul > li > h3')

    # Display the top 100 titles
    print("Top 100 Titles:")
    top_100_titles = []
    for index, title_element in enumerate(title_elements[:100], start=1):
        title_text = title_element.text.strip()
        top_100_titles.append(title_text)
        print(f"{index}. {title_text}")

    # Ask the user if they want to add the titles to Spotify
    add_to_spotify = input("Do you want to add these titles to Spotify? (yes/no): ").lower()

    if add_to_spotify == 'yes':
        # Authenticate with Spotify
        sp = authenticate_spotify()

        # Create a new playlist
        playlist_name = input("Enter the name for your playlist: ")
        playlist = sp.user_playlist_create(sp.current_user()['id'], playlist_name, public=True)

        # Search for each song on Spotify and add it to the playlist
        for title in top_100_titles:
            results = sp.search(q=title, type='track', limit=1)
            if results['tracks']['items']:
                track_uri = results['tracks']['items'][0]['uri']
                sp.playlist_add_items(playlist['id'], [track_uri])

        print(f"Playlist '{playlist_name}' created and songs added to Spotify.")
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")
