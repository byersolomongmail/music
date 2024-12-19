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
    if artist_name:
        api_key = "0qEBzSyEEqPKfI-k4Q1hUOumZSqM1Dhux-L_afptee-rFhEFva4lgwkCHmLOc-XS"
        genius = lg.Genius(api_key, skip_non_songs=True, excluded_terms=["(Remix)", "(Live)"], remove_section_headers=True)
        artist = genius.search_artist(artist_name)
        song = artist.song(song_title)
        lyrics=song.lyrics
    # Format the song title and artist to be URL-friendly
    if(lyrics==None):
        if(artist_name):
            search_query = f"{song_title} {artist_name} lyrics".replace(" ", "+")
        else:
            search_query = f"{song_title} lyrics".replace(" ", "+")

        search_url = f"https://www.google.com/search?q={search_query}"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
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
    print(lyrics)
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

# import tkinter as tk


# def create_color_grid(root, canvas_size, grid_data, grid_words):
#     # Frame to hold the canvas and buttons
#     frame = tk.Frame(root)
#     frame.pack(fill=tk.BOTH, expand=True)

#     # Create the canvas
#     canvas = tk.Canvas(frame, bg="white")
#     canvas.grid(row=0, column=0, columnspan=4, sticky=tk.NSEW)

#     # Configure grid layout for resizing
#     frame.columnconfigure(0, weight=1)
#     frame.rowconfigure(0, weight=1)

#     # Pagination state
#     rows = cols = 7  # Fixed to a 7x7 grid
#     items_per_page = rows * cols
#     current_page = tk.IntVar(value=0)  # Keep track of the current page
#     zoomed = tk.BooleanVar(value=True)  # Track zoom state
#     show_words = tk.BooleanVar(value=False)  # Track zoom state
#     draw_patterns = tk.BooleanVar(value=False)  # Track draw patterns state

#     # Function to redraw the canvas for the current page
#     def redraw_canvas(event=None):
#         nonlocal canvas_size
#         canvas.delete("all")
#         # Update canvas size dynamically
#         canvas_size = min(canvas.winfo_width(), canvas.winfo_height())

#         start_idx = current_page.get() * items_per_page
#         end_idx = start_idx + items_per_page
#         page_data = grid_data[start_idx:end_idx]
#         page_words = grid_words[start_idx:end_idx]

#         def is_in_bounds(index):
#             """Check if the index is within valid bounds."""
#             return 0 <= index < len(page_data)

#         def same_row(idx1, idx2):
#             """Ensure two indices are in the same row."""
#             return idx1 // 7 == idx2 // 7

#         def within_one(idx1, idx2):
#             """Ensure two indices are in the same row."""
#             return abs(idx1 // 7 - idx2 // 7) <= 1

#         def check_match(current_idx, neighbor_idx):
#             """Check if two cells match in color."""
#             if not is_in_bounds(neighbor_idx) or not within_one(current_idx, neighbor_idx) or neighbor_idx > 49:
#                 return False
#             # Ensure neighbors are valid horizontally or diagonally
#             if (neighbor_idx in (current_idx - 1, current_idx + 1) and not same_row(current_idx, neighbor_idx)):
#                 return False
#             if (neighbor_idx in (current_idx - 6, current_idx + 6) and same_row(current_idx, neighbor_idx)):
#                 return False
#             current = page_data[current_idx]
#             neighbor = page_data[neighbor_idx]
#             current_color = current[0] if isinstance(current, list) else current
#             neighbor_color = neighbor[0] if isinstance(neighbor, list) else neighbor
#             return current_color == neighbor_color
#         def draw_arrows_or_box(i, j, idx):
          
#             diagonal_pairs = [
#                 (idx - 8, idx + 8),
#                 (idx - 6, idx + 6),
#             ]
#             adjacent_pairs = [
#                 (idx - 1, idx - 7, idx - 8),
#                 (idx - 1, idx + 7, idx + 6),
#                 (idx + 1, idx - 7, idx - 6),
#                 (idx + 1, idx + 7, idx + 8),
#             ]

