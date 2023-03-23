from do.obj_info import ObjInfo


class Dict(ObjInfo, dict):
    __setattr__ = dict.__setitem__
    __getattr__ = dict.__getitem__