import  random
import  string
from faker import Faker
from uuid import uuid4

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
    def generate_random_movie():
        random_movie = faker.catch_phrase(),
        return str(random_movie)

    @staticmethod
    def generate_random_int():
        random_int = random.randint(1, 10_000)
        return random_int

    @staticmethod
    def generate_random_sentence():
        random_sentence = faker.sentence(nb_words=6)
        return  random_sentence