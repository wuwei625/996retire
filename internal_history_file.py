# 涉及文件处理的函数
import os
import util_func

# 遍历有记录的基金名称
def fund_list(fund_history_dir):
    fund_file_list = []
    for (dirpath, dirnames, filenames) in os.walk(fund_history_dir):
        for f in filenames:
            if f.endswith(".txt"):
                f = f.replace(".txt", "")
                if not util_func.isAnnualCode(f):
                    fund_file_list.append(f)
    return fund_file_list

# 根据文件名，读取历史净值记录
def get_nav_from_file(fund_history_filename):
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