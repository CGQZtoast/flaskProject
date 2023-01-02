# -*- coding = utf-8 -*-
# @Time : 2022/11/16 23:47
# @Author : 乌贼
# @File : get_date.py
# @Software : PyCharm


import datetime

# 项目开始日期
project_start_date = datetime.date(2022, 1, 1)


# 获取获得一个月中的最后一天
def last_day_of_month(any_day):
    """
    获取获得一个月中的最后一天
    :param any_day: 任意日期
    :return: string
    """
    next_month = any_day.replace(day=28) + datetime.timedelta(days=4)  # this will never fail
    return next_month - datetime.timedelta(days=next_month.day)


# 获取近一周日期
def get_date_by_week(param):
    """
    获取近一周日期
    :param: param   0:获取总数
                    1：获取新增数
    :return: last_week_date
    """
    if param == 0:
        days = 7
    else:
        days = 8

    last_week_date = []
    today = datetime.date.today()
    for i in range(days):
        # 获取七天前的日期
        date = today - datetime.timedelta(days=days - 1 - i)
        last_week_date.append(str(date))
    return last_week_date


# 获取近半年前日期（按月，获取每月的最后一天）
def get_date_by_half_year(param):
    """
    获取近半年前日期（按月，获取每月的最后一天）
    param: param
    :return:
    """
    if param == 0:
        months = 6
    else:
        months = 7

    last_half_year_date = []
    today = datetime.date.today()
    year = today.year
    month = today.month
    day = today.day
    for i in range(months):
        last_day = last_day_of_month(datetime.date(year, month, day))
        last_half_year_date.append(str(last_day))
        month = month - 1
        if month == 0:
            year = year - 1
            month = 12
    # 数组反转
    last_half_year_date = last_half_year_date[::-1]
    return last_half_year_date


# 获取从 项目开始 到 最新一天 的每个月的最后一天
def get_date_by_month():
    """
    获取从 项目开始 到 最新一天 的每个月的最后一天
    :return:
    """
    all_month = []
    today = datetime.date.today()
    year = today.year
    month = today.month
    day = today.day
    while True:
        last_day = last_day_of_month(datetime.date(year, month, day))
        if last_day <= project_start_date:
            break
        all_month.append(str(last_day))
        month = month - 1
        if month == 0:
            year = year - 1
            month = 12
    # 数组反转
    all_month = all_month[::-1]
    return all_month
