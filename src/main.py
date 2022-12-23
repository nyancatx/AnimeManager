import json
import copy

cmd_prompt = '>>>'
config = {}
config_path = 'config.json'

welcome_content = '''
    _          _                __  __                                   
   / \\   _ __ (_)_ __ ___   ___|  \\/  | __ _ _ __   __ _  __ _  ___ _ __ 
  / _ \\ | '_ \\| | '_ ` _ \\ / _ \\ |\\/| |/ _` | '_ \\ / _` |/ _` |/ _ \\ '__|
 / ___ \\| | | | | | | | | |  __/ |  | | (_| | | | | (_| | (_| |  __/ |   
/_/   \\_\\_| |_|_|_| |_| |_|\\___|_|  |_|\\__,_|_| |_|\\__,_|\\__, |\\___|_|   
                                                         |___/           

输入"help"以获得帮助'''

help_content = '''
    添加番剧：
        add     （会有提示语）
        add -h <番剧昵称> <番剧网址>         （如果不修改某项请用*代替）
        add -b  （会有提示语）
        add {-bh | -hb} <番剧昵称> <番剧网址> <番剧昵称> <番剧网址>......
        关于 add 的详细说明请输入 add -?
    删除番剧：
        del     （会有提示语）
        del -h <番剧序号>
        del {-af | -fa} (删除所有番剧信息)
        关于 del 的详细说明请输入 del -?
    列出番剧列表：
        list 或 ls
        关于 list 的详细说明请输入 list -?
    编辑番剧信息：
        edit    （会有提示语）
        edit -h <番剧序号> <修改后番剧昵称> <修改后番剧网址>         （如果不修改某项请用*代替）
        关于 edit 的详细说明请输入 edit -?
    插入番剧信息：
        ins     （会有提示语）
        ins -h <番剧序号> <番剧昵称> <番剧网址>         （如果不修改某项请用*代替）  
        ins -b  （会有提示语）
        ins {-bh | -hb} <番剧序号> <番剧昵称> <番剧网址> <番剧昵称> <番剧网址>......
        关于 ins 的详细说明请输入 ins -?
    帮助：
        help
    退出：
        exit
'''

exit_content = '再见！'


# 程序功能函数区
# --------------------------------------------------------------------------------

