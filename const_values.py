def days(days_type):
    if days_type == "YEAR":
        return 244
    elif days_type == "MONTH":
        return 20
    elif days_type == "WEEK":
        return 5
    else:
        return 1

def zero_float(zero_type=""):
    if (zero_type == "NEG"):
        return -0.00000000000000001
    else:
        return 0.00000000000000001

def max_fee_rate():
    return 10.0

def test_times():
    return 7000

def year_after_retire_with_optional():
    return 20

def year_after_retire_with_optional_reduce():
    return 40

def irr_guess():
    return 0.05

def error_tolerance():
    return 0.1

def irr_retry_limit():
    return 100000

def get_error_float():
    return -4444.44

def is_float_error(test_float):
    if abs(test_float - get_error_float()) <= zero_float():
        return True
    else:
        return False