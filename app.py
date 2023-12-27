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
- figure out why i always get 20 results even tho limit is 5 (line 26)
- clear local folder used to store downloaded songs and "songz.zip" after user is finished

[index.html]
- refactor the index file, so we can easily expand on it (don't include search box by default)
- showcase the list of songs on the rightside, make it collapsable?

[downloading.html]
- do I need this html template?
- inform the user that the data is being processed/downloaded

[static]
- match the fonts/font-sizes, and test if it is proportional ENOUGH
"""

@app.route('/', methods=['GET', 'POST']) # Home page
def index_page():
    print("INDEX PAGE.\n")
    if request.method == 'POST':
        # this request is to display results of a given search query
        raw_results = _search(request.form['query'])

        # number of results found
        print("Number of results found: %d\n" % len(raw_results))

        # this includes (video_id, name, artist, thumbnail)
        clean_results = []
        i=0
        for result in raw_results:
            if(i>9):
                break
            artist = result['artists'][0]['name']
            name = result['title']
            _id = result['videoId']
            thumbnail = f"https://img.youtube.com/vi/{_id}/hqdefault.jpg"
            clean_results.append([artist, name, _id, thumbnail])
            i+=1

        print("Showing results.\n")
        return render_template('results.html', CLEAN_RESULTS=clean_results)
    else:
        return render_template('index.html')


# Download page
@app.route('/download', methods=['GET', 'POST'])
def download():
    start = time.time()

    song_input = request.form['song_input'].split('\n')

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


# Add to list
@app.route('/add', methods=['GET'])
def add_to_list():
    if(request.method == "GET"):
        artist = request.args.get("artist-name")
        song = request.args.get("song-name")
        li.append([artist, song])

        # TODO: Make it stay on the page when submitting the request
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