# coding=utf-8
import pyautogui

pyautogui.PAUSE = 1.5  # 停顿

# pyautogui.FAILSAFE = True  # 退出控制。鼠标移到左上角会触发FailSafeException，因此快速移动鼠标到左上角也可以停止

# PyAutoGUI使用x，y坐标，屏幕左上角坐标是(0, 0)，分辨率即坐标值
screen_width, screen_height = pyautogui.size()  # 获得屏幕分辨率
currentMouseX, currentMouseY = pyautogui.position()  # 获得当前位置

# pyautogui.moveTo(screen_width/2, screen_height/2, duration=0)  # 在duration时间内完成移动目标
# pyautogui.moveTo(None, 500)  # x方向不变，y方向移动到500
# pyautogui.moveRel(-40,500)  # 相对位置移动

# 缓动/渐变（Tween / Easing）函数的作用是让光标的移动更炫，可以忽略
pyautogui.moveTo(100, 100, 2, pyautogui.easeInQuad)  # 开始很慢，不断加速
pyautogui.moveTo(100, 100, 2, pyautogui.easeOutQuad)  # 开始很快，不断减速
pyautogui.moveTo(100, 100, 2, pyautogui.easeInOutQuad)  # 开始和结束都快，中间比较慢
pyautogui.moveTo(100, 100, 2, pyautogui.easeInBounce)  # 一步一徘徊前进
pyautogui.moveTo(100, 100, 2, pyautogui.easeInElastic)  # 徘徊幅度更大，甚至超过起点和终点

# 鼠标点击击，button参数设置left，middle和right三个键，多次单击可以设置clicks参数
# pyautogui.click()
# pyautogui.click(clicks=2, interval=0.25)  # 两次点击，间隔0.25s
# pyautogui.click(300, 400, button='right', duration=1)  # 包含了move的点击，右键

# pyautogui.doubleClick()
# pyautogui.tripleClick()
# pyautogui.rightClick()

# 鼠标按下和松开函数
pyautogui.mouseDown(button='right')
pyautogui.mouseUp()
pyautogui.mouseUp(button='right', x=100, y=200)  # 移动后松开鼠标右键

pyautogui.scroll(-10)  # 滚轮

# 点击 + 向下拖动
pyautogui.click(941, 34, button='left')
pyautogui.dragRel(0, 100, button='left', duration=5)


# pyautogui.typewrite('Hello world!', interval=0.25)  # 输入字符串和间隔时间

# 以下是输入中文的方法
pyautogui.press('shift')  # 切换输入法中英文
pyautogui.press(['#', ' '])  # press 可以对单个字符或者列表进行操作
pyautogui.press(['x', 'i', 'a', 'o'])
pyautogui.press(['w', 'e', 'i'])
pyautogui.press(' ')


pyautogui.hotkey('shift', 'a')  # 可以使用组合键，等同下列操作

pyautogui.keyDown('shift')
pyautogui.keyDown('a')
pyautogui.keyUp('shift')
pyautogui.keyUp('a')

# 弹窗
pyautogui.alert('这个消息弹窗是文字+OK按钮')
pyautogui.confirm('这个消息弹窗是文字+OK+Cancel按钮')
pyautogui.prompt('这个消息弹窗是让用户输入字符串，单击OK')
str1 = pyautogui.confirm(text='1-10', title='test', buttons=range(10))
str2 = pyautogui.prompt('这个消息弹窗是让用户输入字符串，单击OK')
str3 = pyautogui.password(text='密码', title='填', default='123', mask='*')

pyautogui.screenshot('foo.png')  # 截屏

pyautogui.moveTo(500, 500, duration=10, tween=pyautogui.easeInOutQuad)

