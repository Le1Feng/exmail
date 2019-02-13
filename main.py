import requests
import json
from setting import URL

class ExmailException(Exception):
    def __init__(self, err):
        Exception.__init__(self, err)

class ACCESS_TOKEN:
    def __init__(self):
        self.AddressBookManager = None
        self.SinglePointLogin = None
        self.EmailRemind = None
        self.FunctionSetting = None
        self.SystemLog = None
        # requests.packages.urllib3.disable_warnings()
    
    class __token:
        def __init__(self, value):
            self.v = value
        def __str__(self):
            return self.v
        def params(self):
            return {'access_token' : self.v}

    def set(self, part , value):
        if (part is 'AddressBookManager'):
            self.AddressBookManager = self.__token(value)
        elif (part is 'SinglePointLogin'):
            self.SinglePointLogin = self.__token(value)
        elif (part is 'EmailRemind'):
            self.EmailRemind = self.__token(value)
        elif (part is 'FunctionSetting'):
            self.FunctionSetting = self.__token(value)
        elif (part is 'SystemLog'):
            self.SystemLog = self.__token(value)

class exmail:
    R'''
    [创建部门]

    requests:
    access_token 是 调用接口凭证 ( None )
    name 是 部门名称。长度限制为1~64个字节，字符不能包括\:*?"<>｜ ( "广州研发中心" )
    parentid 是 父部门id。id为1可表示根部门 ( 1 )
    order 否 在父部门中的次序值。order值小的排序靠前，1-10000为保留值，若使用保留值，将被强制重置为0。 ( 0 )

    responses:
    errcode 返回码
    errmsg 对返回码的文本描述内容
    id 创建的部门id。id为64位整型数
    '''
    def department_create(self, name, parentid, order=None):
        post_data = {
            "name" : name,
            "parentid" : parentid,
            "order" : order,
        }
        res = self.req_session.post(url = URL.DEPARTMENT_CREATE, params = self.ACCESS_TOKEN.AddressBookManager.params() , data = json.dumps(exmail.del_none(post_data))).json()
        return self.ereturn(res)

    @staticmethod
    def del_none(a):
        for i in list(a.keys()):
            if not a[i]:
                del a[i]
        return a

    R'''
    [更新部门]

    requests:
    access_token 是 调用接口凭证 ( None )
    id 是 部门id ( 2 )
    name 否 更新的部门名称。长度限制为1~64个字节，字符不能包括\:*?"<>｜。修改部门名称时指定该参数 ( "广州研发中心" )
    parentid 否 父部门id。id为1可表示根部门 ( 1 )
    order 否 在父部门中的次序值。order值小的排序靠前，1-10000为保留值，若使用保留值，将被强制重置为0。 ( 0 )

    responses:
    errcode 返回码
    errmsg 对返回码的文本描述内容
    '''
    def department_update(self, id, name=None, parentid=None, order=None):
        post_data = {
            "id" : id,
            "name" : name,
            "parentid" : parentid,
            "order" : order,
        }
        res = self.req_session.post(url = URL.DEPARTMENT_UPDATE, params = self.ACCESS_TOKEN.AddressBookManager.params() , data = json.dumps(exmail.del_none(post_data))).json()
        return self.ereturn(res)


    '''
    [删除部门]

    requests:
    access_token 是 调用接口凭证 ( "unknown_par" )
    id 是 部门id。（注：不能删除根部门；不能删除含有子部门、成员的部门） ( "unknown_par" )

    responses:
    errcode 返回码
    errmsg 对返回码的文本描述内容
    '''
    def department_delete(self, id):
        params = {
            'access_token' : self.ACCESS_TOKEN.AddressBookManager ,
            "id" : id,
        }
        res = self.req_session.get(url = URL.DEPARTMENT_DELETE, params = params).json()
        return self.ereturn(res)


    '''
    [获取部门列表]

    requests:
    access_token 是 调用接口凭证 ( "unknown_par" )
    id 否 部门id。获取指定部门及其下的子部门。id为1时可获取根部门下的子部门。 ( "unknown_par" )

    responses:
    errcode 返回码
    errmsg 对返回码的文本描述内容
    department 部门列表数据。以部门的order字段从小到大排列
    id 部门id
    name 部门名称
    parentid 父部门id。
    order 在父部门中的次序值。order值小的排序靠前
    '''
    def department_list(self, id):
        params = {
            'access_token' : self.ACCESS_TOKEN.AddressBookManager ,
            "id" : id,
        }
        res = self.req_session.get(url = URL.DEPARTMENT_LIST, params = params).json()
        return self.ereturn(res)


    '''
    [查找部门]

    requests:
    access_token 是 调用接口凭证 ( None )
    name 否 查找的部门名字，必须合法 ( "邮箱产品部" )
    fuzzy 否 1/0：是否模糊匹配 ( 0 )

    responses:
    errcode 返回码
    errmsg 对返回码的文本描述内容
    department 部门列表数据。以部门的order字段从小到大排列
    id 部门id
    name 部门名称
    parentid 父部门id。根部门为0
    order 在父部门中的次序值。order值小的排序靠前。
    path 部门路径，部门用’/ ’作分割符
    '''
    def department_search(self, name=None, fuzzy=None):
        post_data = {
            "name" : name,
            "fuzzy" : fuzzy,
        }
        res = self.req_session.post(url = URL.DEPARTMENT_SEARCH, params = self.ACCESS_TOKEN.AddressBookManager.params() , data = json.dumps(exmail.del_none(post_data))).json()
        return self.ereturn(res)


    '''
    [创建成员]

    requests:
    access_token 是 调用接口凭证 ( None )
    userid 是 成员UserID。企业邮帐号名，邮箱格式 ( " zhangsan@gzdev.com " )
    name 是 成员名称。长度为1~64个字节 ( "张三" )
    department 是 成员所属部门id列表，不超过20个 ( '[1, 2]' )
    position 否 职位信息。长度为0~64个字节 ( "产品经理" )
    mobile 否 手机号码 ( "15913215XXX" )
    tel 否 座机号码 ( "123456" )
    extid 否 编号 ( "01" )
    gender 否 性别。1表示男性，2表示女性 ( "1" )
    slaves 否 别名列表 ( '[zhangsan@gz.com, zhangsan@bjdev.com]' )
    password 是 密码 ( "******" )
    cpwd_login 否 用户重新登录时是否重设密码, 登陆重设密码后，该标志位还原。0表示否，1表示是，缺省为0 ( 0 )

    responses:
    errcode 返回码
    errmsg 对返回码的文本描述内容
    '''
    def user_create(self, userid, name, department, password, position=None, mobile=None, tel=None, extid=None, gender=None, slaves=None, cpwd_login=None):
        post_data = {
            "userid" : userid,
            "name" : name,
            "department" : department,
            "position" : position,
            "mobile" : mobile,
            "tel" : tel,
            "extid" : extid,
            "gender" : gender,
            "slaves" : slaves,
            "password" : password,
            "cpwd_login" : cpwd_login,
        }
        res = self.req_session.post(url = URL.USER_CREATE, params = self.ACCESS_TOKEN.AddressBookManager.params() , data = json.dumps(exmail.del_none(post_data))).json()
        return self.ereturn(res)


    '''
    [更新成员]

    requests:
    access_token 是 调用接口凭证 ( None )
    userid 是 成员UserID。企业邮帐号名，邮箱格式 ( " zhangsan@gzdev.com " )
    name 否 成员名称。长度为0~64个字节 ( "张三" )
    department 否 成员所属部门id列表，不超过20个 ( '[1, 2]' )
    position 否 职位信息。长度为0~64个字节 ( "产品经理" )
    mobile 否 手机号码 ( "15913215421" )
    tel 否 座机号码 ( None )
    extid 否 编号 ( None )
    gender 否 性别。1表示男性，2表示女性 ( "1" )
    slaves 否 别名列表 ( None )
    enable 否 启用/禁用成员。1表示启用成员，0表示禁用成员 ( 1 )
    password 否 密码 ( "******" )
    cpwd_login 否 用户重新登录时是否重设密码, 登陆重设密码后，该标志位还原。0表示否，1表示是，缺省为0 ( 1 )

    responses:
    errcode 返回码
    errmsg 对返回码的文本描述内容
    '''
    def user_update(self, userid, name=None, department=None, position=None, mobile=None, tel=None, extid=None, gender=None, slaves=None, enable=None, password=None, cpwd_login=None):
        post_data = {
            "userid" : userid,
            "name" : name,
            "department" : department,
            "position" : position,
            "mobile" : mobile,
            "tel" : tel,
            "extid" : extid,
            "gender" : gender,
            "slaves" : slaves,
            "enable" : enable,
            "password" : password,
            "cpwd_login" : cpwd_login,
        }
        res = self.req_session.post(url = URL.USER_UPDATE, params = self.ACCESS_TOKEN.AddressBookManager.params() , data = json.dumps(exmail.del_none(post_data))).json()
        return self.ereturn(res)


    '''
    [删除成员]

    requests:
    access_token 是 调用接口凭证 ( "unknown_par" )
    userid 是 成员UserID。企业邮帐号名，邮箱格式 ( "unknown_par" )

    responses:
    errcode 返回码
    errmsg 对返回码的文本描述内容
    '''
    def user_delete(self, userid):
        params = {
            'access_token' : self.ACCESS_TOKEN.AddressBookManager ,
            "userid" : userid,
        }
        res = self.req_session.get(url = URL.USER_DELETE, params = params).json()
        return self.ereturn(res)


    '''
    [获取成员]

    requests:
    access_token 是 调用接口凭证 ( "unknown_par" )
    userid 是 成员UserID ( "unknown_par" )

    responses:
    errcode 返回码
    errmsg 对返回码的文本描述内容
    userid 成员UserID
    name 成员名称
    department 成员所属部门id列表
    position 职位信息
    mobile 手机号码
    tel 座机号码
    extid 编号
    gender 性别。0表示未定义，1表示男性，2表示女性
    enable 启用/禁用成员。1表示启用成员，0表示禁用成员
    slaves 别名列表
    cpwd_login 用户重新登录时是否重设密码, 登陆重设密码后，该标志位还原。0表示否，1表示是，缺省为0
    '''
    def user_get(self, userid):
        params = {
            'access_token' : self.ACCESS_TOKEN.AddressBookManager ,
            "userid" : userid,
        }
        res = self.req_session.get(url = URL.USER_GET, params = params).json()
        return self.ereturn(res)


    '''
    [获取部门成员]

    requests:
    access_token 是 调用接口凭证 ( "unknown_par" )
    department_id 是 获取的部门id。id为1时可获取根部门下的成员 ( "unknown_par" )
    fetch_child 否 1/0：是否递归获取子部门下面的成员 ( "unknown_par" )

    responses:
    errcode 返回码
    errmsg 对返回码的文本描述内容
    userlist 成员列表
    userid 成员UserID
    name 成员名称
    department 成员所属部门
    '''
    def user_simplelist(self, department_id, fetch_child):
        params = {
            'access_token' : self.ACCESS_TOKEN.AddressBookManager ,
            "department_id" : department_id,
            "fetch_child" : fetch_child,
        }
        res = self.req_session.get(url = URL.USER_SIMPLELIST, params = params).json()
        return self.ereturn(res)


    '''
    [获取部门成员（详情）]

    requests:
    access_token 是 调用接口凭证 ( "unknown_par" )
    department_id 是 获取的部门id。id为1时可获取根部门下的成员 ( "unknown_par" )
    fetch_child 否 1/0：是否递归获取子部门下面的成员 ( "unknown_par" )

    responses:
    errcode 返回码
    errmsg 对返回码的文本描述内容
    userlist 成员列表
    userid 成员UserID。企业邮帐号名，邮箱格式
    name 成员名称
    department 成员所属部门id列表
    position 职位信息
    mobile 手机号码
    tel 座机号码
    extid 编号
    gender 性别。0表示未定义，1表示男性，2表示女性
    slaves 别名列表
    cpwd_login 用户重新登录时是否重设密码, 登陆重设密码后，该标志位还原。0表示否，1表示是，缺省为0。
    '''
    def user_list(self, department_id, fetch_child):
        params = {
            'access_token' : self.ACCESS_TOKEN.AddressBookManager ,
            "department_id" : department_id,
            "fetch_child" : fetch_child,
        }
        res = self.req_session.get(url = URL.USER_LIST, params = params).json()
        return self.ereturn(res)


    '''
    [批量检查帐号]

    requests:
    access_token 是 调用接口凭证 ( None )
    userlist 是 成员帐号，每次检查不得超过20个 ( '["zhangsan@bjdev.com", "zhangsangroup@shdev.com"]' )

    responses:
    errcode 返回码
    errmsg 对返回码的文本描述内容
    list 列表数据
    user 成员帐号
    type 帐号类型。-1:帐号号无效;  0:帐号名未被占用;  1:主帐号;  2:别名帐号;  3:邮件群组帐号
    '''
    def user_batchcheck(self, userlist):
        post_data = {
            "userlist" : userlist,
        }
        res = self.req_session.post(url = URL.USER_BATCHCHECK, params = self.ACCESS_TOKEN.AddressBookManager.params() , data = json.dumps(post_data)).json()
        return self.ereturn(res)


    '''
    [创建邮件群组]

    requests:
    access_token 是 调用接口凭证 ( None )
    groupid 是 邮件群组名称 ( "zhangsangroup@gzdev.com" )
    groupname 是 邮件群组名称 ( "zhangsangroup  )
    userlist 否 成员帐号，userlist，grouplist，department至少一个。成员由userlist，grouplist，department共同组成 ( '["zhangsanp@gzdev.com", "lisi@gzdev.com"]' )
    grouplist 否 成员邮件群组，userlist，grouplist，department至少一个。成员由userlist，grouplist，department共同组成 ( '["group@gzdev.com"]' )
    department 否 成员部门，userlist，grouplist，department至少一个。成员由userlist，grouplist，department共同组成 ( '[1, 2]' )
    allow_type 是 群发权限。0: 企业成员,  1任何人， 2:组内成员，3:指定成员 ( 4 )
    allow_userlist 否 群发权限为指定成员时，需要指定成员 ( '["zhangsanp@gzdev.com"]' )

    responses:
    errcode 返回码
    errmsg 对返回码的文本描述内容
    '''
    def group_create(self, groupid, groupname, allow_type, userlist=None, grouplist=None, department=None, allow_userlist=None):
        post_data = {
            "groupid" : groupid,
            "groupname" : groupname,
            "userlist" : userlist,
            "grouplist" : grouplist,
            "department" : department,
            "allow_type" : allow_type,
            "allow_userlist" : allow_userlist,
        }
        res = self.req_session.post(url = URL.GROUP_CREATE, params = self.ACCESS_TOKEN.AddressBookManager.params() , data = json.dumps(exmail.del_none(post_data))).json()
        return self.ereturn(res)


    '''
    [更新邮件群组]

    requests:
    access_token 是 调用接口凭证 ( None )
    groupid 是 邮件群组id，邮件格式 ( "zhangsangroup@gzdev.com" )
    groupname 否 邮件群组名称 ( "zhangsangroup" )
    userlist 否 成员帐号，userlist，grouplist，department至少一个。成员由userlist，grouplist，department共同组成 ( '["zhangsanp@gzdev.com","lisi@gzdev.com"]' )
    grouplist 否 成员邮件群组，userlist，grouplist，department至少一个。成员由userlist，grouplist，department共同组成 ( '["group@gzdev.com"]' )
    department 否 成员部门，userlist，grouplist，department至少一个。成员由userlist，grouplist，department共同组成 ( '[1,2]' )
    allow_type 否 群发权限。0: 企业成员,1任何人，2:组内成员，3:指定成员 ( 3 )
    allow_userlist 否 群发权限为指定成员时，需要指定成员 ( '["zhangsanp@gzdev.com"]' )

    responses:
    errcode 返回码
    errmsg 对返回码的文本描述内容
    '''
    def group_update(self, groupid, groupname=None, userlist=None, grouplist=None, department=None, allow_type=None, allow_userlist=None):
        post_data = {
            "groupid" : groupid,
            "groupname" : groupname,
            "userlist" : userlist,
            "grouplist" : grouplist,
            "department" : department,
            "allow_type" : allow_type,
            "allow_userlist" : allow_userlist,
        }
        res = self.req_session.post(url = URL.GROUP_UPDATE, params = self.ACCESS_TOKEN.AddressBookManager.params() , data = json.dumps(exmail.del_none(post_data))).json()
        return self.ereturn(res)


    '''
    [删除邮件群组]

    requests:
    access_token 是 调用接口凭证 ( "unknown_par" )
    groupid 是 邮件群组id，邮件格式 ( "unknown_par" )

    responses:
    errcode 返回码
    errmsg 对返回码的文本描述内容
    '''
    def group_delete(self, groupid):
        params = {
            'access_token' : self.ACCESS_TOKEN.AddressBookManager ,
            "groupid" : groupid,
        }
        res = self.req_session.get(url = URL.GROUP_DELETE, params = params).json()
        return self.ereturn(res)


    '''
    [获取邮件群组信息]

    requests:
    access_token 是 调用接口凭证 ( "unknown_par" )
    groupid 是 邮件群组id，邮件格式 ( "unknown_par" )

    responses:
    errcode 返回码
    errmsg 对返回码的文本描述内容
    groupid 邮件群组id，邮件格式
    groupname 邮件群组名称
    userlist 成员帐号
    grouplist 成员邮件群组
    department 成员部门
    allow_type 群发权限。0: 企业成员,  1任何人， 2:组内成员，3:指定成员
    allow_userlist 群发权限为指定成员时，需要指定成员，否则赋值失效
    '''
    def group_get(self, groupid):
        params = {
            'access_token' : self.ACCESS_TOKEN.AddressBookManager ,
            "groupid" : groupid,
        }
        res = self.req_session.get(url = URL.GROUP_GET, params = params).json()
        return self.ereturn(res)


    '''
    [获取功能属性]

    requests:
    access_token 是 调用接口凭证 ( None )
    userid 是 成员UserID ( "zhangsan@gzdev.com" )
    type 是 功能设置属性类型 ( '[1,2,3]' )

    responses:
    errcode 返回码
    errmsg 对返回码的文本描述内容
    option 功能设置属性
    '''
    def useroption_get(self, userid, _type):
        post_data = {
            "userid" : userid,
            "type" : _type,
        }
        res = self.req_session.post(url = URL.USEROPTION_GET, params = self.ACCESS_TOKEN.FunctionSetting.params() , data = json.dumps(post_data)).json()
        return self.ereturn(res)


    '''
    [更改功能属性]

    requests:
    access_token 是 调用接口凭证 ( None )
    userid 是 成员UserID。企业邮帐号名，邮箱格式 ( "zhangsan@gzdev.com" )
    option 是 功能设置属性 ( '[{"type":1,"value":"0"},{"type":2,"value":"1"},{"type":3,"value":"0"}]}' )

    responses:
    errcode 返回码
    errmsg 对返回码的文本描述内容
    '''
    def useroption_update(self, userid, option):
        post_data = {
            "userid" : userid,
            "option" : option,
        }
        res = self.req_session.post(url = URL.USEROPTION_UPDATE, params = self.ACCESS_TOKEN.FunctionSetting.params() , data = json.dumps(post_data)).json()
        return self.ereturn(res)


    '''
    [查询邮件概况]

    requests:
    access_token 是 调用接口凭证 ( None )
    domain 是 域名 ( "gzdev.com" )
    begin_date 是 开始日期。格式为2016-10-01 ( "2016-10-01" )
    end_date 是 结束日期。格式为2016-10-07 ( "2016-10-07" )

    responses:
    errcode 返回码
    errmsg 对返回码的文本描述内容
    sendsum 发信总量
    recvsum 收信总量
    '''
    def log_mailstatus(self, domain, begin_date, end_date):
        post_data = {
            "domain" : domain,
            "begin_date" : begin_date,
            "end_date" : end_date,
        }
        res = self.req_session.post(url = URL.LOG_MAILSTATUS, params = self.ACCESS_TOKEN.SystemLog.params() , data = json.dumps(post_data)).json()
        return self.ereturn(res)


    '''
    [查询邮件]

    requests:
    access_token 是 调用接口凭证 ( None )
    begin_date 是 开始日期。格式为2016-10-01 ( "2016-10-01" )
    end_date 是 开始日期。格式为2016-10-07 ( "2016-10-07" )
    mailtype 是 邮件类型。0:收信+发信  1:发信  2:收信 ( 1 )
    userid 否 筛选条件：指定成员帐号 ( "zhangsanp@gzdev.com" )
    subject 否 筛选条件：包含指定主题内容 ( "test" )

    responses:
    errcode 返回码
    errmsg 对返回码的文本描述内容
    list 列表数据
    mailtype 邮件类型。1:发信  2:收信
    sender 发信者
    receiver 收信者
    time 时间（时间戳格式）
    status 邮件状态
    '''
    def log_mail(self, begin_date, end_date, mailtype, userid=None, subject=None):
        post_data = {
            "begin_date" : begin_date,
            "end_date" : end_date,
            "mailtype" : mailtype,
            "userid" : userid,
            "subject" : subject,
        }
        res = self.req_session.post(url = URL.LOG_MAIL, params = self.ACCESS_TOKEN.SystemLog.params() , data = json.dumps(exmail.del_none(post_data))).json()
        return self.ereturn(res)


    '''
    [查询成员登录]

    requests:
    access_token 是 调用接口凭证 ( None )
    userid 是 成员UserID。企业邮帐号名，邮箱格式-10-01 ( "zhangsanp@gzdev.com" )
    begin_date 是 开始日期。格式为2016-10-01 ( "2016-10-01" )
    end_date 是 结束日期。格式为2016-10-07 ( "2016-10-07" )

    responses:
    errcode 返回码
    errmsg 对返回码的文本描述内容
    list 列表数据
    time 时间（时间戳格式）
    ip 登录ip
    type 登录类型
    '''
    def log_login(self, userid, begin_date, end_date):
        post_data = {
            "userid" : userid,
            "begin_date" : begin_date,
            "end_date" : end_date,
        }
        res = self.req_session.post(url = URL.LOG_LOGIN, params = self.ACCESS_TOKEN.SystemLog.params() , data = json.dumps(post_data)).json()
        return self.ereturn(res)


    '''
    [查询批量任务]

    requests:
    access_token 是 调用接口凭证 ( None )
    begin_date 是 开始日期。格式为2016-10-01 ( "2016-10-01" )
    end_date 是 结束日期。格式为2016-10-07 ( "2016-10-07" )

    responses:
    errcode 返回码
    errmsg 对返回码的文本描述内容
    list 列表数据
    time 时间（时间戳格式）
    operator 操作人员
    type 操作类型
    '''
    def log_batchjob(self, begin_date, end_date):
        post_data = {
            "begin_date" : begin_date,
            "end_date" : end_date,
        }
        res = self.req_session.post(url = URL.LOG_BATCHJOB, params = self.ACCESS_TOKEN.SystemLog.params() , data = json.dumps(post_data)).json()
        return self.ereturn(res)


    '''
    [查询操作记录]

    requests:
    access_token 是 调用接口凭证 ( None )
    type 是 类型 ( 0 )
    begin_date 是 开始日期。格式为2016-10-01 ( "2016-10-01" )
    end_date 是 结束日期。格式为2016-10-07 ( "2016-10-07" )

    responses:
    errcode 返回码
    errmsg 对返回码的文本描述内容
    list 列表数据
    time 时间（时间戳格式）
    operator 操作人员
    type 登录类型
    operand 关联数据
    remark 备注信息：
    '''
    def log_operation(self, _type, begin_date, end_date):
        post_data = {
            "type" : _type,
            "begin_date" : begin_date,
            "end_date" : end_date,
        }
        res = self.req_session.post(url = URL.LOG_OPERATION, params = self.ACCESS_TOKEN.SystemLog.params() , data = json.dumps(post_data)).json()
        return self.ereturn(res)


    '''
    [获取邮件未读数]

    requests:
    access_token 是 调用接口凭证 ( None )
    userid 是 成员UserID ( None )
    begin_date 是 开始日期。格式为2016-10-01 ( "2016-10-01" )
    end_date 是 结束日期。格式为2016-10-07 ( "2016-10-07" )

    responses:
    errcode 返回码
    errmsg 对返回码的文本描述内容
    count 未读邮件数
    '''
    def mail_newcount(self, userid, begin_date, end_date):
        params = {
            'access_token' : self.ACCESS_TOKEN.EmailRemind ,
            "userid" : userid,
            "begin_date" : begin_date,
            "end_date" : end_date,
        }
        res = self.req_session.get(url = URL.MAIL_NEWCOUNT, params = params).json()
        return self.ereturn(res)


    '''
    [获取登录企业邮的url]

    requests:
    access_token 是 调用接口凭证 ( "unknown_par" )
    userid 是 成员UserID ( "unknown_par" )

    responses:
    errcode 返回码
    errmsg 对返回码的文本描述内容
    login_url 登录跳转的url，一次性有效，不可多次使用。
    expires_in url有效时长，单位为秒
    '''
    def service_get_login_url(self, userid):
        params = {
            'access_token' : self.ACCESS_TOKEN.SinglePointLogin ,
            "userid" : userid,
        }
        res = self.req_session.get(url = URL.SERVICE_GET_LOGIN_URL, params = params).json()
        return self.ereturn(res)


    def __init__(self, corpid , proxy = None, verify = True):
        self.corpid = corpid
        self.ACCESS_TOKEN = ACCESS_TOKEN()
        self.req_session = requests.Session()
        if (proxy):
            self.req_session.proxies = proxy
        if not verify:
            self.req_session.verify = False
    
    def ereturn(self, res):
        if res['errcode'] is 0:
            return res
        raise ExmailException('exmail request error({}): {}'.format(res['errcode'] , res['errmsg']))

    

    def get_accesstoken(self, corpsecret, part):
        if not hasattr(self.ACCESS_TOKEN, part):
            raise ExmailException('Unknown accesstoken part: {}'.format(part))
        params = {
            'corpid' : self.corpid,
            'corpsecret' : corpsecret
        }
        res = self.req_session.get(url = URL.ACCESS_TOKEN , params = params).json()
        if res['errcode'] is 0:
            self.ACCESS_TOKEN.set(part , res['access_token'])
            # print(self.ACCESS_TOKEN.AddressBookManager)
        else:
            raise ExmailException('Request error: {}'.format(res))
        return self
    
    def callback_server(self, serobj):
        import http.server
        import socketserver
        import base64
        from re import findall
        from urllib.parse import parse_qs
        from hashlib import sha1
        from Crypto.Cipher import AES
        from socket import ntohl
        from struct import unpack

        def getSHA1(token, timestamp, nonce, encrypt):
                sortlist = [token, timestamp, nonce, encrypt]
                sortlist.sort()
                sha = sha1()
                sha.update("".join(sortlist).encode())
                return  sha.hexdigest()

        class exmail_callback_server(http.server.BaseHTTPRequestHandler):
            @staticmethod
            def decrypt(text):
                key = base64.b64decode(serobj.AESkey +"=")  
                assert len(key) == 32
                cryptor = AES.new(key , AES.MODE_CBC , key[:16])
                # 使用BASE64对密文进行解码，然后AES-CBC解密
                plain_text  = cryptor.decrypt(base64.b64decode(text))
                # pad = ord(plain_text[-1]) 
                pad = plain_text[-1]
                # 去掉补位字符串 
                #pkcs7 = PKCS7Encoder()
                #plain_text = pkcs7.encode(plain_text)   
                # 去除16位随机字符串
                content = plain_text[16:-pad]
                xml_len = ntohl(unpack("I",content[ : 4])[0])
                xml_content = content[4 : xml_len+4] 
                from_corpid = content[xml_len+4:]
                if  from_corpid.decode() != serobj.corpid:
                    return False
                return xml_content

            @staticmethod
            def data_decrypt(exmail_data):
                if 'msg_signature' in exmail_data:
                    msg_signature = exmail_data['msg_signature'][0]
                    if 'timestamp' in exmail_data:
                        timestamp = exmail_data['timestamp'][0]
                        if 'nonce' in exmail_data:
                            nonce = exmail_data['nonce'][0]
                            if 'data_encrypt' in exmail_data:
                                data_encrypt_list = findall(r'CDATA\[(.+?)\]' , exmail_data['data_encrypt'])
                                if len(data_encrypt_list) is 3 and data_encrypt_list[0] == serobj.corpid:
                                    data_encrypt = data_encrypt_list[2]
                                else:
                                    return False
                            # 携带 'echostr' 则为 '验证URL有效性'
                            elif 'echostr' in exmail_data:
                                data_encrypt = exmail_data['echostr'][0]
                            signature = getSHA1(serobj.token, timestamp, nonce, data_encrypt)
                            if signature == msg_signature:
                                rec_plaintext = exmail_callback_server.decrypt(data_encrypt)
                                return rec_plaintext.decode()
                return False 


            def do_GET(self):
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                exmail_data = parse_qs(self.path[2:])
                res = self.data_decrypt(exmail_data)
                if res is not False:
                    self.wfile.write(res)
                    serobj.url_verity()

            def do_POST(self):
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                datas = self.rfile.read(int(self.headers['content-length'])).decode()
                exmail_data = parse_qs(self.path[2:])
                exmail_data['data_encrypt'] = datas
                res = self.data_decrypt(exmail_data)
                if res is not False:
                    self.wfile.write(b'1')
                    serobj.mail_receive(res)

            
            def output_response_header(self, content):
                enc = "UTF-8"
                content = content.encode(enc)            
                self.send_response(200)  
                self.send_header("Content-type", "text/html; charset=%s" % enc)  
                self.send_header("Content-Length", str(len(content)))  
                self.end_headers()  

        with socketserver.TCPServer((serobj.ser_addr, serobj.port), exmail_callback_server) as httpd:
            print("serving at port", serobj.port)
            httpd.serve_forever()

class exmail_callback_server_obj():
    def __init__(self, token , AESkey , corpid , ser_addr = '' , port = 80):
        self.token = token
        self.AESkey = AESkey
        self.corpid = corpid
        self.ser_addr = ser_addr
        self.port = port
    
    def mail_receive(self , data):
        print (data)

    def url_verity(self):
        print ('url verity success')
    
