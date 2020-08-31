import os
import get_mean_and_var_from_history_nav

# 根据文件名，读取历史净值记录
def do_get(fund_history_filename):
    fund_nav = []
    line_amount = 0
    illegal_amount = 0

    try:
        with open(fund_history_filename, encoding='utf-8') as f_history:
            line = f_history.readline()
            while line:
                line_amount += 1
                line = line.strip()
                # 尝试将读取到的净值转为float
                try:
                    nav_single = float(line)
                except:
                    nav_single = 0.0
                # 判断数据合法性
                if nav_single > 0.00001:
                    fund_nav.append(nav_single)
                else:
                    print("警告：排除疑似非法的数据在第" + str(line_amount) + "行：" + line)
                    illegal_amount += 1
                # 处理下一行
                line = f_history.readline()
        f_history.close()
    except:
        print("错误信息：净值文档" + fund_history_filename + "分析发生错误！")
    # 输出错误信息
    if (illegal_amount > 0):
        print("错误信息：净值文件中有" + str(illegal_amount) + "条记录格式或者值非法。")
    return fund_nav
