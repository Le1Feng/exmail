import requests
import re
import json
import time
from html import unescape

if __name__ == '__main__':
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                    'Chrome/70.0.3538.102 Safari/537.36 '
    headers = {
        'User-Agent': user_agent
    }

    # 功能对应英文变量名
    part_dict = {
        '通讯录管理' : 'AddressBookManager' ,
        '功能设置' : 'FunctionSetting' ,
        '系统日志' : 'SystemLog' ,
        '新邮件提醒' : 'EmailRemind' ,
        '单点登录' : 'SinglePointLogin' ,
    }

    # 官方文档中未提供默认值且非必须的参数替代值
    unknown_mark = '"unknown_par"'

    # 自动生成的文件的名称
    auto_active_fun_filename = 'auto_active_fun.py'
    auto_setting_filename = 'auto_setting.py'

    # 删除字典中值为None的函数 
    fun_delnone = '''
def del_none(a):
    for i in list(a.keys()):
        if not a[i]:
            del a[i]
    return a
'''

    # 函数注释说明模板
    fun_head_model = """    '''
    [{}]

    requests:
{}
    responses:
{}    '''"""

    # 函数模板
    fun_body_model = '''
    def {}(self,{}):
        {} = {{
{}
        }}
        res = self.req_session.{}(url = URL.{}, {}).json()
        return self.ereturn(res)
'''

    # 获取文档项目并格式化
    req_session = requests.Session()
    url = 'https://exmail.qq.com/qy_mng_logic/doc'
    res_doc = req_session.get(url=url, headers=headers).text
    # 获取一级类目
    start_strs = re.findall('catalog_level_1"> (.+?) <', res_doc)
    # 初始化文档字典
    exmail_doc = {}
    for num in range(len(start_strs)):
        # ['首页' , '开始开发' , '附录'] 中无主动模式API，所以跳过
        if start_strs[num] in ['首页' , '开始开发' , '附录']:
            continue
        # 创建文档字典一级下列表
        exmail_doc[start_strs[num]] = []
        # 获取一级下列表的函数
        content = re.search(start_strs[num] + r'[\s\S]+?catalog_level_1', res_doc).group(0)
        # 遍历API的 名称 和 ID
        for i in re.findall(r'data-doc="(\d+) "\s+"\s+data-parent="\d+">\s+<.+?> (.+?) ' , content):
            # 跳过回调模式的API
            if '回调模式' in i[1]:
                continue
            # 通过 ID 读取API的详细信息，获取 api_method(请求方式) api_url(请求地址) api_par_des(函数参数描述段)
            url = 'https://exmail.qq.com/qy_mng_logic/doc/read/' + i[0]
            res = req_session.get(url=url, headers=headers).json()
            if res['data']['content'].count('pre') is 4:
                api_pre = re.search(r'pre>([\s\S]+?)<', res['data']['content']).group(1).replace('fuzzy": 0,','fuzzy": 0')
            else:
                api_pre = None
            api_method = re.search(r'请求方式：\s+(GET|POST)', res['data']['content']).group(1)
            api_url = re.search(r'请求地址：\s+(.+?)\?', res['data']['content']).group(1)
            api_par_des = re.findall(r'tbody>[\s\S]+?</tbody', res['data']['content'])
            print (api_method , i[1])
            # 函数参数描述段包括 请求参数、返回参数，分别提取格式化
            if len(api_par_des) is 2:
                reres = re.findall(r'td>(.+?)<' , api_par_des[0])
                api_requests = []
                for a in range(0 , len(reres) , 3):
                    par = {}
                    par['name'] = reres[a]
                    par['must'] = reres[a+1]
                    par['des'] = reres[a+2]
                    api_requests.append(par)                
                reres = re.findall('td>(.+?)<' , api_par_des[1])
                api_responses = []
                for a in range(0 , len(reres) , 2):
                    par = {}
                    par['name'] = reres[a]
                    par['des'] = reres[a+1]
                    api_responses.append(par)
            # 完成数据格式并添加
            exmail_doc[start_strs[num]].append({
                'name' : i[1],
                'url' : api_url,
                'pre' : api_pre,
                'method' : api_method,
                'requests' : api_requests,
                'responses' : api_responses,
            })
    
    with open(auto_active_fun_filename, 'w' , encoding = 'utf8') as f:
        _head = "# 注意此文件为 update_from_doc.py 自动生成\n"
        _head += "# 官方文档中未提供默认值且非必须的参数已使用 '{}' 标记\n".format(unknown_mark)
        _head += '# 生成日期：{}\n\n'.format(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
        _head += 'class active_fun:\n'
        f.write(_head)
    with open(auto_setting_filename, 'w' , encoding = 'utf8') as f:
        _head = "# 注意此文件为 update_from_doc.py 自动生成\n"
        _head += '# 生成日期：{}\n\n'.format(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
        _head += 'class URL:\n'
        f.write(_head)

    for a in exmail_doc:
        with open(auto_setting_filename , 'a' , encoding = 'utf8') as f:
            f.write(4*' ' + '# {} \n'.format(a))
        for b in exmail_doc[a]:
            # 从文档中提取数据提交方法
            fun_body_requestmethod = b['method'].lower()

            # 若提交方式为 GET 则使用 params 作为提交数据，并将ACCESS_TOKEN 添加到提交数据中
            # 若提交方式为 POST 则使用 post_data 作为提交数据，并添加 data 参数
            if b['method'] == 'GET':
                fun_body_updataname = 'params'
                fun_body_updata = 12*' ' + "'access_token' : self.ACCESS_TOKEN.{} ,\n".format(part_dict[a])
                fun_body_requestpar = 'params = params'
            else:
                fun_body_updataname = 'post_data'
                fun_body_updata = ''
                fun_body_requestpar = 'params = self.ACCESS_TOKEN.{}.params() , data = json.dumps(post_data)'.format(part_dict[a])

            # 从文档中提取参数的名称注释和默认值
            fun_head_requests = fun_body_pars = fun_body_pars_default = ''
            # 是否有可空参数标记
            _del_mark = False
            for request in b['requests']:
                # 若参数名为 'access_token' 则使用 'access_token' 作为默认参数备注
                # 其他参数从官方文档中提取示例默认参数
                if request['name'] == 'access_token':
                    _par_value = 'access_token'
                else:
                    _par_value = unknown_mark
                    if b['pre']:
                        _par_value = re.search('{}":(.+?)\n'.format(request['name']) , b['pre'])
                        if _par_value:
                            _par_value = _par_value.group(1).strip()
                            if _par_value[-1] == ',':
                                _par_value = _par_value[:-1]
                            if _par_value[0] == '[':
                                _par_value = "'{}'".format(_par_value)
                fun_head_requests += 4*' ' + '{} {} {} ( {} )\n'.format(request['name'],
                                                                        request['must'],
                                                                        request['des'],
                                                                        _par_value)
                # access_token 作为必须参数不单独传入
                if request['name'] == 'access_token':
                    continue

                # 格式化提交数据
                # 避免 python 保留字 type
                _request_name = request['name']
                if _request_name == 'type':
                    _request_name = request['name'].replace('type' , '_type')
                fun_body_updata += 12*' ' + '"{}" : {},\n'.format(request['name'] , _request_name)

                # 如果为非必须参数则标记此API有需要删除参数的可能，并将可省参数(fun_body_pars_default)放置在必须参数(fun_body_pars)后
                if request['must'] == '否' and b['pre']:
                    _del_mark = True
                    fun_body_pars_default += ' {}={},'.format(_request_name , 'None')
                else:
                    fun_body_pars += ' {},'.format(_request_name)

            # 如果存在可空参数，则在提交数据处使用 del_none 过滤
            if _del_mark:
                if b['method'] == 'GET':
                    fun_body_requestpar = 'params = exmail.del_none(params)'
                else:
                    fun_body_requestpar = 'params = self.ACCESS_TOKEN.{}.params() , data = json.dumps(exmail.del_none(post_data))'.format(part_dict[a])

            # 将可省参数(fun_body_pars_default)放置在必须参数(fun_body_pars)后
            fun_body_pars += fun_body_pars_default
            fun_body_pars = fun_body_pars[:-1]

            # 从文档中提取返回说明
            fun_head_responses = ''
            for response in b['responses']:
                fun_head_responses += '    {} {}\n'.format(response['name'], response['des'])
            
            # 根据API的URL设置函数名，URL变量名
            _temp = re.search('bin/(.+)/(.+)', b['url'])
            fun_body_name = '{}_{}'.format(_temp.group(1) , _temp.group(2))
            fun_body_url_name = fun_body_name.upper()

            # 创建URL表对象文件
            with open(auto_setting_filename , 'a' , encoding = 'utf8') as f:
                f.write('    {} = "{}"\n'.format(fun_body_url_name, b['url']))
            
            # 格式化函数头部注释
            fun_head = fun_head_model.format(b['name'] , 
                                            fun_head_requests , 
                                            fun_head_responses)

            # 格式化函数主体
            fun_body = fun_body_model.format(fun_body_name,
                                            fun_body_pars,
                                            fun_body_updataname,
                                            fun_body_updata[:-1],
                                            fun_body_requestmethod,
                                            fun_body_url_name,
                                            fun_body_requestpar)
            
            # 组合函数并输出到文件
            fun_code = fun_head + fun_body
            with open(auto_active_fun_filename , 'a' , encoding = 'utf8') as f:
                f.write(unescape(fun_code) + '\n\n')
