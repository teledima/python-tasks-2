import requests
from cmd import Cmd


class MyCmd(Cmd):
    intro = 'help - справка по командам\nexit - выход'
    _server = 'http://127.0.0.1:8080'
    _current_user = None

    def do_help(self, arg):
        content = requests.get(f'{self._server}/help').text
        print(content)

    def do_auth(self, arg):
        args = arg.split(' ')
        assert len(args) == 2
        response = requests.post(f'{self._server}/auth', json={'user': args[0], 'pass': args[1]})
        if response.ok:
            self._current_user = args[0]

    def do_list(self, _):
        if self._current_user:
            response = requests.get(f'{self._server}/list', json={'user': self._current_user})
            if response.status_code == 200:
                print(response.text)
        else:
            print('Вы не авторизованы')

    def do_info(self, arg):
        if self._current_user:
            response = requests.get(f'{self._server}/info/{arg}', json={'user': self._current_user})
            if response.status_code == 200:
                print(response.text)
            elif response.status_code == 404:
                print(f'Файл "{arg}" не найден')
        else:
            print('Вы не авторизованы')

    def do_retr(self, arg):
        if self._current_user:
            for file in arg.split(' '):
                response = requests.get(f'{self._server}/retr/{file}', json={'user': self._current_user})
                if response.status_code == 200:
                    with open(file, 'wb') as out_file:
                        out_file.write(response.content)
                        print(f'"{file}": Файл получен')
                elif response.status_code == 404:
                    print(f'(Error) "{file}": файл не найден')
        else:
            print('Вы не авторизованы')

    def do_exit(self, arg):
        if self._current_user:
            requests.post(f'{self._server}/exit', json={'user': self._current_user})
        return True


if __name__ == "__main__":
    MyCmd().cmdloop()