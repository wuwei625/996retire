import get_fund_nav_from_file
import get_mean_and_var_from_history_nav
import const_values

# 调试入口：单个基金的历史分析输出
if __name__ == "__main__":
    tips = "请确保要分析的基金净值数据已经导入到./history/文件夹后，输入基金代码，输入0退出："
    fund_code = input(tips)
    while fund_code != "0":
        fund_history_filename = "./history/" + fund_code + ".txt"
        fund_nav = get_fund_nav_from_file.do_get(fund_history_filename)
        # 至少需要10个值才有意义执行下一步
        nav_amount = len(fund_nav)
        if nav_amount > 10:
            print("共导入" + str(nav_amount) + "个历史净值参与分析")
            fund_nav_increase_logarithm_mean, fund_nav_increase_logarithm_var = get_mean_and_var_from_history_nav.analysis_fund(fund_nav, 0)
            if (abs(fund_nav_increase_logarithm_mean) > const_values.zero_float() or abs(fund_nav_increase_logarithm_var) > const_values.zero_float()):
                print("基金日增长率对数的均值是%.3e，方差是%.3e"%(fund_nav_increase_logarithm_mean,fund_nav_increase_logarithm_var))
                expected_year_rate, expect_year_std_var = get_mean_and_var_from_history_nav.mean_var_trans(fund_nav_increase_logarithm_mean, fund_nav_increase_logarithm_var, const_values.days("YEAR"))
                print("这个基金的历史年化收益率是%.2f%%，历史年化波动率是%.2f%%"%((expected_year_rate - 1.0)*100,expect_year_std_var*100))
            else:
                print("错误信息：未获得正确结果！")
        else:
            print ("错误信息：没有获取到净值历史，或者数据太少，无法完成操作。")

        fund_code = input(tips)