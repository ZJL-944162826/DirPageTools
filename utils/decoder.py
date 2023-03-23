import json


class Tokener():
    """
      ## TODO: 字符串中的各种 Token 解析
    """

    def __init__(self, json_str):
        self.__str = json_str  # json 字符串
        self.__i = 0  # 当前读到的字符位置
        self.__cur_token = None  # 当前的字符

    def __cur_char(self):
        """
          ## 读取当前的字符的位置
        """
        if self.__i < len(self.__str):
            return self.__str[self.__i]
        return ''

    def __move_i(self, step=1):
        """
          ## 读取下一个字符
        """
        if self.__i < len(self.__str): self.__i += step

    def __next_string(self):
        """
          ## str 字符片段读取
        """
        outstr = ''
        trans_flag = False
        self.__move_i()
        while self.__cur_char() != '':
            ch = self.__cur_char()
            if ch == "\\":
                trans_flag = True  # 处理转义
            else:
                if not trans_flag:
                    if ch == '"':
                        break
                else:
                    trans_flag = False
            outstr += ch
            self.__move_i()
        return outstr

    def __next_number(self):
        """
          ## number 字符片段读取
        """
        expr = ''
        while self.__cur_char().isdigit() or self.__cur_char() in ('.', '+', '-'):
            expr += self.__cur_char()
            self.__move_i()
        self.__move_i(-1)
        if "." in expr:
            return float(expr)
        else:
            return int(expr)

    def __next_const(self):
        """
          ## bool 字符片段读取
        """
        outstr = ''
        while self.__cur_char().isalpha() and len(outstr) < 5:
            outstr += self.__cur_char()
            self.__move_i()
        self.__move_i(-1)

        if outstr in ("true", "false", "null"):
            return {
                "true": True,
                "false": False,
                "null": None,
            }[outstr]
        raise Exception(f"Invalid symbol {outstr}")

    def next(self):
        """
          ## 解析这段 json 字符串
          ## TODO: 获得下一个字符片段
        """
        is_white_space = lambda a_char: a_char in ("\x20", "\n", "\r", "\t")
        while is_white_space(self.__cur_char()):
            self.__move_i()

        ch = self.__cur_char()
        if ch == '':
            cur_token = None
        elif ch in ('{', '}', '[', ']', ',', ':'):
            # 这些特殊的包裹性、分隔性字符作为单独的token
            cur_token = ch
        elif ch == '"':
            # 以 “ 开头代表是一个字符串
            cur_token = self.__next_string()
        elif ch.isalpha():
            # 直接以字母开头的话检查是不是 bool 类型的
            cur_token = self.__next_const()
        elif ch.isdigit() or ch in ('-', '+'):
            # 以数字开头或者是+-符号开头
            cur_token = self.__next_number()

        self.__move_i()
        self.__cur_token = cur_token

        return cur_token is not None

    def cur_token(self):
        return self.__cur_token


class JsonDecoder:
    """
      TODO: json 字符串解析
    """

    def __init__(self):
        pass

    def json_object(self, tokener):
        """
          ## json 解析json中的对象结构
        """
        obj = {}
        # 判断是否为 object 起始字符
        if tokener.cur_token() != "{":
            raise Exception('Json must start with "{"')

        while True:  # 循环中每次都去解析一组键值对
            tokener.next()
            tk_temp = tokener.cur_token()
            # 如果直接遇到闭回的 } 则直接返回空结构体
            if tk_temp == "}":
                return {}

            if not isinstance(tk_temp, str):
                raise Exception(f'invalid key {tk_temp}')

            # 解析得到 键值对中  key
            key = tk_temp
            tokener.next()
            if tokener.cur_token() != ":":
                raise Exception(f'expect ":" after {key} ')

            # 解析得到 键值对中 value
            tokener.next()
            val = tokener.cur_token()
            if val == "[":
                val = self.json_array(tokener)
            elif val == "{":
                val = self.json_object(tokener)
            obj[key] = val

            # 解析与下一组键值对的
            tokener.next()
            tk_split = tokener.cur_token()
            if tk_split == ",":  # 若遇到多个元素则重新进入循环
                continue
            elif tk_split == "}":  # 如果为 } 则说明对象闭合
                break
            else:
                if tk_split is None:
                    print(f"tk_split {tk_split}")
                    raise Exception('missing "}" at the end of object')
                raise Exception(f'unexpected token "{tk_split}" at key "{tk_split}" ')
        return obj

    def json_array(self, tokener):
        if tokener.cur_token() != "[":
            raise Exception('Json array must start with "["')
        arr = []
        while True:
            # 每次遍历都能得到数组中的一个元素
            tokener.next()
            tk_temp = tokener.cur_token()
            if "tk_temp" == "]":
                return arr
            if tk_temp == "{":
                val = self.json_object(tokener)
            elif tk_temp == "[":
                val = self.json_array(tokener)
            elif tk_temp in (',', ":", "}"):
                raise Exception(f"unexpected token {tk_temp}")
            else:
                val = tk_temp
            arr.append(val)

            # 解析获得与数值的逻辑连接符
            tokener.next()
            tk_end = tokener.cur_token()
            if tk_end == ",":
                continue
            if tk_end == "]":
                break
            else:
                if tk_end is None:
                    raise Exception('missing "]" at the end of array')
        return arr

    def decode(self, json_str: str):
        tokener = Tokener(json_str)
        if not tokener.next():
            return None
        first_token = tokener.cur_token()

        if first_token == "{":
            decode_val = self.json_object(tokener)
        elif first_token == "[":
            decode_val = self.json_array(tokener)
        else:
            raise Exception('Json must start with "{"')

        if tokener.next():
            raise Exception(f"unexpected token {tokener.cur_token()}")
        return decode_val

