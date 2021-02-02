sql_file = open('update.sql', 'w+')
for i in range(3,201):
    string = "UPDATE [dbo].[tb_space] SET [sync_name]=N'压测配置',[sync_account]=N'testroom" + str(i) + "@dfocusm.com',[sync_enabled]=1 WHERE [id]=" + str(i) +";\n"
    sql_file.write(string)