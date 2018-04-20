import flask
import gallery

from common import app
from google.apputils import app as gapp


class HomeAutomationApp(app.App):
  def __init__(self, *args, **kwargs):
    super(HomeAutomationApp, self).__init__(__name__, *args, **kwargs)
    self.init_logging('./')

    self._app = flask.Flask(__name__)
    self._app.config['TEMPLATES_AUTO_RELOAD'] = True
    self._app.add_url_rule('/', view_func=self._index)
    self._app.add_url_rule('/gallery/next', view_func=self._next_image)

    self._gallery = gallery.GoogleDriveGallery(
        folder_id='0BwbugoG95MdfSmVRQ3NBNXhQMkE')
    self._gallery.start()

  def run(self):
    self._app.run()

  def close(self):
    self._gallery.close()
    super(HomeAutomationApp, self).close()

  def _index(self):
    return flask.render_template('index.html')

  def _next_image(self):
    filepath = self._gallery.next_image()
    filepath = filepath.lstrip('.')
    return flask.jsonify({'path': filepath})


def main(argv):
  with HomeAutomationApp() as ha:
    ha.run()


if __name__ == '__main__':
  gapp.run()