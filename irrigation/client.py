import grpc

from google.protobuf import empty_pb2

from irrigation.proto import irrigation_pb2
from irrigation.proto import irrigation_pb2_grpc


def main():
  channel = grpc.insecure_channel('127.0.0.1:17051')
  stub = irrigation_pb2_grpc.IrrigationServiceStub(channel)
  print(stub.GetConfig(empty_pb2.Empty()))
  while True:
    print('a. Submit Tasks\n'
          'b. Current Task\n'
          'c. List Tasks\n'
          'd. Exit')
    choice = input('?')
    if choice == 'a':
      station_id = int(input('Station id:'))
      duration_sec = int(input('Duration (sec):'))
      print('Run station {0} for {1} sec.'.format(station_id, duration_sec))
      stub.SubmitTasks(irrigation_pb2.TaskList(
          tasks=[
              irrigation_pb2.Task(station_id=station_id,
                                  duration_sec=duration_sec)
          ]))
    elif choice == 'b':
      print(stub.GetCurrentTask(empty_pb2.Empty()))
    elif choice == 'c':
      print(stub.GetPendingTasks(empty_pb2.Empty()))
    elif choice == 'd':
      break


if __name__ == '__main__':
  main()
