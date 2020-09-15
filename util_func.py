# 基本的处理逻辑函数
import const_values

# 判断float为0
def is_float_zero(test_float):
    if abs(test_float) <= const_values.zero_float():
        return True
    else:
        return False

# 判断float是否报错值
def is_float_error(test_float):
    if is_float_zero(test_float - const_values.get_error_float()):
        return True
    else:
        return False

def isExitCode(code):
    return code == const_values.special_code("EXIT")

def isAnnualCode(code):
    return code == const_values.special_code("ANNUAL")

def isLs(code):
    return code == const_values.special_code("LS")