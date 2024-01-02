from datetime import datetime
from dateutil import relativedelta

class write_to_DATA():
    def __init__(self, wrt_t_D):
        self.wrt_t_D = self
        
        def wrt_t_D():
            DATA = []
            DATA.append("Plattform")
            DATA.append("Input")
            
            one_month_from_now = datetime.now() + relativedelta(months=1)
            DATA.append(one_month_from_now.strftime("%H:%M:%S %d/%m/%Y"))


