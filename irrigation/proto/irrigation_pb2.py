# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: irrigation.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='irrigation.proto',
  package='ha.irrigation',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=b'\n\x10irrigation.proto\x12\rha.irrigation\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x1bgoogle/protobuf/empty.proto\"C\n\x08Location\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0f\n\x07\x61\x64\x64ress\x18\x02 \x01(\t\x12\x0b\n\x03lat\x18\x03 \x01(\x02\x12\x0b\n\x03lon\x18\x04 \x01(\x02\"0\n\x07Station\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x0b\n\x03pin\x18\x03 \x01(\r\"\xa0\x01\n\nNaiveModel\x12/\n\x0blast_update\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x11\n\tamount_in\x18\x02 \x01(\x02\x12\x16\n\x0e\x66low_rate_inpm\x18\x03 \x01(\x02\x12\x17\n\x0fwater_amount_in\x18\x04 \x01(\x02\x12\x1d\n\x15\x63onsumption_rate_inpd\x18\x05 \x01(\x02\"\xaf\x01\n\x06\x43onfig\x12)\n\x08location\x18\x01 \x01(\x0b\x32\x17.ha.irrigation.Location\x12(\n\x08stations\x18\x02 \x03(\x0b\x32\x16.ha.irrigation.Station\x12\x15\n\rschedule_hour\x18\x03 \x01(\r\x12\x30\n\x0bnaive_model\x18\n \x01(\x0b\x32\x19.ha.irrigation.NaiveModelH\x00\x42\x07\n\x05model\".\n\x08TaskList\x12\"\n\x05tasks\x18\x01 \x03(\x0b\x32\x13.ha.irrigation.Task\"0\n\x04Task\x12\x12\n\nstation_id\x18\x01 \x01(\x05\x12\x14\n\x0c\x64uration_sec\x18\x02 \x01(\x05\"D\n\x06Status\x12\x1a\n\x12running_station_id\x18\x01 \x01(\x05\x12\x1e\n\x16remaining_duration_sec\x18\x02 \x01(\x05\x32\x9a\x02\n\x11IrrigationService\x12<\n\tGetConfig\x12\x16.google.protobuf.Empty\x1a\x15.ha.irrigation.Config\"\x00\x12@\n\x0bSubmitTasks\x12\x17.ha.irrigation.TaskList\x1a\x16.google.protobuf.Empty\"\x00\x12?\n\x0eGetCurrentTask\x12\x16.google.protobuf.Empty\x1a\x13.ha.irrigation.Task\"\x00\x12\x44\n\x0fGetPendingTasks\x12\x16.google.protobuf.Empty\x1a\x17.ha.irrigation.TaskList\"\x00\x62\x06proto3'
  ,
  dependencies=[google_dot_protobuf_dot_timestamp__pb2.DESCRIPTOR,google_dot_protobuf_dot_empty__pb2.DESCRIPTOR,])




_LOCATION = _descriptor.Descriptor(
  name='Location',
  full_name='ha.irrigation.Location',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='ha.irrigation.Location.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='address', full_name='ha.irrigation.Location.address', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='lat', full_name='ha.irrigation.Location.lat', index=2,
      number=3, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='lon', full_name='ha.irrigation.Location.lon', index=3,
      number=4, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=97,
  serialized_end=164,
)


_STATION = _descriptor.Descriptor(
  name='Station',
  full_name='ha.irrigation.Station',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='ha.irrigation.Station.id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='name', full_name='ha.irrigation.Station.name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='pin', full_name='ha.irrigation.Station.pin', index=2,
      number=3, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=166,
  serialized_end=214,
)


_NAIVEMODEL = _descriptor.Descriptor(
  name='NaiveModel',
  full_name='ha.irrigation.NaiveModel',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='last_update', full_name='ha.irrigation.NaiveModel.last_update', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='amount_in', full_name='ha.irrigation.NaiveModel.amount_in', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='flow_rate_inpm', full_name='ha.irrigation.NaiveModel.flow_rate_inpm', index=2,
      number=3, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='water_amount_in', full_name='ha.irrigation.NaiveModel.water_amount_in', index=3,
      number=4, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='consumption_rate_inpd', full_name='ha.irrigation.NaiveModel.consumption_rate_inpd', index=4,
      number=5, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=217,
  serialized_end=377,
)


_CONFIG = _descriptor.Descriptor(
  name='Config',
  full_name='ha.irrigation.Config',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='location', full_name='ha.irrigation.Config.location', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='stations', full_name='ha.irrigation.Config.stations', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='schedule_hour', full_name='ha.irrigation.Config.schedule_hour', index=2,
      number=3, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='naive_model', full_name='ha.irrigation.Config.naive_model', index=3,
      number=10, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='model', full_name='ha.irrigation.Config.model',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=380,
  serialized_end=555,
)


_TASKLIST = _descriptor.Descriptor(
  name='TaskList',
  full_name='ha.irrigation.TaskList',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='tasks', full_name='ha.irrigation.TaskList.tasks', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=557,
  serialized_end=603,
)


