from cl import Goal


app = Goal()
# app.add_gaol('Важная задача',100.00, category='Задачи', data='16.05.2025')
# app.add_gaol('Важная задача2',1020.00, category='Задачи', data='16.05.2025')
# app.add_gaol('Накопить',100.00, category='Задачи', data='16.05.2025')
# app.add_gaol('продать',1020.00, category='Задачи', data='16.05.2025')
# app.add_gaol('Смотри',100.00, category='Задачи', data='16.05.2025')
# app.add_gaol('Интерфйс',1020.00, category='Задачи', data='16.05.2025')
# app.add_gaol('яху',100.00, category='Задачи', data='16.05.2025')
# app.add_gaol('бла бла бла',1020.00, category='Задачи', data='16.05.2025')
# app.set_balanc(1000)
# app.print()
# app.__get_total_task__()
# print(app.total_task)
# app.save_data()
app.load_data()
# app.set_balance(500)
# app.print()
# app.set_balance(0)
# app.print()

# app.get_total_progress()

print(app.get_inform_by_ittem('Важная задача'))