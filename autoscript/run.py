import os
import re
import shutil

import sys

SCRIPT_DIR = sys.path[0]


class HookParam(object):
    def __init__(self):
        self.online_helper_class = 'NotFound'
        self.category_method = 'NotFound'
        self.toolbar_method = 'NotFound'
        self.found_method = 'NotFound'
        self.game_center_method = 'NotFound'
        self.unicom_method = 'j'  # 此方法目前为空实现

        self.theme_class = 'NotFound'
        self.theme_param_class = 'NotFound'

        self.bmall_class = 'NotFound'
        self.banner_class = 'NotFound'


def print_tips(text):
    print('\n>>> ' + text)


def enter_bl_folder():
    print_tips('Enter Working Directory')
    os.chdir(os.path.join(SCRIPT_DIR, 'out/bl'))
    print(os.getcwd())


def print_result(param):
    print('onlineHelper       = ' + param.online_helper_class)
    print('onlineCategoryGame = ' + param.category_method)
    print('onlineToolbarGame  = ' + param.toolbar_method)
    print('onlineUnicomSim    = ' + param.unicom_method)
    print('onlineFoundGame    = ' + param.found_method)
    print('onlineGameCenter   = ' + param.game_center_method)
    print()
    print('ThemeClass      = ' + param.theme_class)
    print('ThemeParamClass = ' + param.theme_param_class)
    print()
    print('BMallClass      = ' + param.bmall_class)
    print('BannerClass     = ' + param.banner_class)

    print()
    os.system('pause')


# 从 OnlineHelper 的代码块匹配
def get_online_method(line, content, regex):
    end = content.find(line)
    start = content.rfind('.method', 0, end)

    methods = regex.findall(content[start:end])

    return methods[0]


# 查找 OnlineHelper 中的方法名
def find_online_helper(file, param):
    # 文件指针置 0
    file.seek(0)

    content = file.read()
    regex = re.compile(r'\.method public static ([a-zA-z])\(.*\)Z')

    # 因为之前经过 read() 操作
    # 所以这里文件指针再次置 0
    file.seek(0)

    for line in file:
        if 'hide_gamecenter_in_category_channels' in line:
            param.category_method = get_online_method(line, content, regex)

        elif 'hide_gamecenter_in_toolbar_channels' in line:
            param.toolbar_method = get_online_method(line, content, regex)

        elif 'hide_gamecenter_in_discover_channels' in line:
            param.found_method = get_online_method(line, content, regex)

        elif 'hide_gamecenter_in_game_tid_channels' in line:
            param.game_center_method = get_online_method(line, content, regex)


def find_key_text(name, param):
    with open(name, encoding='UTF-8') as file:

        regex = re.compile(r'\s+iget-object v\d+, v\d+, Lcom/bilibili/api/promo/BiliPromoV2;'
                           r'->topBanners:Lcom/bilibili/api/promo/BiliPromoV2\$[a-z]+;')

        # 逐行遍历文件内容
        for line in file:
            # 在线参数配置
            if '"OnlineParamsHelper"' in line:
                param.online_helper_class = name
                find_online_helper(file, param)

            # # 主题
            # elif r'\u8be5\u76ae\u80a4\u4e0d\u5b58\u5728' in line:
            #     param.theme_class = name
            #     file.seek(0)
            #     methods = re.findall('\.method private a\(Lbl/([a-zA-z]{3});\)V', file.read())
            #     param.theme_param_class = methods[0]
            #
            # # 周边商城
            # elif 'http://bmall.bilibili.com' in line:
            #     param.bmall_class = name
            #
            # # 首页推荐
            # elif regex.match(line):
            #     param.banner_class = name


def find_files():
    print_tips('Finding...')
    param = HookParam()
    walk_dir = os.walk(os.curdir)

    for root, dirs, files in walk_dir:
        # 遍历文件
        for name in files:
            find_key_text(name, param)

    # 切换回脚本目录
    os.chdir('../..')

    # if os.path.exists('out'):
    #     print_tips('Delete Temp Files')
    #     shutil.rmtree('out')

    print_tips('Find Complete')
    print_result(param)


def run():
    enter_bl_folder()
    find_files()


def decode_dex():
    try:
        path = sys.argv[1]
    except IndexError:
        print_tips('Class.dex File Not Found')
        exit()
    else:
        print_tips('Decode class.dex...')

        command = 'java -jar {jarPath} disassemble {apkPath} -o {outDir}'
        os.system(command
                  # .replace('{jarPath}', os.path.join(SCRIPT_DIR, 'baksmali.jar'))
                  .replace('{jarPath}', os.path.join(SCRIPT_DIR, 'E:/WorkSpace/Android/BiliNeat/autoscript/baksmali.jar'))
                  .replace('{apkPath}', path)
                  .replace('{outDir}', os.path.join(SCRIPT_DIR, 'out')))


def show_entrance():
    print()
    print('====================================')
    print('‖                                ‖')
    print('‖    BiliNeat Adaptive Script    ‖')
    print('‖          Author:iAcn           ‖')
    print('‖                                ‖')
    print('====================================')


if __name__ == '__main__':
    show_entrance()
    # decode_dex()
    run()
