import time

class User:
    # Каждый объект класса User должен обладать следующими атрибутами и методами:
    # Атрибуты: nickname(имя пользователя, строка), password(в хэшированном виде, число), age(возраст, число)
    def __init__(self, nickname, password, age):
        self.nickname = nickname
        self.password = hash(password)
        self.age = age

    def __str__(self):
        return self.nickname


class Video:
    # Каждый объект класса Video должен обладать следующими атрибутами и методами:
    # Атрибуты: title(заголовок, строка), duration(продолжительность, секунды),
    # time_now(секунда остановки (изначально 0)), adult_mode(ограничение по возрасту, bool (False по умолчанию))
    def __init__(self, title, duration, adult_mode=False):
        self.title = title
        self.duration = duration
        self.time_now = 0
        self.adult_mode = adult_mode


class UrTube:
    # Каждый объект класса UrTube должен обладать следующими атрибутами и методами:
    # Атрибуты: users(список объектов User), videos(список объектов Video), current_user(текущий пользователь, User)
    def __init__(self):
        self.users = []
        self.videos = []
        self.current_user = None

    def __contains__(self, item):
        _title = item.title.lower()
        for video in self.videos:
            if video.title.lower() == item:
                return True
        return False

    # Метод log_in, который принимает на вход аргументы: nickname, password и пытается найти пользователя
    # в users с такими же логином и паролем. Если такой пользователь существует, то current_user меняется на найденного.
    # Помните, что password передаётся в виде строки, а сравнивается по хэшу.
    def log_in(self, nickname, password):
        hashpass = hash(password)
        for user in self.users:
            if user.nickname == nickname and user.password == hashpass:
                self.current_user = user
                break

    # Метод register, который принимает три аргумента: nickname, password, age, и добавляет пользователя в список,
    # если пользователя не существует (с таким же nickname). Если существует, выводит на экран:
    # "Пользователь {nickname} уже существует". После регистрации, вход выполняется автоматически.
    def register(self, nickname, password, age):
        for user in self.users:
            if user.nickname == nickname:
                print(f"Пользователь {nickname} уже существует")
                return
        new_user = User(nickname, password, age)
        self.users.append(new_user)
        self.current_user = new_user

    # Метод log_out для сброса текущего пользователя на None.
    def log_out(self):
        self.current_user = None

    # Метод add, который принимает неограниченное кол-во объектов класса Video и все добавляет в videos,
    # если с таким же названием видео ещё не существует. В противном случае ничего не происходит.
    def add(self, *new_videos):
        for new_video in new_videos:
            if not self.__contains__(new_video):
                self.videos.append(new_video)

    # Метод get_videos, который принимает поисковое слово и возвращает список названий всех видео,
    # содержащих поисковое слово. Следует учесть, что слово 'UrbaN' присутствует в строке 'Urban the best'
    # (не учитывать регистр).
    def get_videos(self, word):
        _word = word.lower()
        titles = []
        for video in self.videos:
            _title = video.title.lower()
            if _title.__contains__(_word):
                titles.append(video.title)
        return titles


    # Метод watch_video, который принимает название фильма, если не находит точного совпадения(вплоть до пробела),
    # то ничего не воспроизводится, если же находит - ведётся отчёт в консоль на какой секунде ведётся просмотр.
    # После текущее время просмотра данного видео сбрасывается.
    def watch_video(self, title):

        if self.current_user == None:
            print("Войдите в аккаунт, чтобы смотреть видео")
            return
        _title = title.lower()

        current_video = None
        for video in self.videos:
            if video.title.lower() == _title:
                current_video = video
                break

        if current_video == None:
            return

        if current_video.adult_mode and self.current_user.age < 18:
            print("Вам нет 18 лет, пожалуйста покиньте страницу")
            return

        for sec in range(current_video.duration):
            time.sleep(1)
            current_video.time_now += 1
            print(current_video.time_now)

        current_video.time_now = 0
        print("Конец видео")


# ===== Код для проверки: ========================================

ur = UrTube()
v1 = Video('Лучший язык программирования 2024 года', 200)
v2 = Video('Для чего девушкам парень программист?', 10, adult_mode=True)

# Добавление видео
ur.add(v1, v2)

# Проверка поиска
print(ur.get_videos('лучший'))
print(ur.get_videos('ПРОГ'))

# Проверка на вход пользователя и возрастное ограничение
ur.watch_video('Для чего девушкам парень программист?')
ur.register('vasya_pupkin', 'lolkekcheburek', 13)
ur.watch_video('Для чего девушкам парень программист?')
ur.register('urban_pythonist', 'iScX4vIJClb9YQavjAgF', 25)
ur.watch_video('Для чего девушкам парень программист?')

# Проверка входа в другой аккаунт
ur.register('vasya_pupkin', 'F8098FM8fjm9jmi', 55)
print(ur.current_user)

# Попытка воспроизведения несуществующего видео
ur.watch_video('Лучший язык программирования 2024 года!')
