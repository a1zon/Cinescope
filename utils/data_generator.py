import  random
import  string
from faker import Faker
from uuid import uuid4
import datetime

faker = Faker()

class DataGenerator:

    @staticmethod
    def generate_random_email():
        random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        return f"kek{random_string}@gmail.com"

    @staticmethod
    def generate_random_name():
        return f"{faker.first_name()} {faker.last_name()}"

    @staticmethod
    def generate_random_password():

        letters = random.choice(string.ascii_letters)
        digits = random.choice(string.digits)

        special_chars = "?@#$%^&*|:"
        all_chars = special_chars + string.digits + string.ascii_letters
        remaining_length = random.randint(6,18)
        remaining_chars  = ''.join(random.choices(all_chars,k = remaining_length))

        password = list(letters + digits + remaining_chars)
        random.shuffle(password)

        return ''.join(password)

    @staticmethod
    def generate_random_movie_name():
        """
        Генерирует более «кинематографичное» название фильма.
        Использует комбинацию слов, catch_phrase и эпитетов - зачем я так запарился хз
        """


        main_title = faker.catch_phrase()


        prefixes = ["The Last", "Shadows of", "Rise of", "Return of", "Chronicles of", "Whispers in"]
        prefix = random.choice(prefixes) if random.random() < 0.6 else ""


        suffixes = [": A Tale", ": The Final Chapter", ": Reborn", ": Origins", ": Awakening"]
        suffix = random.choice(suffixes) if random.random() < 0.5 else ""


        title = f"{prefix} {main_title}{suffix}".strip()

        title = " ".join(title.split())

        return title


    @staticmethod
    def generate_random_int():
        random_int = random.randint(1, 10_000)
        return random_int

    @staticmethod
    def generate_random_int_variable(char: int):
        random_int = random.randint(1, char)
        return random_int


    @staticmethod
    def generate_random_sentence():
        random_sentence = faker.sentence(nb_words=6)
        return  random_sentence

    @staticmethod
    def generate_user_data() -> dict:
        """Генерирует данные для тестового пользователя"""
        from uuid import uuid4

        return {
            'id': f'{uuid4()}',  # генерируем UUID как строку
            'email': DataGenerator.generate_random_email(),
            'full_name': DataGenerator.generate_random_name(),
            'password': DataGenerator.generate_random_password(),
            'created_at': datetime.datetime.now(),
            'updated_at': datetime.datetime.now(),
            'verified': False,
            'banned': False,
            'roles': '{USER}'
        }