class AnimeManager():

    def a_help(self, cmd):
        print(help_content)

    def a_list(self, cmd):
        global config
        mods = cmd[1]
        return_words = ''

        if is_animeList_empty() == True:
            print('列表为空。')
            raise Exception('列表为空。')
        else:
            if mods == '-normal':
                for i in range(len(config['anime'])):
                    anime_name = config['anime'][i]['name']
                    anime_url = config['anime'][i]['url']

                    return_words += f'{i + 1}. {anime_name}   {anime_url}\n'

                print(return_words)
                return return_words

            elif mods == '-h':  # 无输出模式（返回字符串）
                for i in range(len(config['anime'])):
                    anime_name = config['anime'][i]['name']
                    anime_url = config['anime'][i]['url']

                    return_words += f'{i + 1}. {anime_name}   {anime_url}\n'

                return return_words

            elif mods == '-?':
                print('''
    列出番剧列表。
    
    
    无参数 / -normal   正常输出番剧列表。
    
    -h                返回番剧列表，不输出。    
                ''')

            else:
                print('[Error]: 没有此参数!')

    def a_add(self, cmd):
        global config
        mods = cmd[1]
        anime_name = ''
        anime_url = ''

        if mods == '-normal':
            while True:
                anime_name = input('请输入番剧昵称： ')
                if anime_name == '':
                    print('[Error]: 番剧昵称不能为空！')
                    raise Exception('[Error]: 番剧昵称不能为空！')
                else:
                    break
            anime_url = input('请输入番剧对应网址（若没有则按回车）：')

            config['anime'].append({'name': anime_name, 'url': anime_url})
            save_config(config)

        elif mods == '-h':  # 无输出模式
            anime_name = cmd[2]
            anime_url = cmd[3]
            if anime_name == '':
                print('[Error]: 番剧昵称不能为空！')
                raise Exception('[Error]: 番剧昵称不能为空！')
            if anime_url == '*':
                anime_url = ''

            config['anime'].append({'name': anime_name, 'url': anime_url})
            save_config(config)

        elif mods == '-b':  # 批量添加模式
            return_words = ''
            print('请输入番剧昵称和对应网址（若要停止输入则多输入一段空行，若没有网址则输入*，昵称与网址不能有空格）：')

            while True:
                try:
                    words = input().split()
                    anime_name = words[0]
                    anime_url = words[1]

                    if anime_url == '*':
                        anime_url = ''
                    return_words += f'{anime_name} {anime_url}\n'
                    config['anime'].append({'name': anime_name, 'url': anime_url})

                    save_config(config)
                except:
                    break

            return return_words

        elif mods == '-bh' or mods == '-hb':  # 无输出批量添加模式
            # 若要停止输入则多输入一段空行，若没有网址则输入*，名称与网址不能有空格
            return_words = ''
            words = copy.copy(cmd)
            del words[1]
            del words[0]
            loop_num = len(words) / 2
            if (int(loop_num) * 10) != int(loop_num * 10):
                print('[Error]: 请输入正确的数据数量!')
                raise Exception('[Error]: 请输入正确的数据数量!')
            num = 0
            for i in range(int(loop_num)):
                anime_name = words[num]
                num += 1
                anime_url = words[num]
                num += 1
                if anime_url == '*':
                    anime_url = ''

                config['anime'].append({'name': anime_name, 'url': anime_url})
                return_words += f'{anime_name} {anime_url}\n'

            save_config(config)
            return return_words

        elif mods == '-?':
            print('''
    添加番剧信息到番剧列表。
    
    
    无参数 / -normal   根据提示语添加番剧信息。
    
    -h                没有提示语，直接添加番剧信息。
        用法： add -h <番剧昵称> <番剧网址>
        
    -b                批量添加番剧信息，有提示语。
    
    -bh / -hb         批量添加番剧信息，无提示语，直接添加。
        注：若要停止输入则多输入一段空行，若没有网址则输入*，名称与网址不能有空格。
        用法： add {-bh | -hb} <番剧昵称> <番剧网址> <番剧昵称> <番剧网址>......
            ''')

        else:
            print('[Error]: 没有此参数!')

    def a_del(self, cmd):
        global config
        mods = cmd[1]
        del_anime_num = ''

        if mods == '-normal':
            list_content = self.a_list(['', '-h'])

            if list_content == 'empty':
                print('列表为空。')
                raise Exception('列表为空。')
            else:
                del_anime_num = input('请输入你要删除的番剧序号（若没有则回车）：')
                if del_anime_num == '':
                    raise Exception('[Error]: 番剧序号不能为空！')
                del_anime_num = int(del_anime_num) - 1

                try:
                    del config['anime'][del_anime_num]
                except:
                    print('[Error]: 没有此序号!')

                save_config(config)

        elif mods == '-h':  # 无输出模式
            del_anime_num = cmd[2]
            if del_anime_num == '':
                raise Exception('[Error]: 番剧序号不能为空！')
            del_anime_num = int(del_anime_num) - 1

            try:
                del config['anime'][del_anime_num]
            except:
                print('[Error]: 没有此序号!')

            save_config(config)

        elif mods == '-af' or mods == '-fa':  # 删除所有信息
            words = input('你确定要删除所有番剧信息？（YES/NO）：')
            words = words.upper()
            if words == 'YES':
                for i in range(len(config['anime'])):
                    del config['anime'][0]
                save_config(config)
            elif words == 'NO':
                return
            else:
                print('[Error]: 没有此选项!')

        elif mods == '-?':
            print('''
    删除番剧列表中的番剧信息。
    
    
    无参数 / -normal   根据提示语删除番剧信息。
    
    -h                没有提示语，直接删除番剧信息。
        用法： del -h <番剧序号>
        
    -af / -fa         删除所有番剧信息
        用法： del {-af | -fa}
            ''')

        else:
            print('[Error]: 没有此参数!')

    def a_edit(self, cmd):
        global config
        mods = cmd[1]
        sel_anime_num = ''
        anime_name = ''
        anime_url = ''

        if mods == '-normal':
            list_content = self.a_list(['', '-h'])

            if list_content == 'empty':
                print('列表为空。')
                raise Exception('列表为空。')
            else:
                print(list_content)

                sel_anime_num = int(input('请输入你要编辑的番剧序号（若不编辑则按回车）：')) - 1
                if sel_anime_num > len(config['anime']) or sel_anime_num < 0:
                    print('[Error]: 没有此序号！')
                    raise Exception('[Error]: 没有此序号！')
                elif sel_anime_num == '':
                    raise Exception('[Error]: 番剧序号不能为空！')
                anime_name = input('请输入修改后的名称（若不修改则按回车）：')
                anime_url = input('请输入修改后的网址（若不修改则按回车）：')

                if anime_name != '':
                    config['anime'][sel_anime_num]['name'] = anime_name
                if anime_url != '':
                    config['anime'][sel_anime_num]['url'] = anime_url

                save_config(config)
                return f"{config['anime'][sel_anime_num]['name']} {config['anime'][sel_anime_num]['url']}"

        elif mods == '-h':  # 无输出模式
            sel_anime_num = int(cmd[2]) - 1

            anime_name = cmd[3]
            anime_url = cmd[4]

            if anime_name != '*':
                config['anime'][sel_anime_num]['name'] = anime_name
            if anime_url != '*':
                config['anime'][sel_anime_num]['url'] = anime_url

            save_config(config)
            return f"{config['anime'][sel_anime_num]['name']} {config['anime'][sel_anime_num]['url']}"

        elif mods == '-?':
            print('''
    编辑番剧信息。
    
    
    无参数 / -normal   根据提示语删除番剧信息。
    
    -h                没有提示语，直接删除番剧信息。
        注：如果不修改某项请用*代替。
        用法： edit -h <番剧序号> <修改后番剧昵称> <修改后番剧网址>
            ''')

        else:
            print('[Error]: 没有此参数!')

    def a_ins(self, cmd):
        global config
        mods = cmd[1]
        anime_num = None
        anime_name = ''
        anime_url = ''

        if mods == '-normal':
            while True:
                anime_num = int(input('请输入插入在哪个序号之后：'))
                if anime_num == '':
                    print('[Error]: 番剧序号不能为空！')
                    raise Exception('[Error]: 番剧序号不能为空！')

                anime_name = input('请输入番剧昵称： ')
                if anime_name == '':
                    print('[Error]: 番剧昵称不能为空！')
                    raise Exception('[Error]: 番剧昵称不能为空！')
                else:
                    break
            anime_url = input('请输入番剧对应网址（若没有则按回车）：')

            config['anime'].insert(anime_num, {'name': anime_name, 'url': anime_url})
            save_config(config)

        elif mods == '-h':  # 无输出模式
            anime_num = int(cmd[2])
            anime_name = cmd[3]
            anime_url = cmd[4]
            if anime_num == '':
                print('[Error]: 番剧序号不能为空！')
                raise Exception('[Error]: 番剧序号不能为空！')
            if anime_name == '':
                print('[Error]: 番剧昵称不能为空！')
                raise Exception('[Error]: 番剧昵称不能为空！')
            if anime_url == '*':
                anime_url = ''

            config['anime'].insert(anime_num, {'name': anime_name, 'url': anime_url})
            save_config(config)

        elif mods == '-b':  # 批量添加模式
            return_words = ''
            anime_num = int(input('请输入插入在哪个序号之后：'))
            if anime_num == '':
                print('[Error]: 番剧序号不能为空！')
                raise Exception('[Error]: 番剧序号不能为空！')
            print('请输入番剧昵称和对应网址（若要停止输入则多输入一段空行，若没有网址则输入*，昵称与网址不能有空格）：')

            while True:
                try:
                    words = input().split()
                    anime_name = words[0]
                    anime_url = words[1]

                    if anime_url == '*':
                        anime_url = ''
                    return_words += f'{anime_name} {anime_url}\n'
                    config['anime'].insert(anime_num, {'name': anime_name, 'url': anime_url})
                    anime_num += 1

                    save_config(config)
                except:
                    break

            return return_words

        elif mods == '-bh' or mods == '-hb':  # 无输出批量添加模式
            # 若要停止输入则多输入一段空行，若没有网址则输入*，名称与网址不能有空格
            return_words = ''
            anime_num = int(cmd[2])
            words = copy.copy(cmd)
            del words[2]
            del words[1]
            del words[0]
            loop_num = len(words) / 2
            if (int(loop_num) * 10) != int(loop_num * 10):
                print('[Error]: 请输入正确的数据数量!')
                raise Exception('[Error]: 请输入正确的数据数量!')
            num = 0
            for i in range(int(loop_num)):
                anime_name = words[num]
                num += 1
                anime_url = words[num]
                num += 1
                if anime_url == '*':
                    anime_url = ''

                config['anime'].insert(anime_num, {'name': anime_name, 'url': anime_url})
                anime_num += 1
                return_words += f'{anime_name} {anime_url}\n'

            save_config(config)
            return return_words

        elif mods == '-?':
            print('''
    插入番剧信息到番剧列表某项之后。
    注：ins 可以写成  insert
    
    
    无参数 / -normal   根据提示语插入番剧信息。
    
    -h                没有提示语，直接插入番剧信息。
        用法： ins -h <番剧序号> <番剧昵称> <番剧网址>
        
    -b                批量插入番剧信息，有提示语。
    
    -bh / -hb         批量插入番剧信息，无提示语，直接插入。
        注：若要停止输入则多输入一段空行，若没有网址则输入*，名称与网址不能有空格。
        用法： ins {-bh | -hb} <番剧序号> <番剧昵称> <番剧网址>...... 
                    ''')

        else:
            print('[Error]: 没有此参数!')


