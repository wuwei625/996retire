# 关于投资规划的逻辑
import const_values

def current_asset_reallocation(income_year, expense_year, current_liquidity, current_non_liquidity):
    # 按短期内半年开销的最大值，评估流动性基础需求 TODO:此处可以个性化
    # 计算短期资金缺口，算作流动性资产额外需求
    short_term = const_values.short_term()
    short_term_deficit = 0
    basic_liquidity_need = 0
    for i in range(short_term):
        short_term_deficit += (expense_year[i] - income_year[i])
        basic_liquidity_need = max(basic_liquidity_need, expense_year[i] // 2 + 1)
    short_term_deficit = max(0, short_term_deficit)

    # 理想的流动性水平时半年开销加短期资金净缺口
    ideal_liquidity = basic_liquidity_need + short_term_deficit
    # 根据实际资产情况，对流动性/非流动投资资产进行重分配
    if ideal_liquidity <= current_liquidity + current_non_liquidity:
        suggested_liquidity = ideal_liquidity
    else:
        suggested_liquidity = current_liquidity + current_non_liquidity
    suggested_non_liquidity = current_liquidity + current_non_liquidity - suggested_liquidity

    return ideal_liquidity, suggested_liquidity, suggested_non_liquidity