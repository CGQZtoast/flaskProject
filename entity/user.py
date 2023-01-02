# -*- coding = utf-8 -*-
# @Time : 2022/11/20 14:13
# @Author : 乌贼
# @File : user.py
# @Software : PyCharm

from sqlalchemy import func, null

from database.models import *
from methods.get_date import *


class User(object):
    # private_data
    __id = 0,  # id
    __phone = '',  # 手机号
    __DOB = '',  # 出生日期
    __sex = 0,  # 性别
    __province = ''  # 省份
    __city = ''  # 市
    __district = ''  # 区

    def __init__(self, id, phone, DOB, sex, provider, city, district):
        """
        初始化用户对象
        :param id:          用户id
        :param phone:       电话
        :param DOB:         生日
        :param sex:         性别
        :param provider:    所在省份
        """
        self.__id = id
        self.__phone = phone
        self.__DOB = DOB
        self.__sex = sex
        if provider is not None:
            self.__province = provider
        else:
            self.__province = '-'
        if city is not None:
            self.__city = city
        else:
            self.__city = '-'
        if district is not None:
            self.__district = district
        else:
            self.__district = '-'

    def get_dict(self):
        temp_user = {'id': self.__id, 'phone': self.__phone, 'sex': str(self.__sex), 'birth': str(self.__DOB), 'region': [self.__province, self.__city, self.__district], 'showRegion': self.__province + ' ' + self.__city + ' ' + self.__district}
        # temp_user = {'id': self.__id, 'phone': self.__phone, 'sex': str(self.__sex), 'birth': str(self.__DOB), 'region': [self.__province, self.__city, self.__district], 'showRegion': self.__province}

        return temp_user