#             has_square = False
#             for triplet in adjacent_pairs:
#                 if not has_square:
#                     if all(check_match(idx, t) for t in triplet):
#                         has_square = True
#                         canvas.create_rectangle(
#                             x1, y1, x2, y2, outline="white", width=3
#                         )
#             if not has_square:
#                 for (dir1, dir2) in diagonal_pairs:
#                     if check_match(idx, dir1) or check_match(idx, dir2):
#                         if dir1 == idx - 8:  # North-West / South-East
#                             canvas.create_line(
#                                 x1, y1, x2, y2, arrow=tk.LAST, fill="white", width=2
#                             )
#                             canvas.create_line(
#                                 x2, y2, x1, y1, arrow=tk.LAST, fill="white", width=2
#                             )
#                         elif dir1 == idx - 6:  # North-East / South-West
#                             canvas.create_line(
#                                 x2, y1, x1, y2, arrow=tk.LAST, fill="white", width=2
#                             )
#                             canvas.create_line(
#                                 x1, y2, x2, y1, arrow=tk.LAST, fill="white", width=2
#                             )
#         for i in range(rows):
#             for j in range(cols):
#                 idx = i * cols + j
#                 if idx >= len(page_data):
#                     break

#                 x1, y1 = j * (canvas_size // cols), i * (canvas_size // rows)
#                 x2, y2 = x1 + (canvas_size // cols), y1 + (canvas_size // rows)
#                 item = page_data[idx]
#                 word = page_words[idx]

#                 # Draw the main square
#                 if zoomed.get():  # Zoomed mode: Use only the first color to fill the entire square
#                     color = item[0] if isinstance(item, list) else item
#                     canvas.create_rectangle(
#                         x1, y1, x2, y2, fill=color, width=2, outline="black"
#                     )
#                 else:  # Normal mode: Divide the square for multiple colors
#                     if isinstance(item, str):  # Single color
#                         canvas.create_rectangle(
#                             x1, y1, x2, y2, fill=item, width=2, outline="black"
#                         )
#                     elif isinstance(item, list):  # Multiple colors
#                         num_colors = len(item)
#                         sub_cell_width = (x2 - x1) / num_colors
#                         for k, color in enumerate(item):
#                             sub_x1 = x1 + k * sub_cell_width
#                             sub_x2 = sub_x1 + sub_cell_width
#                             canvas.create_rectangle(
#                                 sub_x1, y1, sub_x2, y2, fill=color, width=2, outline="black"
#                             )
#                 if show_words.get():
#                     canvas.create_text(
#                         (x1 + x2) / 2,
#                         (y1 + y2) / 2 - 16,
#                         fill="white",
#                         font="Times 16 italic bold",
#                         text=word,
#                     )
#                     canvas.create_text(
#                         (x1 + x2) / 2,
#                         (y1 + y2) / 2 + 16,
#                         fill="black",
#                         font="Times 16 italic bold",
#                         text=word,
#                     )
#                 if draw_patterns.get():
#                     draw_arrows_or_box(i, j, idx)

#     # Buttons for navigation
#     def next_page():
#         if (current_page.get() + 1) * items_per_page < len(grid_data):
#             current_page.set(current_page.get() + 1)
#             redraw_canvas()

#     def previous_page():
#         if current_page.get() > 0:
#             current_page.set(current_page.get() - 1)
#             redraw_canvas()

#     def toggle_zoom():
#         zoomed.set(not zoomed.get())
#         redraw_canvas()

#     def toggle_show_words():
#         show_words.set(not show_words.get())
#         redraw_canvas()

#     def toggle_draw_patterns():
#         draw_patterns.set(not draw_patterns.get())
#         redraw_canvas()

