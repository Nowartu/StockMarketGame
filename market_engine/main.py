from database.models import *
from database.session import get_db
from sqlalchemy import select, and_, func, case
from functions.orders import match_orders
from functions.transactions import make_transaction

with get_db() as db:
    order_1, order_2 = match_orders(db, 1)
    make_transaction(db, order_1, order_2)