_TASK = _descriptor.Descriptor(
  name='Task',
  full_name='ha.irrigation.Task',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='station_id', full_name='ha.irrigation.Task.station_id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='duration_sec', full_name='ha.irrigation.Task.duration_sec', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=605,
  serialized_end=653,
)


_STATUS = _descriptor.Descriptor(
  name='Status',
  full_name='ha.irrigation.Status',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='running_station_id', full_name='ha.irrigation.Status.running_station_id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='remaining_duration_sec', full_name='ha.irrigation.Status.remaining_duration_sec', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=655,
  serialized_end=723,
)

_NAIVEMODEL.fields_by_name['last_update'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_CONFIG.fields_by_name['location'].message_type = _LOCATION
_CONFIG.fields_by_name['stations'].message_type = _STATION
_CONFIG.fields_by_name['naive_model'].message_type = _NAIVEMODEL
_CONFIG.oneofs_by_name['model'].fields.append(
  _CONFIG.fields_by_name['naive_model'])
_CONFIG.fields_by_name['naive_model'].containing_oneof = _CONFIG.oneofs_by_name['model']
_TASKLIST.fields_by_name['tasks'].message_type = _TASK
DESCRIPTOR.message_types_by_name['Location'] = _LOCATION
DESCRIPTOR.message_types_by_name['Station'] = _STATION
DESCRIPTOR.message_types_by_name['NaiveModel'] = _NAIVEMODEL
DESCRIPTOR.message_types_by_name['Config'] = _CONFIG
DESCRIPTOR.message_types_by_name['TaskList'] = _TASKLIST
DESCRIPTOR.message_types_by_name['Task'] = _TASK
DESCRIPTOR.message_types_by_name['Status'] = _STATUS
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Location = _reflection.GeneratedProtocolMessageType('Location', (_message.Message,), {
  'DESCRIPTOR' : _LOCATION,
  '__module__' : 'irrigation_pb2'
  # @@protoc_insertion_point(class_scope:ha.irrigation.Location)
  })
_sym_db.RegisterMessage(Location)

Station = _reflection.GeneratedProtocolMessageType('Station', (_message.Message,), {
  'DESCRIPTOR' : _STATION,
  '__module__' : 'irrigation_pb2'
  # @@protoc_insertion_point(class_scope:ha.irrigation.Station)
  })
_sym_db.RegisterMessage(Station)

NaiveModel = _reflection.GeneratedProtocolMessageType('NaiveModel', (_message.Message,), {
  'DESCRIPTOR' : _NAIVEMODEL,
  '__module__' : 'irrigation_pb2'
  # @@protoc_insertion_point(class_scope:ha.irrigation.NaiveModel)
  })
_sym_db.RegisterMessage(NaiveModel)

Config = _reflection.GeneratedProtocolMessageType('Config', (_message.Message,), {
  'DESCRIPTOR' : _CONFIG,
  '__module__' : 'irrigation_pb2'
  # @@protoc_insertion_point(class_scope:ha.irrigation.Config)
  })
_sym_db.RegisterMessage(Config)

TaskList = _reflection.GeneratedProtocolMessageType('TaskList', (_message.Message,), {
  'DESCRIPTOR' : _TASKLIST,
  '__module__' : 'irrigation_pb2'
  # @@protoc_insertion_point(class_scope:ha.irrigation.TaskList)
  })
_sym_db.RegisterMessage(TaskList)

Task = _reflection.GeneratedProtocolMessageType('Task', (_message.Message,), {
  'DESCRIPTOR' : _TASK,
  '__module__' : 'irrigation_pb2'
  # @@protoc_insertion_point(class_scope:ha.irrigation.Task)
  })
_sym_db.RegisterMessage(Task)

Status = _reflection.GeneratedProtocolMessageType('Status', (_message.Message,), {
  'DESCRIPTOR' : _STATUS,
  '__module__' : 'irrigation_pb2'
  # @@protoc_insertion_point(class_scope:ha.irrigation.Status)
  })
_sym_db.RegisterMessage(Status)



_IRRIGATIONSERVICE = _descriptor.ServiceDescriptor(
  name='IrrigationService',
  full_name='ha.irrigation.IrrigationService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=726,
  serialized_end=1008,
  methods=[
  _descriptor.MethodDescriptor(
    name='GetConfig',
    full_name='ha.irrigation.IrrigationService.GetConfig',
    index=0,
    containing_service=None,
    input_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    output_type=_CONFIG,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='SubmitTasks',
    full_name='ha.irrigation.IrrigationService.SubmitTasks',
    index=1,
    containing_service=None,
    input_type=_TASKLIST,
    output_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='GetCurrentTask',
    full_name='ha.irrigation.IrrigationService.GetCurrentTask',
    index=2,
    containing_service=None,
    input_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    output_type=_TASK,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='GetPendingTasks',
    full_name='ha.irrigation.IrrigationService.GetPendingTasks',
    index=3,
    containing_service=None,
    input_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    output_type=_TASKLIST,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_IRRIGATIONSERVICE)

DESCRIPTOR.services_by_name['IrrigationService'] = _IRRIGATIONSERVICE

# @@protoc_insertion_point(module_scope)
