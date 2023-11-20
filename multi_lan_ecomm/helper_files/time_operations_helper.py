import datetime



class TimeOperationsHelper():
    
    def convert_str_time_format(strTime):
        FMT = '%H:%M:%S'
        return datetime.datetime.strptime(
                        str(strTime), FMT
                    ).time()