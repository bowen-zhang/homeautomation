from __future__ import print_function

import os
import random
import threading

from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

from common import pattern


class ImageMetadata(object):
  def __init__(self, id, name):
    self._id = id
    self._name = name

  @property
  def id(self):
    return self._id

  @property
  def name(self):
    return self._name


class Gallery(pattern.Closable, pattern.Logger):

  _CACHE_PATH = os.path.join('./static/gallery-cache')
  _REFRESH_INTERVAL = 15 * 60  # sec

  def __init__(self, *args, **kwargs):
    super(Gallery, self).__init__(*args, **kwargs)
    self._images = []
    self._timer = None
    if not os.path.isdir(self._CACHE_PATH):
      os.makedirs(self._CACHE_PATH)

  def start(self):
    pass

  def close(self):
    if self._timer:
      self._timer.cancel()
      self._timer = None

  def get_image_metadata_list(self):
    pass

  def get_image(self, id):
    pass

  def next_image(self):
    if self._images is None:
      self._refresh()
    if not self._images:
        return None

    image = random.choice(self._images)
    self.logger.debug('Next image: {0}'.format(image.id))
    filepath = self._get_filepath(image)
    if not os.path.isfile(filepath):
      self.logger.debug('Downloading image...')
      content = self.get_image(image.id)
      with open(filepath, 'w') as f:
        f.write(content)

    return filepath

  def _refresh(self):
    self.logger.info('Refreshing gallery...')

    self._images = list(self.get_image_metadata_list())
    self.logger.debug('{0} images found.'.format(len(self._images)))

    image_ids = set(map(lambda x: x.id, self._images))
    for filename in os.listdir(self._CACHE_PATH):
      image_id = os.path.basename(filename)
      if image_id not in image_ids:
        filepath = os.path.join(self._CACHE_PATH, filename)
        os.remove(filepath)

    self._timer = threading.Timer(self._REFRESH_INTERVAL, self._refresh)
    self._timer.start()

  def _get_filepath(self, image):
    return os.path.join(self._CACHE_PATH,
                        image.id + os.path.splitext(image.name)[1])


class GoogleDriveGallery(Gallery):

  _SCOPES = 'https://www.googleapis.com/auth/drive.readonly'

  def __init__(self, folder_id, *args, **kwargs):
    super(GoogleDriveGallery, self).__init__(*args, **kwargs)
    self._folder_id = folder_id

    store = file.Storage('credentials.json')
    creds = store.get()
    if not creds or creds.invalid:
      flow = client.flow_from_clientsecrets('client_secret.json', self._SCOPES)
      creds = tools.run_flow(flow, store)
    self._service = build('drive', 'v3', http=creds.authorize(Http()))

  def get_image_metadata_list(self):
    results = self._service.files().list(
        q='\'{0}\' in parents'.format(self._folder_id),
        pageSize=1000).execute()
    items = results.get('files', [])
    for item in items:
      yield ImageMetadata(id=item['id'], name=item['name'])

  def get_image(self, id):
    request = self._service.files().get_media(fileId=id)
    return request.execute()


if __name__ == '__main__':
  gallery = GoogleDriveGallery(folder_id='0BwbugoG95MdfSmVRQ3NBNXhQMkE')
