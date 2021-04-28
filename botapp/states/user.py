from aiogram.dispatcher.filters.state import StatesGroup, State


class User(StatesGroup):
    main = State()

    class GetWallet(StatesGroup):
        wallet = State()
        name = State()

    min_amount = State()
