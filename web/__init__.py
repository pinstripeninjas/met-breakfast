from flask import Flask, render_template
from modules import skewt, gfs_4_panel

def create_app():
    app = Flask(__name__)

    @app.route('/')
    def index():
        spinner = "./static/img/blocks-shuffle-2.svg"
        return render_template('index.html', spinner=spinner)

    @app.route('/img/<img_name>')
    def return_img(img_name):
        if img_name == 'skewT':
            return skewt.draw()
        elif img_name == 'four_panel':
            return gfs_4_panel.draw()

    return app