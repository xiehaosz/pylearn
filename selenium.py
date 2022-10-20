import time

import texttable
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup       # BeautifulSoup是一个可以从HTML或XML中提取数据的Python库
import lxml                         # BeautifulSoup在解析时依赖解析器，除Python标准库中的HTML解析器外，支持第三方库lxml
from lxml import etree

import random                       # 反反爬虫引入随机值
import subprocess
import re
import os
import json

# selenium:https://selenium-python-zh.readthedocs.io/en/latest/locating-elements.html
# Python爬虫Selenium合集：https://blog.csdn.net/weixin_44110998/article/details/103185785
# 使用Python爬CSDN博客：https://blog.csdn.net/u012814856/article/details/78343539
# BeautifulSoup教程：https://www.jianshu.com/p/424e037c5dd8

# 多层窗口定位：https://blog.csdn.net/Shangxingya/article/details/109175475
# 网站克隆机 HTTrack： https://zhuanlan.zhihu.com/p/81691265


def _set_chrome_options():
    # ChromeOptions类用于操作Chrome驱动程序的各种属性, 通常与Desired Capabilities(期望功能)一起使用
    _options = webdriver.ChromeOptions()

    # 接管已有浏览器
    # cmd启动浏览器: chrome.exe --remote-debugging-port=9527 --user-data-dir="D:\Maxthon\chrome_log"
    _options.add_experimental_option("debuggerAddress", "127.0.0.1:9527")

    # 设置User-Agent:https://zhuanlan.zhihu.com/p/35625779反反爬虫,访问https://httpbin.org/user-agent提取信息
    _options.add_argument('user-agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/55.0.2883.103 Safari/537.36"')

    # chrome_options.add_argument('--proxy-server=http://58.209.151.126:808')

    _options.page_load_strategy = 'eager'                        # 等待浏览器DOMContentLoaded事件

    _options.add_argument('lang=zh_CN.UTF-8')                    # 编码格式
    _options.add_argument('--disable-gpu')                       # 禁用gpu, 谷歌文档提到需要加上这个属性来规避bug
    # _options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片,提升速度
    # _options.add_argument('--disable-javascript')                # 禁用javascript（有错误）

    # _options.add_argument('--headless')                          # 无头模式(无界面):爬虫不需要打开浏览器或者linux不支持界面
    # _options.add_argument('--start-maximized')                   # 窗口最大化模式
    # _options.add_argument('--window-size=1000,500')              # 设置浏览器分辨率(窗口大小)

    # _options.add_argument('--disable-popup-blocking')            # 禁用弹窗
    # _options.add_argument('--make-default-browser')              # 设置Chrome为默认浏览器
    # _options.add_argument('--disable-infobars')                  # 不显示“Chrome正在被自动化软件控制”的通知

    _options.add_argument('--no-sandbox')
    _options.add_argument("--disable-extensions")                # 禁用Chrome浏览器上现有的扩展
    _options.add_argument("--allow-running-insecure-content")
    _options.add_argument("--ignore-certificate-errors")
    _options.add_argument("--disable-single-click-autofill")
    _options.add_argument("--disable-autofill-keyboard-accessory-view[8]")
    _options.add_argument("--disable-full-form-autofill-ios")

    # prefs = {'profile.default_content_settings.popups': 0,                      # 禁用保存弹窗
    #          'download.default_directory': r'D:\download',                      # 设置默认下载路径
    #          "profile.default_content_setting_values.automatic_downloads": 1    # 允许多文件下载
    #          }
    # _options.add_experimental_option('prefs', prefs)

    # # 修改windows.navigator.webdriver，防机器人识别机制, selenium自动登陆判别机制
    # _options.add_experimental_option('excludeSwitches', ['enable-automation'])

    _options.add_experimental_option('w3c', False)
    # _options.add_experimental_option('perfLoggingPrefs', {'enableNetwork': True, 'enablePage': False,})

    # Desired capabilities类用于修改Web驱动程序的多个属性, 通过键值对{key:value}更改web驱动程序的各个属性
    _cap = DesiredCapabilities.CHROME
    _cap['loggingPrefs'] = {'performance': 'ALL'}   # log查找动态信息 goog:loggingPrefs?

    return _options, _cap