A = AnimeManager()


# --------------------------------------------------------------------------------


def is_animeList_empty():
    if len(config['anime']) == 0:
        return True
    else:
        return False


def save_config(config):
    json.dump(config, open(config_path, 'w+'))


def get_cmd():
    while True:
        command = input(cmd_prompt)
        if command == '':
            continue

        cmd = command.split()
        try:
            tmp = cmd[1]
        except:
            cmd.append('-normal')

        return cmd


def init():
    global config

    try:
        config = json.load(open(config_path, 'r'))
    except:
        config = {'anime': []}
        save_config(config)


def main():
    # init
    init()
    print(welcome_content)
    # main
    program_flag = True
    while program_flag:
        cmd = get_cmd()

        try:
            match cmd[0]:
                case 'exit':
                    program_flag = False

                case 'help':
                    A.a_help(cmd)

                case 'list':
                    A.a_list(cmd)
                case 'ls':
                    A.a_list(cmd)

                case 'add':
                    A.a_add(cmd)

                case 'del':
                    A.a_del(cmd)

                case 'edit':
                    A.a_edit(cmd)

                case 'ins':
                    A.a_ins(cmd)
                case 'insert':
                    A.a_ins(cmd)

                case default:
                    print('[Error]: 没有此命令!')
        except:
            print('[Error]: 错误!')

    print(exit_content)


if __name__ == '__main__':
    main()
