from main import exmail
import conf
import time

_proxy = {
    "http": "127.0.0.1:8080",
    "https": "127.0.0.1:8080",
}

# use your own corpid and secret
# a = exmail(conf.corpid , _proxy)
a = exmail(conf.corpid)
a.get_accesstoken(conf.secrets['AddressBookManager'], 'AddressBookManager')
a.get_accesstoken(conf.secrets['FunctionSetting'], 'FunctionSetting')
a.get_accesstoken(conf.secrets['SystemLog'], 'SystemLog')
a.get_accesstoken(conf.secrets['EmailRemind'], 'EmailRemind')
a.get_accesstoken(conf.secrets['SinglePointLogin'], 'SinglePointLogin')



def test_1_1():
    print ('通讯录管理 - 管理部门', '测试开始')
    department_name = '测试'
    res = a.department_create('测试' , 1)
    department_id = res['id']
    print ('创建部门 {} 成功，部门id: {}'.format(department_name, res['id']))

    res = a.department_update(department_id, '测试_更新' , 1 , 0)
    print ('更新部门 {} 成功，部门id: {}'.format(department_name, department_id))

    res = a.department_list(1)
    print ('获取部门列表成功：\n{}'.format(res['department']))

    res = a.department_search(name = '测试' , fuzzy = 1)
    print ('查找部门成功：\n{}'.format(res['department']))

    res = a.department_delete(id = department_id)
    print ('删除部门成功：\n' , res)

def test_1_2():
    print ('通讯录管理 - 管理成员', '测试开始')
    name = 'user'
    res = a.user_create('user@domin.com' , 
                        'user' , 
                        [1] , 
                        '!@k;lk1;1;L' , 
                        '测试员' , 
                        slaves=['zhangsan@domin.com', 'zhangsan@domin.com'] ,
                        mobile='15112431243'
                        )
    print ('创建成员 {} 成功 '.format(name))

    res = a.user_update('user@domin.com' , 'user_update' , [1] , '测试经理')
    print ('更新成员 {} 成功 '.format(name))

    res = a.user_get('user@domin.com')
    print ('获取成员成功：\n{}'.format(res))

    res = a.user_simplelist(1, 0)
    print ('获取部门成员成功：\n{}'.format(res['userlist']))

    res = a.user_list(1, 0)
    print ('获取部门成员（详情）：\n{}'.format(res['userlist']))

    res = a.user_batchcheck(['user@domin.com' , 'user2@domin.com'])
    print ('批量检查帐号成功：\n{}'.format(res['list']))

    res = a.user_delete('user@domin.com')
    print ('删除成员 {} 成功'.format(name))

def test_1_3():
    print ('通讯录管理 - 管理邮件群组', '测试开始')

    user1 = 'user1@domin.com'
    user2 = 'user2@domin.com'
    a.user_create(user1 , 'user1' , [1] , password = '!@k;lk1;1;L')
    a.user_create(user2 , 'user2' , [1] , password = '!@k;lk1;1;L')
    print ('添加成员 {} {} 成功'.format(user1 , user2))
    print (a.user_simplelist(1 , 1)['userlist'])

    res = a.group_create('group@domin.com' , 'group' , 1 , [user1, user2])
    print ('创建邮件群组 {}成功'.format('group'))

    res = a.group_update('group@domin.com' , 'group_update', allow_type = 0)
    print ('更新邮件群组 {}成功'.format('group'))

    res = a.group_get('group@domin.com')
    print ('获取邮件群组信息成功：\n{}'.format(res))

    res = a.group_delete('group@domin.com')
    print ('删除邮件群组 {}成功'.format('group@domin.com'))

    a.user_delete(user1)
    a.user_delete(user2)
    print ('删除 {} {} 成功'.format(user1, user2))

def test_2():
    print ('功能设置', '测试开始')

    user = 'test_2@domin.com'
    a.user_create(user , 'test_user' , [1] , password = '!@k;lk1;1;L')
    print ('添加成员 {} 成功：\n{}'.format(user , a.user_simplelist(1 , 1)['userlist']))

    res = a.useroption_get(user,[1,2,3,4])
    print ('获取功能属性成功: \n{}'.format(res['option']))

    options = [
        {'type' : 1 , 'value' : '0'},
        {'type' : 2 , 'value' : '0'},
        {'type' : 3 , 'value' : '0'},
    ]
    res = a.useroption_update(user , options)
    print ('更改功能属性成功: \n{}'.format(a.useroption_get(user,[1,2,3,4])['option']))

    a.user_delete(user)
    print ('删除 {} 成功'.format(user))

def test_3():
    print ('系统日志', '测试开始')

    user = 'test_3@domin.com'
    a.user_create(user , 'test_user' , [1] , password = '!@k;lk1;1;L')
    print ('添加成员 {} 成功：\n{}'.format(user , a.user_simplelist(1 , 1)['userlist']))

    res = a.log_mailstatus('domin.com' , '2019-02-08' , time.strftime("%Y-%m-%d", time.localtime(time.time()-86400)) )
    print ('查询邮件概况成功：\n{}'.format(res))

    res = a.log_mail('2019-02-08' , time.strftime("%Y-%m-%d", time.localtime(time.time()-86400)), 0 , user)
    print ('查询邮件成功：\n{}'.format(res))

    res = a.log_login(user , '2019-02-08' , time.strftime("%Y-%m-%d", time.localtime(time.time()-86400)))
    print ('查询成员登录成功：\n{}'.format(res))

    res = a.log_batchjob('2019-02-08' , time.strftime("%Y-%m-%d", time.localtime(time.time()-86400)))
    print ('查询批量任务成功：\n{}'.format(res))

    res = a.log_operation(1 , '2019-02-08' , time.strftime("%Y-%m-%d", time.localtime(time.time()-86400)))
    print ('查询操作记录成功：\n{}'.format(res))
    
    a.user_delete(user)
    print ('删除 {} 成功'.format(user))

def test_4():
    print ('获取邮件未读数', '测试开始')

    user = 'test_4@domin.com'
    a.user_create(user , 'test_user' , [1] , password = '!@k;lk1;1;L')
    print ('添加成员 {} 成功：\n{}'.format(user , a.user_simplelist(1 , 1)['userlist']))

    res = a.mail_newcount(user , '2019-02-08' , time.strftime("%Y-%m-%d", time.localtime(time.time()-86400)))
    print ('获取邮件未读数成功：\n{}'.format(res))

    a.user_delete(user)
    print ('删除 {} 成功'.format(user))

def test_5():
    print ('获取登录企业邮的url', '测试开始')

    user = 'test_5@domin.com'
    a.user_create(user , 'test_user' , [1] , password = '!@k;lk1;1;L')
    print ('添加成员 {} 成功：\n{}'.format(user , a.user_simplelist(1 , 1)['userlist']))

    res = a.service_get_login_url(user)
    print ('获取{} 单点登录URL成功：\n{}'.format(user , res))

    
    # a.user_delete(user)
    # print ('删除 {} 成功'.format(user))
test_1_1()
test_1_2()
test_1_3()
test_2()
test_3()
test_4()
test_5()