class UserManege(object):
    __total_user_date_list = []
    __total_user = []
    __increased_user_date_list = []
    __increased_user = []

    __age_distribution = {}
    __gender_distribution = {}
    __provinces_distribution = {}

    __user_msg = []

    def get_total_user_date_list(self):
        return self.__total_user_date_list

    def get_total_user(self):
        return self.__total_user

    def get_increased_user_date_list(self):
        return self.__increased_user_date_list

    def get_increased_user(self):
        return self.__increased_user

    def get_age_distribution(self):
        return self.__age_distribution

    def get_gender_distribution(self):
        return self.__gender_distribution

    def get_provinces_distribution(self):
        return self.__provinces_distribution

    def get_user_msg(self):
        return self.__user_msg

    def __total_user_statistics(self, total_user_time_slot):
        """
        用户总数统计
        :param total_user_time_slot:    0：代表最近一周的用户总数(7统计个点，每个点时间代表1天）
                                        1：代表最近半年的用户总数(6统计个点，每个点时间代表1个月,返回该月月末时的数据）
                                        2：代表从系统启用到目前的用户总数（按月统计，每个月一个点，返回月末时的数据）
        :return:    total_user_data_list:   时间点
                    total_user:             时间点对应的用户总数
        """
        try:
            if total_user_time_slot == "0":  # 最近一周
                temp_date = get_date_by_week(0)
            elif total_user_time_slot == "1":  # 最近半年
                temp_date = get_date_by_half_year(0)
            else:  # 全部（按月统计）
                temp_date = get_date_by_month()

            # 获取日期对应的用户总数
            for date in temp_date:
                count = user.query.filter(user.register_time <= date).count()
                self.__total_user.append(count)
                # 日期处理
                if total_user_time_slot == '0':
                    date = date.replace('-', '/')
                else:
                    date = date[:-3]
                self.__total_user_date_list.append(date)
        except Exception as e:
            print('entity-UserManege-total_user_statistics error')
            print('error: ', e)

    def __new_user_statistics(self, increased_user_time_slot):
        """
        新增用户统计
        :param increased_user_time_slot:    0：代表最近一周的用户新增(7个统计点，每个点时间代表1天）
                                            1：代表最近半年的用户新增(6个统计点，每个点时间代表1个月）
                                            2：代表从系统启用到目前的用户新增（从系统启用到现在，按月统计，每个月一个点）
        :return:    increased_user_date_list    时间点
                    increased_user              时间点对应的新增人数
        """
        try:
            if increased_user_time_slot == "0":  # 最近一周
                temp_date = get_date_by_week(1)
            elif increased_user_time_slot == "1":  # 最近半年
                temp_date = get_date_by_half_year(1)
            else:  # 全部（按月统计）
                temp_date = get_date_by_month()

            for i in range(0, len(temp_date)):
                if i == 0:
                    date = temp_date[i]
                    if increased_user_time_slot == "0":
                        date = date.replace('-', '/')
                    else:
                        date = date[:-3]
                    self.__increased_user_date_list.append(date)
                    self.__increased_user.append(0)
                    continue
                count = user.query.filter(
                    user.register_time > temp_date[i - 1],
                    user.register_time <= temp_date[i]
                ).count()
                date = temp_date[i]
                if increased_user_time_slot == "0":
                    date = date.replace('-', '/')
                else:
                    date = date[:-3]
                self.__increased_user_date_list.append(date)
                self.__increased_user.append(count)
        except Exception as e:
            print('entity-UserManege-new_user_statistics error')
            print('error: ', e)

    def count_statistics(self, total_user_time_slot, increased_user_time_slot):
        """
        用户数量统计（用户总数、用户新增）（近一周，近半年，全阶段）
        :param total_user_time_slot:    0：代表最近一周的用户总数(7统计个点，每个点时间代表1天）
                                        1：代表最近半年的用户总数(6统计个点，每个点时间代表1个月,返回该月月末时的数据）
                                        2：代表从系统启用到目前的用户总数（按月统计，每个月一个点，返回月末时的数据）
        :param increased_user_time_slot:    0：代表最近一周的用户新增(7个统计点，每个点时间代表1天）
                                            1：代表最近半年的用户新增(6个统计点，每个点时间代表1个月）
                                            2：代表从系统启用到目前的用户新增（从系统启用到现在，按月统计，每个月一个点）
        :return:    True:   正常
                    False:  出错
        """
        self.__total_user = []
        self.__total_user_date_list = []
        self.__increased_user_date_list = []
        self.__increased_user = []
        try:
            self.__total_user_statistics(total_user_time_slot)
            self.__new_user_statistics(increased_user_time_slot)
            return True
        except Exception as e:
            print('entity-UserManege-count_statistics error')
            print('error: ', e)
            return False

    def __user_age_statistics(self):
        """
        用户年龄分布统计
        """
        sql1 = "select count(*) from user where TIMESTAMPDIFF(YEAR, DOB, CURDATE()) <= 10"
        sql2 = "select count(*) " \
               "from user " \
               "where TIMESTAMPDIFF(YEAR, DOB, CURDATE()) > 10 and " \
               "TIMESTAMPDIFF(YEAR, DOB, CURDATE()) <= 20"
        sql3 = "select count(*) " \
               "from user " \
               "where TIMESTAMPDIFF(YEAR, DOB, CURDATE()) > 20 and " \
               "TIMESTAMPDIFF(YEAR, DOB, CURDATE()) <= 40"
        sql4 = "select count(*) from user where TIMESTAMPDIFF(YEAR, DOB, CURDATE()) > 40"

        try:
            ret = db.session.execute(sql1)
            self.__age_distribution['0-10'] = ret.fetchone()[0]
            ret = db.session.execute(sql2)
            self.__age_distribution['10-20'] = ret.fetchone()[0]
            ret = db.session.execute(sql3)
            self.__age_distribution['20-40'] = ret.fetchone()[0]
            ret = db.session.execute(sql4)
            self.__age_distribution['40以上'] = ret.fetchone()[0]
        except Exception as e:
            print('entity-UserManege-user_age_statistics error')
            print('error: ', e)

    def __user_gender_statistics(self):
        """
        用户性别分布统计
        """
        try:
            male_count = user.query.filter(user.sex == 0).count()
            female_count = user.query.filter(user.sex == 1).count()
            self.__gender_distribution['male'] = male_count
            self.__gender_distribution['female'] = female_count
        except Exception as e:
            print('entity-UserManege-user_gender_statistics error', e)
            print('error: ', e)

    def __provinces_statistics(self):
        """
        用户省份分布统计
        :return:
        """
        try:
            provinces = db.session.query(
                user.province,
                func.count()
            ).filter(user.province != null).group_by(user.province).order_by(func.count().desc()).all()
            number = 1
            count = 0
            for i in provinces:
                if number <= 7:
                    self.__provinces_distribution[i[0]] = i[1]
                else:
                    # 其他
                    # 统计总数
                    count = count + i[1]
                number = number + 1
            self.__provinces_distribution['其他省份'] = count
            count = user.query.filter(user.province == None).count()
            self.__provinces_distribution['未选择'] = count
        except Exception as e:
            print('entity-UserManege-provinces_statistics error')
            print('error: ', e)

    def distribution_statistics(self):
        """
        用户分布统计（年龄分布、性别分布、省份分布）
        :return:    True:   正常
                    False:  出错
        """
        self.__age_distribution = {}
        self.__gender_distribution = {}
        self.__provinces_distribution = {}
        try:
            self.__user_age_statistics()
            self.__user_gender_statistics()
            self.__provinces_statistics()
            return True
        except Exception as e:
            print('entity-UserManege-distribution_statistics error')
            print('error: ', e)
            return False

    def get_all_user_information(self):
        """
        获取所有用户信息
        :return:    True:   正常
                    False:  出错
        """
        self.__user_msg = []

        try:
            # 遍历用户表
            user_info = db.session.query(
                user.id,
                user.phone,
                user.DOB,
                user.sex,
                user.province,
                user.city,
                user.district
            ).filter().all()

            for info in user_info:
                temp_user = User(info[0], info[1], info[2], info[3], info[4], info[5], info[6])
                self.__user_msg.append(temp_user.get_dict())
            return True
        except Exception as e:
            print('entity-UserManege-get_all_user_information error')
            print('error: ', e)
            return False

    def delete_user(self, ids):
        """
        删除用户
        :param ids: 待删除的用户id数组
        :return:    True:   正常
                    False:  出错
        """
        try:
            for user_id in ids:
                user.query.filter(user.id == user_id).delete()
            db.session.commit()
            return True
        except Exception as e:
            print('entity-UserManege-delete_user error')
            print('error: ', e)
            return False

    def edit_user_info(self, id, phone, sex, DOB, region):
        """
        修改用户信息
        :param id:      用户id
        :param phone:   手机
        :param sex:     性别
        :param DOB:     生日
        :param region:  地区的数组
        :return:
        """
        try:
            # 查找对象
            temp_user = user.query.filter(user.id == id).first()
            if temp_user is not None:
                temp_user.phone = phone
                temp_user.sex = sex
                temp_user.DOB = DOB
                temp_user.province = region[0]
                temp_user.city = region[1]
                temp_user.district = region[2]
                db.session.commit()
                return True
        except Exception as e:
            print('entity-UserManege-edit_user_info error')
            print('error: ', e)
            return False