#     def go_to_input_frame():
#         frame.destroy()
#         create_input_frame(root, canvas_size)

#     prev_button = tk.Button(frame, text="<- Previous", command=previous_page)
#     next_button = tk.Button(frame, text="Next ->", command=next_page)
#     zoom_button = tk.Button(frame, text="🔍 Zoom +/-", command=toggle_zoom)
#     show_words_button = tk.Button(frame, text="Show Words", command=toggle_show_words)
#     patterns_button = tk.Button(frame, text="Draw Patterns", command=toggle_draw_patterns)
#     close_button = tk.Button(frame, text="New Song", command=go_to_input_frame)

#     prev_button.grid(row=1, column=0, pady=10, padx=10)
#     zoom_button.grid(row=1, column=1, pady=10, padx=10)
#     show_words_button.grid(row=2, column=1, pady=10, padx=10)
#     next_button.grid(row=1, column=2, pady=10, padx=10)
#     patterns_button.grid(row=2, column=0, pady=10, padx=10)
#     close_button.grid(row=2, column=2, pady=10, padx=10)

#     # Initial draw and resizing
#     root.bind("<Configure>", redraw_canvas)
#     redraw_canvas()

# # Example usage
# def process_input(song, artist):
#     # Combine song and artist, then split into words
#     original,lyrics, code, colors,colorsArray,deepCode,deepColors,deepColorsArray = get_lyrics(song, artist)
#     lyrics=lyrics.replace('\n'," ")
#     lyrics=re.sub(r"\[.*?\]",'',lyrics)
#     # Filter out words composed only of vowels
#     split_words=lyrics.split()

#     vowels = set("aeiouAEIOU")
#     split_words = list(filter(lambda x: not set(x).issubset(vowels) and x.isalpha(), split_words))
#     print(split_words)
#     class WordClass:
#         def __init__(self, word, code):
#             self.word = word
#             self.code = code

#     frames = []  # List to hold frames
#     chunk_size = 49

#     # Ensure the code_string has enough numbers for all words
#     word_codes = list(code[:len(split_words)])  # Take only as many codes as there are words

#     # Create frames of 49 words and their codes
#     for i in range(0, len(split_words), chunk_size):
#         chunk_words = split_words[i:i + chunk_size]
#         chunk_codes = word_codes[i:i + chunk_size]
#         frame = [WordClass(word, int(code)) for word, code in zip(chunk_words, chunk_codes)]
#         frames.append(frame)

#     # Return the deepColorsArray, split_words, and frames
#     return deepColorsArray, split_words, frames
# def create_input_frame(root, canvas_size):
#     frame = tk.Frame(root)
#     frame.pack()

#     tk.Label(frame, text="Song Name:").grid(row=0, column=0)
#     song_entry = tk.Entry(frame)
#     song_entry.grid(row=0, column=1)

#     tk.Label(frame, text="Artist Name:").grid(row=1, column=0)
#     artist_entry = tk.Entry(frame)
#     artist_entry.grid(row=1, column=1)

#     def submit():
#         song = song_entry.get()
#         artist = artist_entry.get()
#         grid_data, grid_words = process_input(song, artist)
#         frame.destroy()  # Remove input frame
#         create_color_grid(root, canvas_size, grid_data, grid_words)  # Call function 2

#     submit_button = tk.Button(frame, text="Submit", command=submit)
#     submit_button.grid(row=2, column=1)

# if __name__ == "__main__":
#     root = tk.Tk()
#     root.title("Grid Input Example")
#     canvas_size = 750
#     create_input_frame(root, canvas_size)
#     root.mainloop()

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
    deepColorsArray = []  # Example: Replace with your logic
    return deepColorsArray, split_words

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
    deepColorsArray, split_words = process_input(song, artist)
    return jsonify({"colors": deepColorsArray, "words": split_words})

if __name__ == "__main__":
    app.run(debug=True)