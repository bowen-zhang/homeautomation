import threading
import subprocess

from third_party.common import pattern


class Ffmpeg(pattern.Logger):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self._probesize = 32
    self._input_reader = None
    self._input_filepath = None
    self._input_container = None
    self._input_vcodec = None
    self._input_pixel_format = None
    self._input_framerate = None
    self._input_size = None
    self._map = None
    self._output_writer = None
    self._output_filepath = None
    self._output_container = None
    self._output_vcodec = None
    self._output_pixel_format = None
    self._proc = None
    self._input_thread = None
    self._output_thread = None
    self._abort = threading.Event()

  def from_file(self, filepath, container=None, vcodec=None, pixel_format=None):
    self._input_reader = None
    self._input_filepath = filepath
    self._input_container = container
    self._input_vcodec = vcodec
    self._input_pixel_format = pixel_format
    return self

  def from_reader(self, reader, container=None, vcodec=None, pixel_format=None, framerate=None, size=None):
    self._input_reader = reader
    self._input_filepath = None
    self._input_container = container
    self._input_vcodec = vcodec
    self._input_pixel_format = pixel_format
    self._input_framerate = framerate
    self._input_size = size
    return self

  def to_file(self, filepath, container=None, vcodec=None, pixel_format=None):
    self._output_writer = None
    self._output_filepath = filepath
    self._output_container = container
    self._output_vcodec = vcodec
    self._output_pixel_format = pixel_format
    return self

  def to_writer(self, writer, container=None, vcodec=None, pixel_format=None):
    self._output_writer = writer
    self._output_filepath = None
    self._output_container = container
    self._output_vcodec = vcodec
    self._output_pixel_format = pixel_format
    return self

  def map(self, value):
    self._map = value
    return self

  def start(self):
    cmd = ['ffmpeg']
    if self._probesize is not None:
      cmd.append('-probesize')
      cmd.append(str(self._probesize))
    if self._input_container:
      cmd.append('-f')
      cmd.append(self._input_container)
    if self._input_vcodec:
      cmd.append('-vcodec')
      cmd.append(self._input_vcodec)
    if self._input_pixel_format:
      cmd.append('-pix_fmt')
      cmd.append(self._input_pixel_format)
    if self._input_framerate:
      cmd.append('-r')
      cmd.append(str(self._input_framerate))
    if self._input_size:
      cmd.append('-s')
      cmd.append('{0}x{1}'.format(self._input_size[0], self._input_size[1]))
    if self._input_filepath:
      cmd.append('-i')
      cmd.append(self._input_filepath)
    else:
      cmd.append('-i')
      cmd.append('pipe:')
    if self._map:
      cmd.append('-map')
      cmd.append(self._map)
    if self._output_container:
      cmd.append('-f')
      cmd.append(self._output_container)
    if self._output_vcodec:
      cmd.append('-vcodec')
      cmd.append(self._output_vcodec)
    if self._output_pixel_format:
      cmd.append('-pix_fmt')
      cmd.append(self._output_pixel_format)
    if self._output_filepath:
      cmd.append(self._output_filepath)
    else:
      cmd.append('pipe:')

    self._abort.clear()
    self._proc = subprocess.Popen(cmd,
                                  bufsize=-1,
                                  stdin=None if self._input_filepath else subprocess.PIPE,
                                  stdout=None if self._output_filepath else subprocess.PIPE,
                                  stderr=subprocess.PIPE)

    if self._input_reader:
      self._input_thread = threading.Thread(
          target=self._pipe_from_reader, daemon=True)
      self._input_thread.start()
    else:
      self._input_thread = None
    if self._output_writer:
      self._output_thread = threading.Thread(
          target=self._pipe_to_writer, daemon=True)
      self._output_thread.start()
    else:
      self._output_thread = None

  def send_input(self, data):
    self._proc.stdin.write(data)

  def stop(self):
    self._abort.set()

    if self._input_reader:
      if self._input_thread:
        self._input_thread.join()
        self._input_thread = None
    elif self._input_filepath:
      if self._proc:
        self._proc.terminate()
    else:
      if self._proc:
        self._proc.stdin.close()

    if self._output_writer:
      if self._output_thread:
        self._output_thread.join()
        self._output_thread = None
    else:  # output to file
      if self._proc:
        self._proc.wait()

    if self._proc:
      try:
        self._proc.terminate()
      except:
        pass
      self._proc = None

  def _pipe_from_reader(self):
    for data in self._input_reader(self._abort):
      self._proc.stdin.write(data)
    self._proc.stdin.close()

  def _pipe_to_writer(self):
    while True:
      succeed = self._output_writer(self._proc.stdout)
      if not succeed and self._proc.poll() is not None:
        break
