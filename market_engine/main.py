from database.session import get_db
from database.redis_connection import get_connection
from functions.orders import match_orders, check_if_available
from functions.transactions import make_transaction


def main():

    price_change_pub = get_connection()
    new_order = get_connection()
    new_order_sub = new_order.pubsub()
    new_order_sub.subscribe("new_order")

    for message in new_order_sub.listen():
        print(f"message received ({message})")
        with get_db() as db:
            if check_if_available(db):
                order_1, order_2 = match_orders(db, 1)
                while order_1 is not None and order_2 is not None:

                    make_transaction(db, order_1, order_2, price_change_pub)
                    order_1, order_2 = match_orders(db, 1)

                    if order_1 is None or order_2 is None:
                        break




if __name__ == "__main__":
    main()