def _get_xhr_logs(chrome):
    log_xhr_array = []
    for type_log in chrome.log_types:
        for row in chrome.get_log(type_log):    # 动态内容只能get一次,再次get会变化
            try:
                log = json.loads(row['message'])['message']
                if log['method'] == 'Network.responseReceived':
                    if log['params']['type'] == "XHR":  # 去掉静态js、css等，仅保留xhr请求
                        log_xhr_array.append(log)
            except Exception:
                continue
    # （可选）过滤特定内容
    res_url_list = []
    for xhr in log_xhr_array:
        try:
            _url = xhr['params']['response']['url']
            if _url[-10:] == 'adapt.m3u8':
                res_url_list.append(_url)
        except Exception:
            continue
    return res_url_list  # log_xhr_array


def validate_name(_name):
    # 无效字符统一替换为下划线, 返回可作为文件名的字符串，'/ \ : * ? " < > |'
    r_str = r"[\/\\\:\*\?\"\<\>\|]"
    return re.sub(r_str, '_', _name)


def _save_element_link_page(browser, element, path, title=None, home_handle=None, pause=0):
    # 将网页元素所链接的网页保存为mhtml文件
    _home_page = home_handle if home_handle else browser.current_window_handle
    title = title if title else validate_name(element.text)
    try:
        browser.execute_script(r'window.open("%s");' % element.get_attribute('href'))
        if pause > 0:
            time.sleep(pause)
    except Exception:
        pass
    browser.switch_to.window(browser.window_handles[-1])

    _res = browser.execute_cdp_cmd('Page.captureSnapshot', {})
    with open(os.path.join(path, '%s.mhtml' % title), 'w', newline='') as _f:
        _f.write(_res['data'])
        _f.close()
    browser.close()
    browser.switch_to.window(_home_page)


