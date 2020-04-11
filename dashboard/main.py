from absl import app as absl_app
import flask

from dashboard import gallery
from third_party.common import app


GOOGLE_DRIVE_FOLDER_ID = '1eRR7gsmM6ojJl7buVhqYXLJHOqLcr9rz'


class HomeAutomationApp(app.App):
  def __init__(self, *args, **kwargs):
    super(HomeAutomationApp, self).__init__(__name__, *args, **kwargs)
    self.init_logging('./')

    self._web = flask.Flask(__name__,
                            template_folder='./web',
                            static_url_path='',
                            static_folder='./web')
    self._web.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    self._web.config['TEMPLATES_AUTO_RELOAD'] = True
    self._web.add_url_rule('/', view_func=self._index)
    self._web.add_url_rule('/gallery/next', view_func=self._next_image)

    self._gallery = gallery.GoogleDriveGallery(
        folder_id=GOOGLE_DRIVE_FOLDER_ID)
    self._gallery.start()

  def run(self):
    self._web.run(host='0.0.0.0', port=6250, debug=True)

  def close(self):
    self._gallery.close()
    super(HomeAutomationApp, self).close()

  def _index(self):
    return self._web.send_static_file('index.html')

  def _next_image(self):
    filepath = self._gallery.next_image()
    filepath = filepath.lstrip('.')
    return flask.jsonify({'path': filepath})


def main(argv):
  with HomeAutomationApp() as ha:
    ha.run()


if __name__ == '__main__':
  absl_app.run(main)
