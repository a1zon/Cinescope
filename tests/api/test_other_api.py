import pytest
from requests import Session

from models.db_models.accounts_transaction_model import AccountTransactionTemplate
from utils.data_generator import DataGenerator


class TestTransactionApi:
    def test_accounts_transaction_template(self, db_session: Session):
        # Создаем новые записи в базе данных (чтоб точно быть уверенными что в базе присутствуют данные для тестирования)

        stan = AccountTransactionTemplate(user=f"Stan_{DataGenerator.generate_random_int_variable(10)}", balance=1000)
        bob = AccountTransactionTemplate(user=f"Bob_{DataGenerator.generate_random_int_variable(10)}", balance=500)

        # Добавляем записи в сессию, да сук почему он ругается на методы сессии!!!
        db_session.add_all([stan, bob])
        # Фиксируем изменения в базе данных
        db_session.commit()

        def transfer_money(session, from_account, to_account, amount):
            # пример функции выполняющей транзакцию
            # представим что она написана на стороне тестируемого сервиса
            # и вызывая метод transfer_money, мы какбудтобы делем запрос в api_manager.movies_api.transfer_money
            """
            Переводит деньги с одного счета на другой.
            :param session: Сессия SQLAlchemy.
            :param from_account_id: ID счета, с которого списываются деньги.
            :param to_account_id: ID счета, на который зачисляются деньги.
            :param amount: Сумма перевода.
            """
            # Получаем счета
            from_account = session.query(AccountTransactionTemplate).filter_by(user=from_account).one()
            to_account = session.query(AccountTransactionTemplate).filter_by(user=to_account).one()

            # Проверяем, что на счете достаточно средств
            if from_account.balance < amount:
                raise ValueError("Недостаточно средств на счете")

            # Выполняем перевод
            from_account.balance -= amount
            to_account.balance += amount

            # Сохраняем изменения
            session.commit()

        # Проверяем начальные балансы
        assert stan.balance == 1000
        assert bob.balance == 500

        try:
            # Выполняем перевод 200 единиц от stan к bob
            transfer_money(db_session, from_account=stan.user, to_account=bob.user, amount=200)

            # Проверяем, что балансы изменились
            assert stan.balance == 800
            assert bob.balance == 700

        except Exception as e:
            # Если произошла ошибка, откатываем транзакцию
            db_session.rollback()  # откат всех введеных нами изменений
            pytest.fail(f"Ошибка при переводе денег: {e}")

        finally:
            # Удаляем данные для тестирования из базы
            db_session.delete(stan)
            db_session.delete(bob)
            # Фиксируем изменения в базе данных
            db_session.commit()

    def test_accounts_transaction_template_insufficient_funds(self, db_session: Session):
        """
        Проверка сценария, когда у Стена недостаточно средств для перевода Бобу.
        После попытки перевода баланс в базе не должен измениться.
        p.s Дядя Стен опять хочет нагреть Гидеона на кеш
        """

        stan = AccountTransactionTemplate(
            user=f"Stan_{DataGenerator.generate_random_int_variable(10)}", balance=100
        )  # меньше чем хотим перевести
        bob = AccountTransactionTemplate(
            user=f"Bob_{DataGenerator.generate_random_int_variable(10)}", balance=500
        )

        db_session.add_all([stan, bob])
        db_session.commit()

        #  функция перевода денег
        def transfer_money(session: Session, from_account_name: str, to_account_name: str, amount: int):
            from_account = session.query(AccountTransactionTemplate).filter_by(user=from_account_name).one()
            to_account = session.query(AccountTransactionTemplate).filter_by(user=to_account_name).one()

            if from_account.balance < amount:
                raise ValueError("Недостаточно средств на счете")

            from_account.balance -= amount
            to_account.balance += amount
            session.commit()

        # Проверяем начальные балансы
        initial_stan_balance = stan.balance
        initial_bob_balance = bob.balance

        with pytest.raises(ValueError, match="Недостаточно средств на счете"):
            transfer_money(db_session, from_account_name=stan.user, to_account_name=bob.user, amount=200)

        # Проверяем, что балансы не изменились
        db_session.refresh(stan)
        db_session.refresh(bob)
        assert stan.balance == initial_stan_balance, "Баланс Стена изменился после неудачного перевода"
        assert bob.balance == initial_bob_balance, "Баланс Боба изменился после неудачного перевода"

        # Очистка базы
        db_session.delete(stan)
        db_session.delete(bob)
        db_session.commit()
