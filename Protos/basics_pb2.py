# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: basics.proto
# Protobuf Python Version: 5.28.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    28,
    1,
    '',
    'basics.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import enums_pb2 as enums__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0c\x62\x61sics.proto\x12\x14ScriptsOfTributeGRPC\x1a\x0b\x65nums.proto\"\xd4\x02\n\x04Move\x12\x30\n\x05\x42\x61sic\x18\x01 \x01(\x0b\x32\x1f.ScriptsOfTributeGRPC.BasicMoveH\x00\x12\x38\n\x08\x43\x61rdMove\x18\x02 \x01(\x0b\x32$.ScriptsOfTributeGRPC.SimpleCardMoveH\x00\x12<\n\nPatronMove\x18\x03 \x01(\x0b\x32&.ScriptsOfTributeGRPC.SimplePatronMoveH\x00\x12H\n\x0e\x43\x61rdChoiceMove\x18\x04 \x01(\x0b\x32..ScriptsOfTributeGRPC.MakeChoiceMoveUniqueCardH\x00\x12L\n\x10\x45\x66\x66\x65\x63tChoiceMove\x18\x05 \x01(\x0b\x32\x30.ScriptsOfTributeGRPC.MakeChoiceMoveUniqueEffectH\x00\x42\n\n\x08moveType\"<\n\tBasicMove\x12/\n\x07\x63ommand\x18\x01 \x01(\x0e\x32\x1e.ScriptsOfTributeGRPC.MoveEnum\"W\n\x0eSimpleCardMove\x12/\n\x07\x63ommand\x18\x01 \x01(\x0e\x32\x1e.ScriptsOfTributeGRPC.MoveEnum\x12\x14\n\x0c\x63\x61rdUniqueId\x18\x02 \x01(\x05\"z\n\x10SimplePatronMove\x12/\n\x07\x63ommand\x18\x01 \x01(\x0e\x32\x1e.ScriptsOfTributeGRPC.MoveEnum\x12\x35\n\x08patronId\x18\x02 \x01(\x0e\x32#.ScriptsOfTributeGRPC.PatronIdProto\"c\n\x18MakeChoiceMoveUniqueCard\x12/\n\x07\x63ommand\x18\x01 \x01(\x0e\x32\x1e.ScriptsOfTributeGRPC.MoveEnum\x12\x16\n\x0e\x63\x61rdsUniqueIds\x18\x02 \x03(\x05\"^\n\x1aMakeChoiceMoveUniqueEffect\x12/\n\x07\x63ommand\x18\x01 \x01(\x0e\x32\x1e.ScriptsOfTributeGRPC.MoveEnum\x12\x0f\n\x07\x65\x66\x66\x65\x63ts\x18\x02 \x03(\t\"I\n\x0c\x45ndGameState\x12\x0e\n\x06winner\x18\x01 \x01(\t\x12\x0e\n\x06reason\x18\x02 \x01(\t\x12\x19\n\x11\x41\x64\x64itionalContext\x18\x03 \x01(\t\"\x8a\x01\n\x11PatronStatesProto\x12\x45\n\x07patrons\x18\x01 \x03(\x0b\x32\x34.ScriptsOfTributeGRPC.PatronStatesProto.PatronsEntry\x1a.\n\x0cPatronsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"\xd2\x01\n\x0fUniqueCardProto\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x31\n\x04\x64\x65\x63k\x18\x02 \x01(\x0e\x32#.ScriptsOfTributeGRPC.PatronIdProto\x12\x0c\n\x04\x63ost\x18\x03 \x01(\x05\x12\x31\n\x04type\x18\x04 \x01(\x0e\x32#.ScriptsOfTributeGRPC.CardTypeProto\x12\n\n\x02hp\x18\x05 \x01(\x05\x12\r\n\x05taunt\x18\x06 \x01(\x08\x12\x11\n\tunique_id\x18\x07 \x01(\x05\x12\x0f\n\x07\x65\x66\x66\x65\x63ts\x18\x08 \x03(\t\"\xf2\x03\n\x0bPlayerProto\x12\x38\n\tplayer_id\x18\x01 \x01(\x0e\x32%.ScriptsOfTributeGRPC.PlayerEnumProto\x12\x33\n\x04hand\x18\x02 \x03(\x0b\x32%.ScriptsOfTributeGRPC.UniqueCardProto\x12<\n\rcooldown_pile\x18\x03 \x03(\x0b\x32%.ScriptsOfTributeGRPC.UniqueCardProto\x12\x35\n\x06played\x18\x04 \x03(\x0b\x32%.ScriptsOfTributeGRPC.UniqueCardProto\x12\x43\n\x14known_upcoming_draws\x18\x05 \x03(\x0b\x32%.ScriptsOfTributeGRPC.UniqueCardProto\x12:\n\x06\x61gents\x18\x06 \x03(\x0b\x32*.ScriptsOfTributeGRPC.SerializedAgentProto\x12\r\n\x05power\x18\x07 \x01(\x05\x12\x14\n\x0cpatron_calls\x18\x08 \x01(\r\x12\r\n\x05\x63oins\x18\t \x01(\x05\x12\x10\n\x08prestige\x18\n \x01(\x05\x12\x38\n\tdraw_pile\x18\x0b \x03(\x0b\x32%.ScriptsOfTributeGRPC.UniqueCardProto\"\xeb\x02\n\x10\x45nemyPlayerProto\x12\x38\n\tplayer_id\x18\x01 \x01(\x0e\x32%.ScriptsOfTributeGRPC.PlayerEnumProto\x12:\n\x06\x61gents\x18\x02 \x03(\x0b\x32*.ScriptsOfTributeGRPC.SerializedAgentProto\x12\r\n\x05power\x18\x03 \x01(\x05\x12\r\n\x05\x63oins\x18\x04 \x01(\x05\x12\x10\n\x08prestige\x18\x05 \x01(\x05\x12<\n\rhand_and_draw\x18\x06 \x03(\x0b\x32%.ScriptsOfTributeGRPC.UniqueCardProto\x12\x35\n\x06played\x18\x07 \x03(\x0b\x32%.ScriptsOfTributeGRPC.UniqueCardProto\x12<\n\rcooldown_pile\x18\x08 \x03(\x0b\x32%.ScriptsOfTributeGRPC.UniqueCardProto\"~\n\x14SerializedAgentProto\x12\x11\n\tcurrentHP\x18\x01 \x01(\x05\x12@\n\x11representing_card\x18\x02 \x01(\x0b\x32%.ScriptsOfTributeGRPC.UniqueCardProto\x12\x11\n\tactivated\x18\x03 \x01(\x08\"\xa9\x02\n\x0b\x43hoiceProto\x12\x13\n\x0bmax_choices\x18\x01 \x01(\x05\x12\x13\n\x0bmin_choices\x18\x02 \x01(\x05\x12\x0f\n\x07\x63ontext\x18\x03 \x01(\t\x12\x18\n\x10\x63hoice_follow_up\x18\x04 \x01(\t\x12\x37\n\x04type\x18\x05 \x01(\x0e\x32).ScriptsOfTributeGRPC.ChoiceDataTypeProto\x12\x39\n\x0c\x63\x61rd_options\x18\x06 \x01(\x0b\x32!.ScriptsOfTributeGRPC.CardOptionsH\x00\x12=\n\x0e\x65\x66\x66\x65\x63t_options\x18\x07 \x01(\x0b\x32#.ScriptsOfTributeGRPC.EffectOptionsH\x00\x42\x12\n\x10possible_options\"L\n\x0b\x43\x61rdOptions\x12=\n\x0epossible_cards\x18\x01 \x03(\x0b\x32%.ScriptsOfTributeGRPC.UniqueCardProto\")\n\rEffectOptions\x12\x18\n\x10possible_effects\x18\x01 \x03(\tb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'basics_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_PATRONSTATESPROTO_PATRONSENTRY']._loaded_options = None
  _globals['_PATRONSTATESPROTO_PATRONSENTRY']._serialized_options = b'8\001'
  _globals['_MOVE']._serialized_start=52
  _globals['_MOVE']._serialized_end=392
  _globals['_BASICMOVE']._serialized_start=394
  _globals['_BASICMOVE']._serialized_end=454
  _globals['_SIMPLECARDMOVE']._serialized_start=456
  _globals['_SIMPLECARDMOVE']._serialized_end=543
  _globals['_SIMPLEPATRONMOVE']._serialized_start=545
  _globals['_SIMPLEPATRONMOVE']._serialized_end=667
  _globals['_MAKECHOICEMOVEUNIQUECARD']._serialized_start=669
  _globals['_MAKECHOICEMOVEUNIQUECARD']._serialized_end=768
  _globals['_MAKECHOICEMOVEUNIQUEEFFECT']._serialized_start=770
  _globals['_MAKECHOICEMOVEUNIQUEEFFECT']._serialized_end=864
  _globals['_ENDGAMESTATE']._serialized_start=866
  _globals['_ENDGAMESTATE']._serialized_end=939
  _globals['_PATRONSTATESPROTO']._serialized_start=942
  _globals['_PATRONSTATESPROTO']._serialized_end=1080
  _globals['_PATRONSTATESPROTO_PATRONSENTRY']._serialized_start=1034
  _globals['_PATRONSTATESPROTO_PATRONSENTRY']._serialized_end=1080
  _globals['_UNIQUECARDPROTO']._serialized_start=1083
  _globals['_UNIQUECARDPROTO']._serialized_end=1293
  _globals['_PLAYERPROTO']._serialized_start=1296
  _globals['_PLAYERPROTO']._serialized_end=1794
  _globals['_ENEMYPLAYERPROTO']._serialized_start=1797
  _globals['_ENEMYPLAYERPROTO']._serialized_end=2160
  _globals['_SERIALIZEDAGENTPROTO']._serialized_start=2162
  _globals['_SERIALIZEDAGENTPROTO']._serialized_end=2288
  _globals['_CHOICEPROTO']._serialized_start=2291
  _globals['_CHOICEPROTO']._serialized_end=2588
  _globals['_CARDOPTIONS']._serialized_start=2590
  _globals['_CARDOPTIONS']._serialized_end=2666
  _globals['_EFFECTOPTIONS']._serialized_start=2668
  _globals['_EFFECTOPTIONS']._serialized_end=2709
# @@protoc_insertion_point(module_scope)
