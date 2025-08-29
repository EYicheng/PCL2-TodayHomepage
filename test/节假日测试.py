import datetime

from chinese_calendar import is_holiday, is_workday
april_last = datetime.date(2018, 4, 30)
assert is_workday(april_last) is False
assert is_holiday(april_last) is True

import chinese_calendar as calendar
on_holiday, holiday_name = calendar.get_holiday_detail(april_last)
assert on_holiday is True
assert holiday_name == calendar.Holiday.labour_day.value

import chinese_calendar
assert chinese_calendar.is_in_lieu(datetime.date(2006, 2, 1)) is False
assert chinese_calendar.is_in_lieu(datetime.date(2006, 2, 2)) is True

print(f'今天{"是" if is_workday(datetime.date.today()) else "不是"}工作日，是{calendar.get_holiday_detail(datetime.date.today())}')

work_date = datetime.date(2025,8, 1)
lieu_date = datetime.date(2025, 10, 11)
holiday = datetime.date(2025, 10, 1)
weekend = datetime.date(2025, 8, 30)
datelist = [work_date, lieu_date, holiday, weekend]

for i in range(4):
    is_workday_ = is_workday(datelist[i])
    is_holiday_ = is_holiday(datelist[i])
    is_holiday__ = calendar.get_holiday_detail(datelist[i])
    is_in_lieu_ = calendar.is_in_lieu(datelist[i])
    print(f'{datelist[i]}是工作日：{is_workday_}，是假期：{is_holiday_}，{is_holiday__}，是调休：{is_in_lieu_}')
    print(is_holiday__[0], is_holiday__[1])
    if is_holiday__[1]:
        print(1)