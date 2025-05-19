import npyscreen 
from cl import Goal , Check, cheak_money
from curses import ascii


class HelpMsgEnter(npyscreen.TitlePager):
    name = 'Подсказка:'
    def create(self):
        self.values = ['Если ввести не валидные данные, данные сохранены не будут! Что запись не дабавлена сразу будет видно в', 
                       'списке задач. После того как заполнение полей будет окончено нажимет ок',\
                       'Поддерживается ввод только латинцей, дата должна быть введена в формате (д.м.ГГ)']

class HelpText(npyscreen.TitlePager):
    name = 'Подсказка:'
    def create(self):
        self.values = ['Навигация по меню стрелками верх вниз, чтобы выбрать категорию нажимите space,', '                для перехода между элементами нажмите tab',\
                        'Доля добавления новой записи нажмите <c> - create. Раскладка клавиатуры = лат',
                        'Для изменения колличества средств в копилке нажмите <z>']
        self.add_handlers({
            'q': self.exit_program,  # Привязка клавиши 'q' для выхода
            'c': self.create_write,
        })
    def create_write(self, key):
        self.parent.create_write(key)
    
    def exit_program(self, key):
        print("Инициализрован выход из программы из MyMenu")
        self.parent.exit_program(113)

class EnterTexr(npyscreen.TitleText):
    def create(self):
        self.name = 'Имя цели'

class EnterForm(npyscreen.Form):
    DEFAULT_LINES = 40
    DEFAULT_COLUMNS = 130
    
    def create(self):
        self.add(HelpMsgEnter,max_height=3, relx= 5, rely= 2).create()
        self.n = self.add(npyscreen.TitleText,   name = 'Введи имя цели:', max_height=2, relx= 8, rely= 6,  max_width=50, use_two_lines=False)
        self.c = self.add(npyscreen.TitleText,   name = 'Цель:',           max_height=1, relx= 8, rely= 8,  max_width=50, use_two_lines=False)
        self.cat = self.add(npyscreen.TitleText, name = 'Категория:',      max_height=1, relx= 8, rely= 10,  max_width=50, use_two_lines=False)
        self.d = self.add(npyscreen.TitleText,   name = 'До какой даты:',  max_height=2, relx= 8, rely= 12, max_width=50, use_two_lines=False)
        self.base = self.parentApp.backend
        self.base.load_data()
        
        
    def afterEditing(self):
        print(f"self.n = {self.n}, self.n.values{self.n.value}")
        answer = Check(self.n.value, self.c.value, self.cat.value, self.d.value).validate()
        if answer:
            self.base.add_gaol(name = answer[0], amount = float(answer[1]), category = answer[2], data = answer[3])
        self.parentApp.switchFormPrevious() 


class EntertMoneyHelp(HelpMsgEnter):
    def create(self):
        self.values = ['Если ввести не валидные данные, данные сохранены не будут!',
                       'Необходимо ввести число которе заменит число имеющихся среств']

class EntertMoney(EnterForm):
    def create(self):
        self.add(EntertMoneyHelp,max_height=3, relx= 5, rely= 2).create()
        self.money = self.add(npyscreen.TitleText, name = 'Введи кол. ср:', max_height=2, relx= 2, rely= 6,  max_width=100, use_two_lines=False)
        self.base = self.parentApp.backend
        self.base.load_data()
    
    def afterEditing(self):
        # print(f"self.n = {self.n}, self.n.values{self.n.value}")
        money = cheak_money(self.money.value)
        if money:
            self.base.set_balance(money)
        self.parentApp.switchFormPrevious() 
        
    

class MyTextField(npyscreen.BoxTitle):
    name = 'Подробнее о цели'
    def create(self):
        self.values = ['','','','','','','','','','','           Выберите цель для отображение подробностей']
        
        self.add_handlers({
            'q': self.exit_program,  # Привязка клавиши 'q' для выхода
            'c': self.create_write,
        })
    def create_write(self, key):
        self.parent.create_write(key)
    
    def exit_program(self, key):
        print("Инициализрован выход из программы из MyMenu")
        self.parent.exit_program(113)
        
class MyMenu(npyscreen.TitleSelectOne):
    def create(self, base:Goal, text:MyTextField):
        self.base = base
        # obj = Goal()
        # obj.load_data()
        # self.menu_items = self.set_values([item for item in obj.goal.keys()])
        self.txt = text
        base.load_data()
        self.menu_items = self.item = self.set_values([item for item in base.goal.keys()])
        
        self.add_handlers({
            'q': self.exit_program,  # Привязка клавиши 'q' для выхода
            'c': self.create_write
        })
  
    def when_value_edited(self): # вот она
        super().when_value_edited()
        # ch = int(self._get_ch())
        # print('when_value_edited', ch)
        # if self._get_ch() == 110:
        #     self.create_write(110)
        
        if self.value:
            n_item = self.values[self.value[0]]
            self.txt.values = self.base.get_inform_by_ittem(n_item)
            self.txt.display()
    
    def create_write(self, key):
        self.parent.create_write(key)
    
    def exit_program(self, key):
        print("Инициализрован выход из программы из MyMenu")
        self.parent.exit_program(113)

    
class MainForm(npyscreen.Form):
    DEFAULT_LINES = 40
    DEFAULT_COLUMNS = 130
    OK_BUTTON_TEXT = 'Для выхода нажми <q>'
   
    def create(self):
        self.add_handlers({
            'q': self.exit_program,  # Привязка клавиши 'q' для выхода
            'c': self.create_write,
            'z': self.edit_money,
        })
     
        
        self.help = self.add(HelpText, max_height=4, relx= 5, rely= 2).create()
        self.menu =self.add(MyMenu, name='Выбор цели', max_height=25, max_width=50, relx= 3, rely= 10,  scroll_exit = True)
        self.textfd = self.add(MyTextField, max_height= 25, relx=60, rely= 9)
        self.menu.create(base=self.parentApp.backend, text = self.textfd)
        self.textfd.create()
        

    def get_item_menu_by_index(self):
        try:   
            return self.menu.values[self.menu.value[0]]
        except:
            return None
    def update_menu(self):
        self.menu.values = [key for key in self.parentApp.backend.goal.keys()]
        
    def while_editing(self, input):
        if len(self.menu.values) < len(self.parentApp.backend.goal.keys()):
            self.update_menu()
            self.display()
        
        if self.get_item_menu_by_index():
            self.textfd.values = self.parentApp.backend.get_inform_by_ittem(self.get_item_menu_by_index())
            self.textfd.display()
            self.display()
    
    def edit_money(self, key):
        self.parentApp.switchForm('CHEANGEMONEY')

    def create_write(self, key):
        print("call create_write")
        self.parentApp.switchForm('DATA')
    
    def exit_program(self, key):
        print(f"Инициализрован выход из программы {key}")
        # self.parentApp.backend.save_data()
        self.parentApp.switchForm(None)
    


class My_app(npyscreen.NPSAppManaged): # основной класс приложения
    def onStart(self):
        self.backend = Goal()
        self.backend.load_data()
        self.addForm("MAIN", MainForm, 'Копилка')
        self.addForm("DATA", EnterForm, 'Ввод новой цели')
        self.addForm("CHEANGEMONEY",EntertMoney, 'Ввод колличества средств в копилке')


if __name__ == "__main__":
    app = My_app()
    app.run()