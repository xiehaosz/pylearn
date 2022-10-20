import requests
from lxml import etree


def post_request(url):
    # 请求头
    header = {
        # 用户请求的代理，建议请求header中要加上，避免服务端接口有反爬虫设置
        'user-agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/55.0.2883.103 Safari/537.36"'
        # "User-Agent": "PostmanRuntime/7.28.1",
        
        "Content-Type": "application/json",                         # 设置连接请求类型为json
        "Postman-Token": "0f7408f7-9869-48ba-9433-871bf4b6f560"     # token，这里使用的是postman
        }
    body = {"key1": "value1", "key2": "value2"}                     # 请求数据
    response = requests.post(url, data=body, headers=header)        # 发送请求
    return response.json()                                          # 返回json格式


def get_page(url):
    # 代理设置
    proxies = {
        "http": "http://12.34.56.78:9527",                          # 一般代理
        "https": "user:password@12.34.56.79:9527"                   # 私密代理
    }

    auth = ('user', 'password')                                     # 客户端验证

    # 直接登录-------------------------------------------------------------------------------------------
    page = requests.get(url, auth=auth, proxies=proxies)            # verify参数置为True可验证SSL证书

    print(page.cookies)
    print(page.url)
    print(page.encoding)                                            # 头部字符编码
    print(page.status_code)                                         # 响应码
    print(page.text)                                                # 响应内容, Unicode格式
    print(page.content)                                             # 响应内容, 二进制字节流格式（可用于提取图片等）

    html = etree.HTML(page.content.decode('utf-8'))
    element = html.xpath('//table/tr[2]/td')                        # 转换为HTML格式,使用xpath查找

    print(etree.tostring(element))                                  # 输出节点内容, 对比输出格式
    print(etree.tostring(element, encoding='utf-8').decode('utf-8'))

    # 创建session登录, 可以保留cookies
    session = requests.session()
    auth_data = {"email": "xx@y.com", "password": "psw123"}
    session.post('http://www.renren.com/PLogin.do', data=auth_data)
    page = session.get('url')                                       # 继续访问页面
