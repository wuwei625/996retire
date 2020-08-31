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
    return 2000