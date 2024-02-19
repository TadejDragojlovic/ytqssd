from flask import Flask
from flask import request, render_template, send_file

from main import gatherLinks, downloadSongs, _search
import shutil
import time

app = Flask(__name__)

li = []

"""
TODO:
[app.py]
- figure out how to show the list (is results.html really needed?)
- clear local folder used to store downloaded songs and "songz.zip" after user is finished

[index.html]
- figure out where to put clear list button, currently greyed out
- showcase the list of songs on the rightside, make it collapsable?

[downloading.html]
- do I need this html template?
- inform the user that the data is being processed/downloaded

[static]
- match the fonts/font-sizes, and test if it is proportional ENOUGH
- split artist and song name when displaying results
- in index.html button "Go" is not aligned properly when zoomed in
"""

@app.route('/', methods=['GET', 'POST']) # Home page
def index_page():
    print("INDEX PAGE.\n")
    if request.method == 'POST':
        # this request is to display results of a given search query
        try:
            raw_results = _search(request.form['query'])
        except Exception as e:
            print("Error while searching for query. Error: ", e)
            return render_template('index.html')

        # number of results found
        print("Number of results found: %d\n" % len(raw_results))

        # this includes (video_id, name, artist, thumbnail)
        clean_results = []
        for i, result in enumerate(raw_results):
            artist = result['artists'][0]['name']
            name = result['title']
            _id = result['videoId']
            thumbnail = f"https://img.youtube.com/vi/{_id}/hqdefault.jpg"
            clean_results.append([artist, name, _id, thumbnail])

        print("Showing results.\n")
        return render_template('results.html', CLEAN_RESULTS=clean_results)
    else:
        return render_template('index.html')


# Download page
@app.route('/download', methods=['GET', 'POST'])
def download():
    start = time.time()

    song_input = request.form['song_input'].split('\n')

    try:
        song_links = gatherLinks(song_input)

        # main function to download the song
        downloadSongs(song_links)

        # Zipping the folder (we need to store it locally, so we can send it out zipped)
        shutil.make_archive('songz', 'zip', 'songs/')

        print("Finished `main()` in : %f" % (time.time() - start))

        path = "songz.zip"

        try:
            return send_file(path)
        except Exception as e:
            return str(e)

    except Exception as e:
        # Case if the list is empty
        if(len(song_input) == 1):
            if(song_input[0] == ''):
                return render_template("quick-list.html")

        # Different unknown error
        return str(e)


# Add to list
@app.route('/add', methods=['GET'])
def add_to_list():
    if(request.method == "GET"):
        artist = request.args.get("artist-name")
        song = request.args.get("song-name")
        li.append([artist, song])

        # TODO: Make it stay on the page when submitting the request
        print("LIST: \n", li)
        return render_template("index.html", LIST=li)
    else:
        return "Error"


@app.route('/clear', methods=['GET'])
def clear_list():
    if(request.method == "GET"):
        global li
        li=[]
        return render_template("index.html")
    else:
        return "Error"

@app.route('/quick-list', methods=['GET', 'POST'])
def text_quick_list():
    return render_template("quick-list.html")


# Main driver function
if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')