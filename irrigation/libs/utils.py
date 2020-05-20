def is_in_any_time_window(dt, windows):
  for window in windows:
    if is_in_time_window(dt, window):
      return True
  return False


def is_in_time_window(dt, window):
  if window.from_hour < window.to_hour:
    if window.from_hour <= dt.hour and dt.hour < window.to_hour:
      return True
  else:
    if dt.hour >= window.from_hour or dt.hour < window.to_hour:
      return True
  return False
