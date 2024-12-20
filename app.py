import requests
# import subprocess
from bs4 import BeautifulSoup
# from langdetect import detect, detect_langs
# from phonemizer import phonemize
# from transliterate import translit
# from polyglot.text import Text
import lyricsgenius as lg
import os
# import tkinter as tk
# from polyglot.downloader import downloader
# import pandas lib as pd
import pandas as pd
import re
os.environ["JOBLIB_TEMP_FOLDER"] = "/tmp"
def get_lyrics(song_title, artist_name):
    lyrics = None
    # if artist_name:
    #     api_key = "0qEBzSyEEqPKfI-k4Q1hUOumZSqM1Dhux-L_afptee-rFhEFva4lgwkCHmLOc-XS"
    #     genius = lg.Genius(api_key, skip_non_songs=True, excluded_terms=["(Remix)", "(Live)"], remove_section_headers=True)
    #     artist = genius.search_artist(artist_name)
    #     song = artist.song(song_title)
    #     lyrics=song.lyrics
    # Format the song title and artist to be URL-friendly
    if(lyrics==None):
        if(artist_name):
            search_query = f"{song_title} {artist_name} lyrics".replace(" ", "+")
        else:
            search_query = f"{song_title} lyrics".replace(" ", "+")

        search_url = f"https://www.google.com/search?q={search_query}"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Referer": "https://www.google.com",
            "DNT": "1",  # Do Not Track Request Header
            "Pragma": "no-cache",
            "Cache-Control": "no-cache"
        }

        try:
            # Perform Google search to find the lyrics page
            response = requests.get(search_url, headers=headers)
            response.raise_for_status()
        except requests.RequestException as e:
            print("Failed to connect to Google:", e)
            return None,None, None, None,None, None, None, None

        # Parse the search results page
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Try to find a link to a lyrics website
        lyrics_url = None
        for link in soup.find_all("a", href=True):
            url = link["href"]
            if "genius.com" in url or "azlyrics.com" in url:
                lyrics_url = url
                break

        if not lyrics_url:
            print("Could not find a lyrics page.")
            return None,None, None, None,None, None, None, None

        try:
            # Fetch the lyrics page
            response = requests.get(lyrics_url, headers=headers)
            response.raise_for_status()
        except requests.RequestException as e:
            print("Failed to retrieve lyrics page:", e)
            return None,None, None, None,None, None, None, None

        # Parse the lyrics page
        lyrics_soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract lyrics text
        
        try:
            if "genius.com" in lyrics_url:
                # For Genius
                lyrics_div = lyrics_soup.find("div", class_="lyrics") or lyrics_soup.find("div", {"data-lyrics-container": "true"})
                lyrics = lyrics_div.get_text(separator="\n") if lyrics_div else None
            elif "azlyrics.com" in lyrics_url:
                # For AZLyrics
                lyrics_div = lyrics_soup.find("div", attrs={"class": None, "id": None})
                lyrics = lyrics_div.get_text(separator="\n") if lyrics_div else None
            elif "lyricsted.com" in lyrics_url:
                lyrics_div = lyrics_soup.find("div", class_="lyrics-content")
                lyrics = lyrics_div.get_text(separator="\n") if lyrics_div else None
            elif "lyricsbell.com" in lyrics_url:
                lyrics_div = lyrics_soup.find("div", class_="lyrics")
                lyrics = lyrics_div.get_text(separator="\n") if lyrics_div else None
            elif "glamsham.com" in lyrics_url:
                lyrics_div = lyrics_soup.find("div", id="songLyricsDiv")
                lyrics = lyrics_div.get_text(separator="\n") if lyrics_div else None
            elif "lyricsmint.com" in lyrics_url:
                lyrics_div = lyrics_soup.find("div", class_="lyrics")
                lyrics = lyrics_div.get_text(separator="\n") if lyrics_div else None

        except AttributeError as e:
            print("Failed to parse lyrics:", e)

    if not lyrics:
        print("Lyrics not found.")
        return None,None, None, None,None, None, None, None
    lyrics=re.sub(r"\[.*?\]",'',lyrics)
    lyrics=lyrics.replace("\n"," ")
    original=lyrics
    try:
        pass
        # text_obj = Text(lyrics)
        # detected_language = text_obj.language.code  # Detect language
        # if detected_language != "en":  # If not English
        #     lyrics = text_obj.transliterate("en")
    except Exception as e:
        print("Failed to transliterate lyrics:", e)
        # Attempt to install the missing language package and retry
        try:
            pass
            # language_code = e.args[0].split("'")[-2]  # Extract language code from the error message
            # downloader.download("TASK:transliteration2", quiet=True)
            # transliteration_path = os.path.join("polyglot_data", "transliteration2", "he")
            # target_path = os.path.join("polyglot_data", "transliteration2", "iw")

            # # Rename the folder if it exists
            # if os.path.exists(transliteration_path) and not os.path.exists(target_path):
            #     os.rename(transliteration_path, target_path)
            #     print(f"Renamed folder from 'he' to 'iw' to resolve the issue.")
            # print(f"Installed missing language package: {language_code}. Retrying transliteration.")
            # text_obj = Text(lyrics)
            # lyrics = text_obj.transliterate("en")
        except Exception as retry_error:
            print("Failed to install missing language package or retry transliteration:", retry_error)
            # return lyrics, None, None, None,None, None, None, None
    # Mapping consonants to colors

    code = ""
    colors = ""
    colorsArray = [] 
    deepCode = "" 
    deepColors = "" 
    deepColorsArray = [] 
    color_map = {
        "Yellow": ['K', 'G', 'J', 'CH'],
        "Grey": ['M', 'N'],
        "Red": ['T', 'D'],
        "Blue": ["R", "L"],
        "Green": ['Y', 'W', 'H', 'KH'],
        "Purple": ['P', 'B', 'F', 'V'],
        "Brown": ['S', 'Z']
    }
    if isinstance(lyrics, list):  # Check if lyrics is a WordList
        lyrics = " ".join(lyrics)

    for word in lyrics.split():
        # Skip non-alphabetic words
        if not word.isalpha():
            continue
        
        # Find the first consonant and all consonants in the word
        first_consonant = None
        consonants = []
        try:
            for letter in word.upper():
                if letter not in "AEIOU":
                    if first_consonant is None:
                        first_consonant = letter
                    consonants.append(letter)
            
            # Process the first consonant for `code` and `colors`
            if first_consonant:
                for index, (color, letters) in enumerate(color_map.items(), start=1):
                    if first_consonant in letters:
                        code += str(index)
                        colors += color
                        colorsArray.append(color)
                        break  # Exit loop once the first consonant is mapped
            
            # Process all consonants for `deepCode`, `deepColors`, and `deepColorsArray`
            word_deep_code = ""
            word_deep_colors = []
            for consonant in consonants:
                for index, (color, letters) in enumerate(color_map.items(), start=1):
                    if consonant in letters:
                        word_deep_code += str(index)
                        word_deep_colors.append(color)
                        break  # Exit loop once the consonant is mapped
            
            # Append results for the word
            if word_deep_code:
                deepCode += word_deep_code
            if word_deep_colors:
                deepColors += "".join(word_deep_colors)
                deepColorsArray.append(word_deep_colors)
        except Exception as e:
            print(f"Error processing word '{word}':", e)
    return original,lyrics, code, colors,colorsArray,deepCode,deepColors,deepColorsArray

