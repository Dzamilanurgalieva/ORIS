class Playlist:
    def __init__(self):
        self.song = []

    def add_song(self, name, duration):
        if not isinstance(name, str):
            print("Ошибка! Ожидается строка для названия.")
            return

        name = name.strip()
        if name == "":
            print("Ошибка! Название не должно быть пустым.")
            return

        if not isinstance(duration, (int, float)):
            print("Ошибка! Ожидается число для длительности")
            return

        if duration <= 0:
            print("Ошибка! Длительность песни должна быть больше нуля")
            return

        song = {
            "name": name,
            "duration": duration
        }
        self.song.append(song)
        print(f"Песня '{name}' добавлена")

    def remove_song(self, name):
        if not isinstance(name, str):
            print("Ошибка! Ожидается строка для названия.")
            return

        name = name.strip()
        for song in self.song:
            if song["name"] == name:
                self.song.remove(song)
                print(f"Песня '{name}' удалена")
                return

        print(f"Песня '{name}' не найдена")

    def total_duration(self):
        total = 0
        for song in self.song:
            total += song["duration"]
        return total

    def __len__(self):
        return len(self.song)

    def show(self):
        if len(self.song) == 0:
            print("Плейлист пуст")
            return

        print("Песни в плейлисте:")
        for index, song in enumerate(self.song, start=1):
            print(f"{index}. {song['name']} — {song['duration']} сек.")


if __name__ == "__main__":
    playlist = Playlist()

    #ПРОВЕРКА
    print("1. Пустой плейлист")
    print("Количество песен:", len(playlist))
    print("Общая длительность:", playlist.total_duration())
    playlist.show()
    print()

    print("2. Добавляем несколько песен")
    playlist.add_song("Bohemian Rhapsody", 354)
    playlist.add_song("Song 1", 200)
    playlist.add_song("Song 2", 300)

    print("Количество песен:", len(playlist))
    print("Общая длительность:", playlist.total_duration())
    playlist.show()
    print()

    print("3. Удаляем существующую песню")
    playlist.remove_song("Song 1")

    print("Количество песен:", len(playlist))
    print("Общая длительность:", playlist.total_duration())
    playlist.show()
    print()

    print("4. Пробуем удалить несуществующую песню")
    playlist.remove_song("Какая-то песня")
    print("Количество песен:", len(playlist))
    print()

    print("5. Пробуем добавить неправильные данные")
    playlist.add_song("Плохая", "две минуты")
    playlist.add_song(12345, 100)
    playlist.add_song("Ноль", 0)

    print("Количество песен не изменилось:", len(playlist))