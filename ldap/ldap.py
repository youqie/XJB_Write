import csv
import codecs

OU_List = [
    'OU=Group_1_1,OU=DMtest,DC=dfocus,DC=com',
    'OU=Group_1_2,OU=DMtest,DC=dfocus,DC=com',
    'OU=Group_1_3,OU=DMtest,DC=dfocus,DC=com',
    'OU=Group_1_4,OU=DMtest,DC=dfocus,DC=com',
    'OU=Group_1_5,OU=DMtest,DC=dfocus,DC=com',
    'OU=Group_1_6,OU=DMtest,DC=dfocus,DC=com',
    'OU=Group_1_7,OU=DMtest,DC=dfocus,DC=com',
    'OU=Group_1_8,OU=DMtest,DC=dfocus,DC=com',
    'OU=Group_1_9,OU=DMtest,DC=dfocus,DC=com',
    'OU=Group_1_10,OU=DMtest,DC=dfocus,DC=com',
    'OU=Group_1_11,OU=DMtest,DC=dfocus,DC=com',
    'OU=Group_2_1,OU=Group_1_1,OU=DMtest,DC=dfocus,DC=com',
    'OU=Group_2_2,OU=Group_1_1,OU=DMtest,DC=dfocus,DC=com',
    'OU=Group_2_3,OU=Group_1_1,OU=DMtest,DC=dfocus,DC=com',
    'OU=Group_2_4,OU=Group_1_1,OU=DMtest,DC=dfocus,DC=com',
    'OU=Group_2_11,OU=Group_1_2,OU=DMtest,DC=dfocus,DC=com',
    'OU=Group_3_1,OU=Group_2_1,OU=Group_1_1,OU=DMtest,DC=dfocus,DC=com',
    'OU=Group_3_2,OU=Group_2_1,OU=Group_1_1,OU=DMtest,DC=dfocus,DC=com',
    'OU=Group_3_3,OU=Group_2_1,OU=Group_1_1,OU=DMtest,DC=dfocus,DC=com',
    'OU=Group_3_4,OU=Group_2_1,OU=Group_1_1,OU=DMtest,DC=dfocus,DC=com',
    'OU=Group_3_5,OU=Group_2_1,OU=Group_1_1,OU=DMtest,DC=dfocus,DC=com',
    'OU=Group_4_1,OU=Group_3_1,OU=Group_2_1,OU=Group_1_1,OU=DMtest,DC=dfocus,DC=com',
    'OU=Group_4_2,OU=Group_3_1,OU=Group_2_1,OU=Group_1_1,OU=DMtest,DC=dfocus,DC=com',
    'OU=Group_4_3,OU=Group_3_1,OU=Group_2_1,OU=Group_1_1,OU=DMtest,DC=dfocus,DC=com',
    'OU=Group_5_1,OU=Group_4_1,OU=Group_3_1,OU=Group_2_1,OU=Group_1_1,OU=DMtest,DC=dfocus,DC=com'
]
data = [
    ['givenName', 'sn', 'userPrincipalName', 'sAMAccountName', 'displayName', 'name/cn', 'OUName', 'password', 'pwdLastSet', 'userAccountControl'],
]
from random import choice
for i in range(10000):
    data_add = []
    data_add.append('Test')
    data_add.append('User ' + str(i+1))
    data_add.append('测试员工' + str(i+1))
    data_add.append('测试员工' + str(i+1))
    data_add.append('Test Guy ' + str(i+1))
    data_add.append('Test Guy ' + str(i+1))
    data_add.append(choice(OU_List))
    data_add.append('DFocus1234qwer')
    data_add.append('-1')
    data_add.append('65536')
    data.append(data_add)

f = codecs.open('/Users/yunshen/Desktop/ldap/sample.csv','w','utf-8')
writer = csv.writer(f)
for i in data:
    writer.writerow(i)
f.close()
# f = csv.reader(open('/Users/yunshen/Desktop/ldap/sample.csv', 'r'))
# for i in f:
#     print(i)