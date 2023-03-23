from do.my_dict import Dict


def object_2_map(obj: object):
    """对象转Dict"""
    m = obj.__dict__
    for k in m.keys():
        v = m[k]
        if hasattr(v, "__dict__"):
            m[k] = object_2_map(v)
    return m


def dict_2_obj(dict_obj):
    if not isinstance(dict_obj, dict):
        return dict_obj
    d = Dict()
    for k, v in dict_obj.items():
        d[k] = dict_2_obj(v)
    return d
