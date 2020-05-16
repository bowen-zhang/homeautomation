from third_party.common import app
from weather.libs import storage_lib


class SetupApp(app.App):
  def __init__(self):
    super().__init__(name='weather.setup')
    self.init_logging(log_path='/tmp')

  def run(self):
    storage = storage_lib.MongoStorage('weather')
    storage.create_indexes()


if __name__ == '__main__':
  app.start(SetupApp)
