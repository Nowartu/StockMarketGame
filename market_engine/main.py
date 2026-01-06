from database.session import get_db
from functions.orders import match_orders
from functions.transactions import make_transaction
import redis

r = redis.Redis(
    host="localhost",
    port=6379,
    db=0,
    password="smg"
)
p = r.pubsub()
p.subscribe('new_order')
print("Listening for messages")
for message in p.listen():
    print(f"message received ({message})")
    with get_db() as db:
        order_1, order_2 = match_orders(db, 1)
        if order_1 is not None and order_2 is not None:
            make_transaction(db, order_1, order_2)