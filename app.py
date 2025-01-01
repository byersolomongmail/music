import os
import sqlite3
import re
os.environ["JOBLIB_TEMP_FOLDER"] = "/tmp"
from flask import Flask, request, render_template, jsonify
import re
app = Flask(__name__)

def process_input(song, artist):
    # Fetch data from the database
    result = get_lyrics_from_db(song, artist)

    if not result:
        raise ValueError("No data found for the given song and artist")

    # Unpack relevant fields from the result tuple
    (
        _id, title, tag, artist, year, views, features, lyrics, 
        tranlitLyrics, originalLyrics, code, colors, colorsArray, 
        deepCode, deepColors, deepColorsArray, json, language
    ) = result

    # Clean up the lyrics
    if lyrics:
        lyrics = lyrics.replace('\n', " ")
        lyrics = re.sub(r"\[.*?\]", '', lyrics)  # Remove content inside square brackets

    # Split lyrics into words and filter out words composed only of vowels
    split_words = lyrics.split() if lyrics else []
    vowels = set("aeiouAEIOU")
    split_words = list(filter(lambda x: not set(x).issubset(vowels) and x.isalpha(), split_words))

    # Return the processed data
    return originalLyrics, lyrics, code, colors, colorsArray, deepCode, deepColors, deepColorsArray, split_words



DB_NAME = "lyrics_processing.db"

def get_lyrics_from_db(song, artist=None):
    """Fetch lyrics from the database for a given song and optionally an artist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    try:
        # Build the query to select all the relevant columns
        if artist:
            cursor.execute("""
                SELECT 
                    id, title, tag, artist, year, views, features, lyrics, 
                    tranlitLyrics, originalLyrics, code, colors, colorsArray, 
                    deepCode, deepColors, deepColorsArray, json, language
                FROM processed_lyrics 
                WHERE title = ? AND artist = ?
            """, (song, artist))
        else:
            cursor.execute("""
                SELECT 
                    id, title, tag, artist, year, views, features, lyrics, 
                    tranlitLyrics, originalLyrics, code, colors, colorsArray, 
                    deepCode, deepColors, deepColorsArray, json, language
                FROM processed_lyrics 
                WHERE title = ?
            """, (song,))
        
        # Fetch the first matching record
        result = cursor.fetchone()

        # Return the result directly
        return result if result else None
    finally:
        conn.close()

def autocomplete_artist(partial_artist):
    """Fetch a list of artists matching the partial input."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT DISTINCT artist FROM processed_lyrics
            WHERE artist LIKE ?
            ORDER BY artist ASC
            LIMIT 10
        """, (f"%{partial_artist}%",))
        results = cursor.fetchall()
        return [row[0] for row in results]
    finally:
        conn.close()

def autocomplete_song(partial_song):
    """Fetch a list of songs matching the partial input."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT DISTINCT title FROM processed_lyrics
            WHERE title LIKE ?
            ORDER BY title ASC
            LIMIT 10
        """, (f"%{partial_song}%",))
        results = cursor.fetchall()
        return [row[0] for row in results]
    finally:
        conn.close()

@app.route("/")
def home():
    return render_template("index.html")  # Create an HTML file named "index.html" in a "templates" folder

@app.route("/process", methods=["POST"])
def process():
    data = request.json
    song = data.get("song")
    artist = data.get("artist") if data.get("artist") != "" else None
    if not song:
        return jsonify({"error": "Song title is required"}), 400

    # Process input
    original, lyrics, code, colors, colorsArray, deepCode, deepColors, deepColorsArray, split_words = process_input(song, artist)
    return jsonify({"colors": deepColorsArray, "words": split_words, "original":original,"lyrics": lyrics, "code": code, "stringcolors": colors, "colorsArray": colorsArray, "deepCode": deepCode, "deepColors": deepColors})
@app.route("/suggestions", methods=["GET"])
def suggest():
    suggestion_type = request.args.get("type", "").lower()
    query = request.args.get("query", "")

    if not query:
        return jsonify({"error": "Query parameter is required"}), 400

    if suggestion_type == "song":
        suggestions = autocomplete_song(query)
        return jsonify({"suggestions": suggestions})

    if suggestion_type == "artist":
        suggestions = autocomplete_artist(query)
        return jsonify({"suggestions": suggestions})

    return jsonify({"error": "Invalid type parameter. Use 'song' or 'artist'."}), 400


if __name__ == "__main__":
    app.run(debug=True)