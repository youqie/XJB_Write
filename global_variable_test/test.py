import global_var
global_var.set_value('hello', 'aaa')
print(global_var.get_value('hello'))
global_var.set_value('aa', 12312312)
print(global_var.get_value('aa'))

global_var.clear_up()
print(global_var.get_value('hello'))
print(global_var.get_value('aa'))

global_var.set_value('hello', 'bbb')
print(global_var.get_value('hello'))