if __name__ == '__main__':
    # 设置属性并创建浏览器实例
    options, capabilities = _set_chrome_options()
    # driver = webdriver.Chrome(r'C:\Python3\Scripts\chromedriver', options=options)

    # subprocess.Popen(r'"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" '
    #                  r'--remote-debugging-port=9527 --user-data-dir="D:\Maxthon\chrome_log"')
    # time.sleep(1)
    driver = webdriver.Chrome(r'C:\Python3\Scripts\chromedriver', desired_capabilities=capabilities, options=options)

    # 窗口操作-------------------------------------------------------------------------------------------
    # driver.fullscreen_window()
    driver.maximize_window()
    # driver.minimize_window()

    # # 设置窗口大小和位置
    # driver.set_window_position(30, 30)
    # driver.set_window_size(500, 500)
    # driver.set_window_rect(10, 10, 1050, 708)     # {'height', 'width', 'x', 'y'}

    # 获取窗口大小和位置
    # print(driver.get_window_position())
    # print(driver.get_window_size())
    # print(driver.get_window_rect())

    # 访问操作-------------------------------------------------------------------------------------------
    # driver.set_page_load_timeout(5)                                     # 设定页面加载限时,超时抛异常
    # driver.set_script_timeout(5)                                         # 设置页面异步js执行超时
    # try:                                                                # 访问地址
    #     driver.get('http://rnd-skb.huawei.com/user/threatlib/stlItemList')
    # except TimeoutError:
    #     driver.execute_script('window.stop()')                          # 加载超时执行停止,可执行后续动作
    # print(driver.title)                                                 # 当前窗口标题
    # print(driver.current_url)                                           # 当前窗口地址
    # home_handle = driver.current_window_handle                          # 获取当前句柄
    #
    # driver.execute_script('window.open("https://www.baidu.com");')      # 新标签页
    # new_handle = driver.window_handles[-1]                              # 获取新标签句柄

    # 切换标签页（新窗口必须要主动切换）
    # handles = driver.window_handles                                     # 获取所有标签页
    # driver.switch_to.window(new_handle)                                 # 句柄为惰性,必须主动切换

    # driver.forward()
    # driver.back()
    # driver.refresh()
    # driver.close()                                                      # 关闭页面
    # driver.switch_to.window(home_handle)                                # 句柄切换

    # driver.execute_script('js')                                         # 执行js脚本

    # 等待机制----------------------------------------------------------------------------------------------
    # # 基于页面元素的等待WebDriverWait配合until或until_not(method返回True或False, message='')
    # wait_element = WebDriverWait(driver, timeout=5, poll_frequency=0.5, ignored_exceptions=None).\
    #     until(EC.presence_of_element_located((By.ID, "kw")))    # 超时默认抛NoSuchElementException
    # # 隐式等待：当脚本执行到任意元素定位时，循环定位直到成功继续执行，或超时抛出NoSuchElementException
    # driver.implicitly_wait(5)
    #
    # # 处理弹窗/警告框----------------------------------------------------------------------------------------
    # driver.switch_to.alert().text()
    # driver.switch_to.alert().accept()
    # driver.switch_to.alert().dismiss()
    # driver.switch_to.alert().send_keys(Keys.ENTER)
    #
    # # 页面框架切换：当网页由多个框架组成时需要切换框架才能定位元素----------------------------------------------------
    # # frame标签有frameset、frame、iframe三种，frameset跟其他普通标签没有区别，不影响定位，selenium对frame与iframe的操作相同
    # driver.switch_to.frame('frame_name')
    # driver.switch_to.frame(driver.find_elements_by_tag_name("iframe")[0])
    # driver.switch_to.frame(1)
    #
    # rq = driver.find_element_by_xpath('//iframe[@scrolling="no"]')      # 当一个框架没有name或者id属性时, 先定位后切换
    # driver.switch_to.frame(rq)
    # driver.switch_to.parent_frame()                                     # 返回到上一层框架
    # driver.switch_to.default_content()                                  # 返回到主文档

    # 定位页面元素：find_element（单个）和find_elements（多个）-------------------------------------------------
    # element = driver.switch_to.active_element                           # 页面激活的元素
    # element = driver.find_element_by_id('id_text')                      # 通过name选择元素
    # element = driver.find_element_by_name('cheese')                     # 通过name选择元素
    # element = driver.find_element_by_class_name('cheese')               # 通过class选择元素
    # element = driver.find_element_by_link_text('full_text')             # 通过超链接文本（精确）选择元素
    # element = driver.find_element_by_partial_link_text('word')          # 通过超链接文本（模糊）匹配的第一个符合条件的元素
    # element = driver.find_element_by_tag_name('iframe')                 # 通过tag选择元素,如果iframe这个tag在本html中唯一

    # 查找页面元素BY_XPATH：可以定位标签，也可以@任意属性，以下为一些示例：
    # elements = driver.find_elements_by_xpath("//*[@href]")                      # 获取所有的href元素（*匹配任意标签）
    # elements = driver.find_elements_by_xpath("//div[@id='chapter']")            # 通过tag(标签)定位
    # element = driver.find_element_by_xpath("/html/body/div/div/input[@href]")   # 绝对路径
    # element = driver.find_element_by_xpath("//form[@id='01']/span/input")       # 相对路径（//代表相对路径）
    # element = driver.find_element_by_xpath("//*[@id='nr']/option[3]")           # 索引（多个同级子元素,从1开始）
    # element = driver.find_element_by_xpath("//*[@name='Jim' and @id='01']")     # 同级条件组合
    # element = driver.find_element_by_xpath("//*[@id='01'/a[@name='01']")        # 不同级条件组合
    #
    # element = driver.find_element_by_xpath("//a[contains(@name,'baidu')]")      # 模糊匹配: contains
    # element = driver.find_element_by_xpath("//a[starts-with(@name,'baidu')]")   # 模糊匹配: starts-with
    # element = driver.find_element_by_xpath("//a[contains(text(),'baidu')]")     # 转换为文本的模糊匹配

    # 返回元素同级兄弟节点: following-sibling::*
    # driver.find_element_by_xpath("//div/a[contains(text(), '%s')]/following-sibling::*" % "word")

    # 表格定位: 固定格式：.//*[@id='表格id']/tbody/tr[行数]/td[列数]/a-----------------------------------------
    # x, y = 6, 4     # 参数化
    # driver.find_element_by_xpath(f"//*[@id=table']/tbody/tr[{x}/td[{y}]/a")
    # t = f'.//*[text()="上传附件"]/../../td[@class="text-right"]/a[@title="编辑"]'
    # element = driver.find_element_by_xpath(t)                       # 定位表格后的按钮

    # 页面元素操作.方法------------------------------------------------------------------------------------------
    # element = driver.find_element_by_id("//*[@name='button']")
    # e_text = element.text                                           # 获取元素文本
    # e_text = element.get_attribute('textContent')                   # 获取元素文本（如果上面的不行）
    # element.get_attribute("innerText")                              # 获取不可见页面元素的文本（例如折叠的多级菜单）
    # e_size = element.size                                           # 获取元素尺寸
    # e_show = element.is_displayed()                                 # 获取元素可见状态
    #
    # e_link = element.get_attribute('href')                          # 获取元素属性
    # e_html = element.get_attribute('innerHTML')                     # 元素HTML片段,'outerHTML'包含对象本身的标签
    #
    # element.send_keys('OK')                                         # 模拟按键输入
    # element.send_keys(Keys.CONTROL, 'a')                            # 模拟按键Ctrl+A
    # element.clear()                                                 # （输入框）清除文本
    # element.submit()                                                # 等同于回车
    # element.click()                                                 # 单击
    # element.double_click()                                          # 双击

    # 实现selenium中可能会遇到element.click()不起作用
    # driver.find_elements_by_xpath("//button[@type='submit']")[0].send_keys(Keys.ENTER)  # 改用键盘方法
    # driver.execute_script("arguments[0].click();", element)                             # 或使用js代码来触发点击操作

    # 下拉框中动态加载的元素定位不到或无法定位的问题, 通过js修改元素属性
    # driver.execute_script("arguments[0].style = 'width: 360px;left: 360px;top: 465px;';", element)
    # 通过js动态修改元素
    # driver.execute_script(f"document.getElementById('{attr_id}').remove();")
    # driver.execute_script(f"document.getElementsByClassName('{attr_cls}')[0].remove();")

    # 页面元素操作.ActionChains方法创建操作队列, 调用perform()执行操作, 方法列表如下-------------------------------
    """
    click(on_element=None)                                          单击鼠标左键
    click_and_hold(on_element=None)                                 长按鼠标左键
    context_click(on_element=None)                                  点击鼠标右键
    double_click(on_element=None)                                   双击鼠标左键
    move_by_offset(xoffset, yoffset)                                鼠标从当前位置移动到某个坐标
    release(on_element=None)                                        在某个元素位置松开鼠标左键
    move_to_element(to_element)                                     鼠标移动到某个元素
    drag_and_drop(source, target)                                   拖拽到某个元素然后松开
    drag_and_drop_by_offset(source, xoffset, yoffset)               拖拽到某个坐标然后松开
    move_to_element_with_offset(to_element, xoffset, yoffset)       移动到距某个元素（左上角坐标）多少距离的位置
    send_keys(*keys_to_send)                                        发送某个键到当前焦点的元素
    key_down(value, element=None)                                   按下某个键盘上的键
    key_up(value, element=None)                                     松开某个键
    send_keys_to_element(element, *keys_to_send)                    发送某个键到指定元素
    perform()                                                       执行链中的所有动作
    """
    # # ActionChains链式语法
    # # ActionChains(driver).click(element).double_click(element).context_click(element).perform()
    #
    # # ActionChains分步语法
    # actions = ActionChains(driver)
    # actions.move_to_element(element)
    # target = driver.find_element_by_name("xxx")
    # actions.drag_and_drop(element, target).perform()
    #
    # # 模拟滑动验证条
    # slide_bar = driver.find_element_by_xpath('***')                 # 找到滑动条元素
    # x_stops = [5, 6, 19, 40, 42, 50]                                # 设置滑动路径
    # ActionChains(driver).click_and_hold(slide_bar).perform()        # 点击滑块并保持
    # for _x in x_stops:
    #     # 按照预先设计的路径滑动并引入随机变化反反爬虫
    #     ActionChains(driver).move_by_offset(xoffset=_x+random.randint(0, 2), yoffset=0).perform()
    # ActionChains(driver).release().perform()                        # 释放
    #
    # # 鼠标拖拽操作
    # ActionChains(driver).drag_and_drop(driver.find_element_by_id("draggable"),
    #                                    driver.find_element_by_id("droppable")).perform()

    # 页面滚动/翻页--------------------------------------------------------------------------------------
    # driver.execute_script('window.scrollBy(0,500)')                     # 滚动指定像素(x, y),支持正负值
    # driver.execute_script("arguments[0].scrollIntoView();", element)    # 滚动至元素可见
    #
    # # 1. 定位到下一页按键
    # driver.find_element_by_link_text("next").click()
    # # 2. 标签属性逐步定位到按键
    # pagelist = driver.find_element_by_class_name("pagelist")
    # pagelist.find_elements_by_class_name("nextpage").click()
    # # 3. 定位页码输入框
    # input_page = driver.find_element_by_xpath('//input[@id="Page_input"]')
    # input_page.clear()
    # input_page.send_keys('1')
    # input_page.send_keys(Keys.ENTER)
    # # 4. js脚本翻页（需要js脚本定位到页码）
    # driver.execute_script("document.getElementsByClassName('pagelist')[7].click()")

    # 网页转换------------------------------------------------------------------------------------------
    # soup = BeautifulSoup(driver.page_source, 'xml')                 # 转化为beautiful soup格式提取数据
    # html = etree.HTML(driver.page_source)                           # 转化为xml文档使用xpath语法提取数据

    # COOKIE设置：免去输入账号、密码、验证码过程--------------------------------------------------------------
    # cookies = driver.get_cookies()                                  # 手动登录后获取新的cookies
    # # driver.delete_all_cookies()                                     # 清空cookies
    # # driver.delete_cookie("CookieName")                              # 删除指定cookies
    #
    # for _cookie in cookies:
    #     driver.add_cookie(_cookie)
    # driver.get('https://w3.huawei.com/')                            # 访问相关页面看是否成功登录
    """
    invalid cookie domain:
    selenium的默认域名为data, cookie中带域名，在设置cookie时发现当前域名不包含在cookie中，会抛出设置失败
    在设置cookies前先访问需要登录的地址再添加cookies, 添加成功后再次跳转（或refresh）
    """

    # 保存网页-------------------------------------------------------------------------------------------
    # # mhtml格式
    # res = driver.execute_cdp_cmd('Page.captureSnapshot', {})        # 执行chrome开发工具命令获取mhtml内容
    # with open('res.mhtml', 'w', newline='') as f:
    #     f.write(res['data'])
    #     f.close()
    #
    # # html格式
    # with open('res.html', 'wb') as f:
    #     f.write(driver.page_source.encode("gbk", "ignore"))         # 忽略非法字符
    #     f.close()

    # driver.quit()

    # 提取的数据保存为excel---------------------------------------------------------------------------------
    # import pandas as pd
    # from openpyxl import load_workbook
    # web_df = pd.DataFrame('要保存的数据')
    # book = load_workbook('test.xlsx')                               # 读取被写入的Excel工作簿
    # writer = pd.ExcelWriter(r'test.xlsx', engine='openpyxl')        # 建立写入对象
    # writer.book = book
    # writer.sheets = {ws.title: ws for ws in book.worksheets}
    # web_df.to_excel(writer, sheet_name='sheet0', header=False, index=False, startrow=2, startcol=2)
    # writer.save()
    # writer.close()
    
