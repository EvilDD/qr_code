import PySimpleGUI as sg
from subprocess import Popen, PIPE, STDOUT
from os.path import abspath, dirname, exists
from os import startfile, makedirs
from sys import path


RUN_DIR = dirname(abspath(__file__))
path.append(RUN_DIR)

SAVE_DIR = RUN_DIR + '/result'
if not exists(SAVE_DIR):
    makedirs(SAVE_DIR)

pt = [
    [sg.Button('生成普通的二维码', key='-PT-')]
]  # 普通
ys = [
    [sg.Text('合入原图片:'), sg.Input('test.png', size=12, key='-PIC-')],
    [sg.Button('生成黑白图二维码', key='-HBPIC-'), sg.Button('生成彩色图二维码', key='-CCPIC-')]
]  # 艺术
dt = [
    [sg.Text('合入动态图:'), sg.Input('test.gif', size=12, key='-GIF-')],
    [sg.Button('生成黑白动态二维码', key='-HBGIF-'), sg.Button('生成彩色动态二维码', key='-CCGIF-')]
]  # 动态
log_col = [
    [sg.Output(size=(60, 20), key='-LOG-', echo_stdout_stderr=True)],
    # [sg.Button('清空日志', key='_CLEARLOG_')]
]
layout = [
    [sg.Text('操作目录:'), sg.Input(SAVE_DIR, size=(45, 1), justification='right', readonly=True), sg.Button(button_text='打开目录', key='_OPENDIR_')],
    [sg.Text('二维码原数据:'), sg.Input('https://qr.alipay.com/fkx11055hmy08edjeipil10?t=1637310468149', key='-DATA-', size=50)],
    [sg.Text('生成边长1-40:'), sg.Input(default_text='10', key='-BC-', size=4), sg.Text('生成对比度1.0-n.0:'),
     sg.Input('1.0', key='-DBD-', size=4), sg.Text('生成亮度1.0-n.0:'), sg.Input('1.0', key='-LD-', size=4)],
    [sg.Text('生成名称:'), sg.Input('result.png', key='-RESULT-', size=12), sg.Text('支持 .jpg .png .bmp .gif 与合并原图后缀要一致')],
    [sg.Frame('普通二维码', pt, font='any 16 bold')],
    [sg.Frame('艺术二维码', ys, font='any 16 bold')],
    [sg.Frame('动态二维码', dt, font='any 16 bold')],
    [sg.Frame('日志输出', log_col, font='any 16 bold')]
]

# Create the Window
window = sg.Window('二维码生成工具', layout)


def defaultCmd(values):
    source_str = values['-DATA-']
    code_size = int(values['-BC-'])
    code_duibidu = float(values['-DBD-'])
    code_light = float(values['-LD-'])
    code_name = values['-RESULT-']
    cmd = f'{RUN_DIR}/amzqr {source_str} -v {code_size} -n {code_name} -con {code_duibidu} -bri {code_light} -d {SAVE_DIR}'
    return cmd


def executeCmd(cmd):  # pyinstaller不可用os自带的popen
    proc = Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT, stdin=PIPE)
    proc.stdin.close()
    proc.wait()
    res = proc.stdout.read().decode('gbk')
    proc.stdout.close()
    assert 'Succeed' in res, res
    # return res


def verifyType(f1, f2):
    # print(exists(f"{SAVE_DIR}/{f2}"), f"{SAVE_DIR}/{f2}")
    if not exists(f"{SAVE_DIR}/{f2}"):
        sg.popup('输入文件不存！', title='提示', font='any 16 bold')
        assert True is False, '文件不存在'
    t1 = f1[-3:]
    t2 = f2[-3:]
    if t1 != t2:
        sg.popup('输入输出文件后缀不一致！', title='提示', font='any 16 bold')
        assert True is False, '后缀问题'


if __name__ == "__main__":
    while True:
        try:
            event, values = window.read()
            # print(event, values)
            if event in (sg.WIN_CLOSED, '退出'):
                break
            elif event == '_OPENDIR_':
                startfile(SAVE_DIR)
            elif event == '-PT-':
                cmd = defaultCmd(values)
                # print(cmd)
                executeCmd(cmd)
            elif event == '-HBPIC-':
                verifyType(values['-RESULT-'], values['-PIC-'])
                cmd = defaultCmd(values)
                cmd_tmp = f'{cmd} -p {SAVE_DIR}/{values["-PIC-"]}'
                executeCmd(cmd_tmp)
            elif event == '-CCPIC-':
                verifyType(values['-RESULT-'], values['-PIC-'])
                cmd = defaultCmd(values)
                cmd_tmp = f'{cmd} -p {SAVE_DIR}/{values["-PIC-"]} -c'
                # print(cmd_tmp)
                executeCmd(cmd_tmp)
            elif event == '-HBGIF-':
                verifyType(values['-RESULT-'], values['-GIF-'])
                cmd = defaultCmd(values)
                cmd_tmp = f'{cmd} -p {SAVE_DIR}/{values["-GIF-"]}'
                executeCmd(cmd_tmp)
            elif event == '-CCGIF-':
                verifyType(values['-RESULT-'], values['-GIF-'])
                cmd = defaultCmd(values)
                cmd_tmp = f'{cmd} -p {SAVE_DIR}/{values["-GIF-"]} -c'
                executeCmd(cmd_tmp)
            else:
                print('无事件')
        except Exception as e:
            print(e)
    window.close()