from flask import Flask, request, render_template, jsonify
import re

app = Flask(__name__)


def process_input(song, artist):
    # Combine song and artist, then split into words
    original, lyrics, code, colors, colorsArray, deepCode, deepColors, deepColorsArray = get_lyrics(song, artist)
    lyrics = lyrics.replace('\n', " ")
    lyrics = re.sub(r"\[.*?\]", '', lyrics)
    # Filter out words composed only of vowels
    split_words = lyrics.split()

    vowels = set("aeiouAEIOU")
    split_words = list(filter(lambda x: not set(x).issubset(vowels) and x.isalpha(), split_words))

    # Process lyrics into required data
    return  original, lyrics, code, colors, colorsArray, deepCode, deepColors, deepColorsArray, split_words

@app.route("/")
def home():
    return render_template("index.html")  # Create an HTML file named "index.html" in a "templates" folder

@app.route("/process", methods=["POST"])
def process():
    data = request.json
    song = data.get("song")
    artist = data.get("artist")
    if not song:
        return jsonify({"error": "Song title is required"}), 400

    # Process input
    original, lyrics, code, colors, colorsArray, deepCode, deepColors, deepColorsArray, split_words = process_input(song, artist)
    return jsonify({"colors": deepColorsArray, "words": split_words, "original":original,"lyrics": lyrics, "code": code, "stringcolors": colors, "colorsArray": colorsArray, "deepCode": deepCode, "deepColors": deepColors})

if __name__ == "__main__":
    app.run(debug=True)