"""website==========================================================================="""
    driver.set_page_load_timeout(5)                                     # 设定页面加载限制时间

    # try:
    #     driver.get('http://w3.huawei.com/next/indexa.html')
    #     time.sleep(1)
    #     # 在Python中隐藏和加密密码: http://www.codebaoku.com/it-python/it-python-238119.html
    #     driver.find_element_by_xpath("//input[@class='user']").send_keys('x00336957')
    #     driver.find_element_by_xpath("//input[@class='psw']").send_keys('Bwatest)0461wtl')
    #     driver.find_element_by_xpath("//input[@class='btn']").click()
    # except Exception:
    #     driver.execute_script('window.stop()')
    #     driver.quit()

    home = driver.current_window_handle
    home_path = r'D:\downloads'

    res = []
    driver.get('http://www.baidu.com')
    time.sleep(10)

    menus = driver.find_elements_by_xpath("//div[@class='scrollable-menu']/ul/li")
    if not menus:
        driver.quit()
        raise RuntimeError

    header = validate_name(driver.title.split('|')[0].replace(' ', '').replace('\t', ''))

    # res.append(header)  # 单标题
    for menu in menus:
        sub_title = validate_name(menu.get_attribute('title').replace(' ', '').replace('.', '_'))
        res.append(header + (sub_title if sub_title[0].isdigit() else ('_' + sub_title)))

        sub_icons = menu.find_elements_by_xpath("./div//div[starts-with(@class,'type-icon doc-block')]")
        if len(sub_icons) == 1:
            sub_items = menu.find_elements_by_xpath("./div//div[@class='li-text']")
        elif len(sub_icons) > 1:
            all_items = menu.find_elements_by_xpath("./div//div[@class='subsection-li-text']")
            sub_items = [all_items[i] for i in range(len(sub_icons)) if
                         ('video-block' in sub_icons[i].get_attribute('class'))]
        else:
            sub_items = []
        if not sub_items:
            res.pop()
            continue

        try:
            folder = menu.find_element_by_xpath("./div/ul")
            # driver.execute_script("arguments[0].scrollIntoView();", folder)
            driver.execute_script("arguments[0].style = '';", folder)
        except Exception:
            pass

        _get_xhr_logs(driver)   # 取一次清除历史记录避免干扰
        for _item in sub_items:
            print(sub_title, _item.text)
            flag_click_ok, counter = False, 3
            while not flag_click_ok and (counter > 0):
                try:
                    counter -= 1
                    time.sleep(1)
                    driver.execute_script("arguments[0].click();", _item)
                    time.sleep(1)
                    flag_click_ok = True
                except Exception:
                    pass
            if not flag_click_ok:
                driver.quit()
                raise RuntimeError('click failed')
            res.extend(_get_xhr_logs(driver))
    driver.quit()
    for i in res:
        print(i)
