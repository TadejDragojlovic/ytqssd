from flask import Flask
from flask import request, render_template, send_file

from main import getLinksYTMUSIC, _downloadSongs
import shutil

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST']) # Home page
def index():
    if request.method == 'POST':
        return render_template('downloading.html')
    else:
        return render_template('index.html')


@app.route('/download', methods=['GET', 'POST']) # Download page
def download():
    song_input = request.form['song_input'].split('\n')

    song_links = getLinksYTMUSIC(song_input)

    selected_format = request.form['format_selector']

    # main function to download the song
    _downloadSongs(song_links, format=selected_format)

    # Zipping the folder
    shutil.make_archive('songz', 'zip', 'songs/')

    # testing the download function
    path = "songz.zip"
    return send_file(path, as_attachment=True)

# Main driver function
if __name__ == '__main__':
    app.run()
