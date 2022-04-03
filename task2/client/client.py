import requests
import sys
from cmd import Cmd
from msvcrt import getch, putch


class MyCmd(Cmd):
    intro = 'help - справка по командам\nexit - выход'
    _server = 'http://127.0.0.1:8080'
    _current_user = None

    def do_help(self, arg):
        content = requests.get(f'{self._server}/help').text
        print(content)

    def do_auth(self, arg):
        args = arg.split(' ')
        try:
            assert len(args) == 2
            response = requests.post(f'{self._server}/auth', json={'user': args[0], 'pass': args[1]})
            if response.ok:
                self._current_user = args[0]
        except AssertionError:
            print(f'Неверное число аргументов. Введено: {len(args)}, Необходимо: 2')

    def do_list(self, _):
        if self._current_user:
            response = requests.get(f'{self._server}/list', json={'user': self._current_user})
            if response.status_code == 200:
                print(response.text)
        else:
            print('Вы не авторизованы')

    def do_read(self, arg):
        if self._current_user:
            response = requests.get(f'{self._server}/read/{arg}', json={'user': self._current_user})
            if response.status_code == 200:
                print(response.text)
        else:
            print('Вы не авторизованы')

    def do_send(self, _):
        if self._current_user:
            message = input("Введите сообщение, ввод заканчивается точкой\n").split('.')[0]
            response = requests.get(f'{self._server}/send', json={'user': self._current_user, "message": message})
            if response.status_code == 200:
                print('Сообщение доставлено')
        else:
            print('Вы не авторизованы')

    def do_exit(self, _):
        if self._current_user:
            requests.post(f'{self._server}/exit', json={'user': self._current_user})
        return True


if __name__ == "__main__":
    MyCmd().cmdloop()
