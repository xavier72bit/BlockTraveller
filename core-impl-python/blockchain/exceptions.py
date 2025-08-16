# -*- coding: UTF-8 -*-
# @Project: core-impl-python
# @File   : exceptions.py
# @Author : Xavier Wu
# @Date   : 2025/8/16 14:03

# Hash Check Error
class DeserializeHashValueCheckError(Exception):
    """
    反序列化时的hash检查未通过
    """
    pass
