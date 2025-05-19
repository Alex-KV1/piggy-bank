from json import dumps, loads
from datetime import datetime

class Goal:
    balanc = 0.0 # Текущий баланс
    total_amount = 0 # сумма сумм всех целей
    task_complate = 0 # счетик завершонных задач
    def __init__(self) -> None:
        self.goal = dict()
    
    def add_gaol(self, name:str, amount:float, status="in progres", category='No category', data='no data'):
        self.goal[name] = { 'amount' : amount, #сумма цели
                            'status':status, # статус завершина или активна
                            'category':category, # категория
                            'data':data # дата заврешния задачи
                          }
        self.save_data()
        self.cacl_total_amount()
        
    def load_data(self):
        try:
            with open("data.json", "r", encoding='utf-8') as file:
                self.balanc, self.goal = loads(file.read())
            self.cacl_total_amount()
            self.check_balance()
            
        except Exception as e:
            print(e)
    
    def save_data(self):
        pac = (self.balanc, self.goal)
        try:
            with open("data.json", "w", encoding='utf-8') as file:
                file.write(dumps(pac))
                
        except Exception as e:
            print(e)
    
    def print(self):
        for i in self.goal.keys():
            for key, item in self.goal[i].items():
                print(key, ":", item)
            print(f"Процент выполнение по цели {self.get_progress(self.goal[i]['amount'])} %")
            print("текущий баланс:", self.balanc, "\n", "Общая сумма всех задач", self.total_amount,"\n")
            
    
    def _task_comp_(self): # подсчет завершенных задач
        count = 0
        for key in self.goal.keys():
            if self.goal[key]['status'] == 'complate':
                count+=1
        return count
    
    def cacl_total_amount(self): # подсчет общей суммы
        answ = 0
        if self.__get_total_task__() > 0:
            for key in self.goal.keys():
                answ += self.goal[key]['amount']
        self.total_amount = answ
        return answ
    
    def __get_total_task__(self): # счетик задач
        if not hasattr(Goal, 'total_taks'):
            Goal.total_task = len(self.goal)
        else: 
            self.total_task = len(self.goal)
        return self.total_task
    
    def get_total_progress(self):
        p_a = 0
        p_tsk = 0
        # print(f'{self.total_amount} {self.balanc} {self.task_complate}')
        if len(self.goal) !=0:
            p_a = round(self.balanc/self.total_amount*100, 2)
        if self.task_complate !=0:
            p_tsk = round(self.task_complate/len(self.goal)*100, 2)
        # print("прогрес по общей сумме", p_a)
        # print("прогрес по целям", p_tsk)
        return (p_a, p_tsk)
    
    def get_progress(self, amount): # подсчет % выполнения цели на основе текущего баланаса
        return round(self.balanc/amount*100, 2)
    
    def check_balance(self): # проверка баланса и завершенных задач
        for key in self.goal.keys():
            if self.balanc >= self.goal[key]['amount']:
                self.goal[key]['status'] = 'complate'
            elif self.balanc < self.goal[key]['amount']\
                and self.goal[key]['status'] == 'complate':
                self.goal[key]['status'] = 'in progres'
        self.task_complate = self._task_comp_()
            
    def set_balance(self, num:float): 
        self.balanc = num
        self.check_balance()
        self.save_data()

    def get_inform_by_ittem(self, item):
        if item in self.goal:
            self.check_balance()
            total_amount = self.cacl_total_amount()
            progres_goal = self.get_progress(self.goal[item]['amount'])
            total_progres, progres_by_goal = self.get_total_progress()
            answer = ['',
                f"Текущий баланс: {self.balanc}",
                f"Сумма цели {item}: {self.goal[item]['amount']}",
                f"Категория: {self.goal[item]['category']}",
                f"Текущий статус: {self.goal[item]['status']}",
                f"Дата заврешения цели: {self.goal[item]['data']}",
                f"Цель выполнена на: {progres_goal}%",
                f"-------------------------------------------",
                '',
                f"Общая сумма по всем целям: {total_amount}",
                f"Прогрес по общей сумме: {total_progres}",
                f"Прогрес по целям: {progres_by_goal}"            
            ]
            return answer
        else:
            return ['Цель не выбрана']
        


class Check():
    def __init__(self, name_goal, goal, cat, data) -> None:
        self.name_goal = name_goal
        self.goal = goal
        self.cat = cat
        self.data = data

    def validate (self):
        try:
            self.goal = float(self.goal)
            dateformat = "%d.%m.%Y"
            datetime.strptime(self.data, dateformat)
        except Exception:
            return None
       
        return [self.name_goal, self.goal, self.cat, self.data]
    

def cheak_money(num):
    try:
        num = float(num)
    except Exception:
        return None
    
    return num