import sys

from shared.proto import common_pb2
from weather.libs import storage_lib


def main():
  zipcode = sys.argv[1]
  storage = storage_lib.MongoStorage(database_name='weather')
  storage.locations.save(common_pb2.Location(zipcode=zipcode))


if __name__ == '__main__':
  main()
