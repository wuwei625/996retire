def get_simulated_asset_values(invest_cycle, invest_times, single_amount, fee_rate, future_nav):
    # 根据目标基金的定投周期、定投金额、费率、模拟未来净值组，测算账户价值变化情况
    result = []
        
    # 用这sample_amount组净值序列模拟未来投资的每日账户值
    for nav_sequence in future_nav:
        i = 0
        share_amount = 0.0
        daily_account_value = 0.0
        account_value = []
        days_amount = len(nav_sequence)
        while i < days_amount:
            if (i % invest_cycle == 0) and ((i // invest_cycle) < invest_times):
                # 如果时间点位于定投周期点，则执行一次申购操作
                share_amount += single_amount * (1.0 - fee_rate) / nav_sequence[i] 
            # 计算当天账户总价值
            daily_account_value = nav_sequence[i] * share_amount
            # 将账户总价值记录到账户价值变化数组中
            account_value.append(daily_account_value)
            i += 1
        # 将某一组模拟值记录到总结果中
        result.append(account_value)
    return result