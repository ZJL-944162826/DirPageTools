import datetime
import json
from array import array

from do.obj_info import ObjInfo
from utils.class_util import object_2_map


class ObjInfoEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, datetime.datetime):
                print("MyEncoder-datetime.datetime")
                return obj.strftime("%Y-%m-%d %H:%M:%S")
            if isinstance(obj, bytes):
                return str(obj, encoding='utf-8')
            if isinstance(obj, int):
                return int(obj)
            elif isinstance(obj, float):
                return float(obj)
            elif isinstance(obj, array):
                return obj.tolist()
            elif isinstance(obj, ObjInfo):
                return object_2_map(obj)
            else:
                return super(ObjInfoEncoder, self).default(obj)
        except Exception as e:
            print(e)

