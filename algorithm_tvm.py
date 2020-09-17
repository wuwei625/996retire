# 时间价值计算的模块
import math
import const_values

# 净现值计算，返回现金流贴现到期初值
def get_npv(net_cf, discount_rate):
    length = len(net_cf)
    npv = 0.0
    if length == 0:
        return 0.0
    else:
        for i in range(length):
            npv += net_cf[i] / ((1.0 + discount_rate) ** i)
    return npv

# 净未来值计算，计算现金流期末价值
def get_nfv(net_cf, discount_rate):
    length = len(net_cf)
    nfv = 0.0
    if length == 0:
        return 0.0
    else:
        for i in range(length):
            nfv += net_cf[i] * ((1.0 + discount_rate) ** (length - i - 1))
    return nfv

def get_irr(net_cf, fv, guess = const_values.irr_guess()):
    irr_step = guess / 2.0
    error_tolerance = abs(const_values.error_tolerance())
    residual = error_tolerance * 10.0 + 1.0
    irr_retry_limit = const_values.irr_retry_limit()
    current_guess = guess
    last_try = ""

    while abs(residual) > error_tolerance and irr_retry_limit > 0:
        irr_retry_limit -= 1
        residual = get_nfv(net_cf, current_guess) - fv
        if residual > error_tolerance:
            # 利率太高，需要降低
            irr_step = 0 - abs(irr_step)
            # 和上一次调整方向相反时，改变修正步长，否则维持不变
            if last_try == "POS" or last_try == "":
                step_discount = False
            else:
                step_discount = True
            last_try = "POS"
        elif residual < 0.0 - error_tolerance:
            # 利率太低，需要调高
            irr_step = abs(irr_step)
            if last_try == "NEG" or last_try == "":
                step_discount = False
            else:
                step_discount = True
            last_try = "NEG"
        if step_discount:
            irr_step /= 2.0
        current_guess += irr_step
    if abs(residual) > error_tolerance:
        # 如果经过所有尝试都无法得到结果，返回一个错误标记
        return const_values.get_non_sense_float()
    else:
        # 返回基本符合计算结果的值
        return current_guess