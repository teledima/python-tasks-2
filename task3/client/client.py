import requests
from cmd import Cmd


class MyCmd(Cmd):
    _server = 'http://127.0.0.1:8080'
    _current_user = None

    def do_login(self, arg):
        args = arg.split(' ')
        try:
            assert len(args) == 2
        except AssertionError:
            print('LOGIN: 3; ERROR - Неверное число аргументов')
            return
        response = requests.post(f'{self._server}/login', json={'user': args[0], 'pass': args[1]})
        if response.ok:
            self._current_user = args[0]
            print('LOGIN: 0')
        else:
            print('LOGIN: 1; ERROR - ошибка авторизации')

    def do_store(self, arg):
        if self._current_user:
            coefficients = list(map(float, arg.split(' ')))
            response = requests.put(f'{self._server}/store', json={'user': self._current_user, 'coefficients': coefficients})
            if response.status_code == 204:
                print('STORE: 0')
            else:
                if response.json().get('error') == 'incorrect_coeff':
                    print('STORE: 2; ERROR - неверное число коэффициентов')
                else:
                    print(f'STORE: 3; ERROR - {response.json()["error"]}')
        else:
            print('STORE: 1; ERROR - Вы не авторизованы')

    def do_solve(self, arg):
        if self._current_user:
            try:
                if arg:
                    coefficients = list(map(float, arg.split(' ')))
                else:
                    coefficients = []
            except ValueError:
                print('SOLVE: 3; ERROR - некорректные коэффициенты')
                return
            response = requests.get(f'{self._server}/solve', json={'user': self._current_user, 'coefficients': coefficients})
            if response.status_code == 200:
                print(f'SOLVE: 0; RESULT: {response.json()["result"]}')
            else:
                if response.json().get('error') == 'incorrect_coeff':
                    print('SOLVE: 2; ERROR - неверное число коэффициентов')
                else:
                    print(f'SOLVE: 3; ERROR - {response.json()["error"]}')
        else:
            print('SOLVE: 1; ERROR: Вы не авторизованы')

    def do_exit(self, _):
        if self._current_user:
            requests.post(f'{self._server}/exit', json={'user': self._current_user})
        return True


if __name__ == "__main__":
    MyCmd().cmdloop()
