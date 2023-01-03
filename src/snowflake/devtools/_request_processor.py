# Prototyping pipeline processor

# class RecordingProcessor(object):
#     def process_request(self, request):
#         return request
#
#     def process_response(self, response):
#         return response
#
#     @classmethod
#     def replace_header(cls, entity, header, old, new):
#         for key, values in entity["headers"].items():
#             if key.lower() == header.lower():
#                 if isinstance(values, list):
#                     entity["headers"][key] = \
#                       [v.replace(old, new) for v in values]
#                 else:
#                     entity["headers"][key] = values.replace(old, new)
#
#
# class BasicRecordingProcessor(RecordingProcessor):
#     pass
