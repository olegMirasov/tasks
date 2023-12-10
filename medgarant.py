
busy = [
    {'start': '10:30', 'stop': '10:50'},
    {'start': '18:40', 'stop': '18:50'},
    {'start': '14:40', 'stop': '15:50'},
    {'start': '16:40', 'stop': '17:20'},
    {'start': '20:05', 'stop': '20:20'}]


class TimeGap:
    def __init__(self, int_time: dict = None, str_time: dict = None):
        if not int_time and not str_time:
            raise AttributeError('No data')

        if int_time:
            self.int_start = int_time['start']
            self.int_stop = int_time['stop']
            self.str_start = self.__time_to_str(self.int_start)
            self.str_stop = self.__time_to_str(self.int_stop)
        elif str_time:
            self.str_start = str_time['start']
            self.str_stop = str_time['stop']
            self.int_start = self.__time_to_int(self.str_start)
            self.int_stop = self.__time_to_int(self.str_stop)

        self.gap = self.int_stop - self.int_start

    def get_drop(self, minute: int):
        count = self.gap // minute
        temp = []
        for i in range(count):
            d = {'start': self.int_start + i * minute,
                 'stop': self.int_start + (i + 1) * minute}
            d['start'] = self.__time_to_str(d['start'])
            d['stop'] = self.__time_to_str(d['stop'])
            temp.append(d)
        return temp

    @staticmethod
    def __time_to_str(time: int):
        hour = str(time // 60).rjust(2, '0')
        minute = str(time % 60).rjust(2, '0')
        return f'{hour}:{minute}'

    @staticmethod
    def __time_to_int(time: str):
        temp = [int(i) for i in time.split(':')]
        return temp[0] * 60 + temp[1]

    def __str__(self):
        start_s = f'start: {self.str_start}, int: {self.int_start}'
        stop_s = f'stop: {self.str_stop}, int: {self.int_stop}'
        return f'{start_s}\n{stop_s}\ngap: {self.gap}\n{"="*10}'


class TimeInfo:
    def __init__(self, start_work: str, stop_work: str):
        self.__start_work = {'start': start_work, 'stop': start_work}
        self.__stop_work = {'start': stop_work, 'stop': stop_work}
        self.__timeline = [self.__start_work, self.__stop_work]
        self.__work_time = []
        self.__rest_time = []

    @staticmethod
    def __set_time(data):
        temp = []
        try:
            for i in data:
                if type(i['start']) == str:
                    temp.append(TimeGap(str_time=i))
                else:
                    temp.append(TimeGap(int_time=i))
        except Exception as e:
            print('Wrong data!!!')
            print(e)
            return []

        return temp

    def new_time(self, work_data):
        # создаем рабочее время
        __work_time = self.__set_time(work_data + self.__timeline)
        __work_time = sorted(__work_time, key=lambda x: x.int_stop)

        # создаем время отдыха/приема пациентов
        temp = []
        for i in range(len(__work_time) - 1):
            rt = {'start': __work_time[i].int_stop,
                  'stop': __work_time[i + 1].int_start}
            temp.append(rt)

        __rest_time = self.__set_time(temp)

        # защищаем данные от пустого списка
        if __work_time:
            self.__reset()
            self.__work_time = __work_time
            self.__rest_time = __rest_time

    def get_free_list(self, minute: int = 30):
        temp = []
        for i in self.__rest_time:
            if i.gap < minute:
                continue
            temp.extend(i.get_drop(minute))
        return temp

    def __reset(self):
        self.__work_time = []
        self.__rest_time = []


if __name__ == '__main__':
    time_info = TimeInfo(start_work='09:00', stop_work='21:00')
    time_info.new_time(busy)
    result = time_info.get_free_list(30)

    for j in result:
        print(j)
