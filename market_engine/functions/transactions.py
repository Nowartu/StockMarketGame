import datetime
from sqlalchemy import select, and_
from database.models import Order, Transaction, UserStock, UserProfile, Event

def make_transaction(db, order1, order2):
    events = []

    order_buy = db.execute(select(Order).where(Order.id == order1).with_for_update()).scalar_one_or_none()
    order_sell = db.execute(select(Order).where(Order.id == order2).with_for_update()).scalar_one_or_none()

    user_buy = db.execute(select(UserProfile).where(UserProfile.id == order_buy.user_id).with_for_update()).scalar_one_or_none()
    user_sell = db.execute(select(UserProfile).where(UserProfile.id == order_sell.user_id).with_for_update()).scalar_one_or_none()

    user_buy_stock = db.execute(select(UserStock).where(and_(
        UserStock.user_id == order_buy.user_id,
        UserStock.company_id == order_buy.company_id
    )).with_for_update()).scalar_one_or_none()

    user_sell_stock = db.execute(select(UserStock).where(and_(
        UserStock.user_id == order_sell.user_id,
        UserStock.company_id == order_sell.company_id
    )).with_for_update()).scalar_one_or_none()

    amount = min(order_buy.available, order_sell.available)
    price = (order_buy.price + order_sell.price) / 2

    events.append(update_order(order_buy, amount))
    events.append(update_order(order_sell, amount))

    events.append(update_user_profile(user_buy, order_buy.price, order_sell.price, amount, True))
    events.append(update_user_profile(user_sell, order_buy.price, order_sell.price, amount, False))

    us, e = update_user_stock(user_buy_stock, user_buy.id, order_buy.company_id, amount, True)
    events.append(e)
    _, e = update_user_stock(user_sell_stock, user_sell.id, order_sell.company_id, amount, False)
    events.append(e)

    if us is not None:
        db.add(us)

    t = add_transaction(order_buy, order_sell, amount, price)
    db.add(t)

    db.commit()

    events.append(Event(
        type="NEW TRANSACTION",
        source="TRANSACTION",
        reference_id=t.id,
        payload={}
    ))

    for event in events:
        db.add(event)

    db.commit()


def update_user_profile(user_profile, buy_price, sell_price, amount, buy):
    if buy:
        user_profile.balance -= (buy_price + sell_price) / 2 * amount
        user_profile.blocked_balance -= buy_price * amount
        return Event(
            type="TRANSACTION",
            source="USER",
            reference_id=user_profile.id,
            payload={
                "status": "Money taken from user account",
                "amount": float((buy_price + sell_price) / 2 * amount)
            }
        )
    else:
        user_profile.balance += (buy_price + sell_price) / 2 * amount
        return Event(
            type="TRANSACTION",
            source="USER",
            reference_id=user_profile.id,
            payload={
                "status": "Money added to user account",
                "amount": float((buy_price + sell_price) / 2 * amount)
            }
        )


def update_user_stock(user_stock, user_id, company, amount, buy):
    if buy:
        e = Event(
            type="TRANSACTION",
            source="USER",
            reference_id=user_id,
            payload={
                "status": "Stock added to user account",
                "company": company,
                "amount": amount
            }
        )
        if user_stock is not None:
            user_stock.amount += amount
            return None, e
        else:
            us = UserStock(
                amount=amount,
                company_id=company,
                user_id=user_id,
                blocked=0
            )

            return us, e
    else:
        user_stock.blocked -= amount
        user_stock.amount -= amount
        e = Event(
                type="TRANSACTION",
                source="USER",
                reference_id=user_id,
                payload={
                    "status": "Stock taken from user account",
                    "company": company,
                    "amount": amount
                }
            )
    return None, e


def update_order(order, amount):
    order.available -= amount
    if order.available == 0:
        order.done = True

        e = Event(
            type="TRANSACTION",
            source="ORDER",
            reference_id=order.id,
            payload={
                "status": "ORDER COMPLETED"
            }
        )
    else:
        e = Event(
            type="TRANSACTION",
            source="ORDER",
            reference_id=order.id,
            payload={
                "status": "ORDER PARTIALLY COMPLETED",
                "available": order.available
            }
        )

    return e


def add_transaction(order_buy, order_sell, amount, price):
    t = Transaction(
        order_1_id=order_buy.id,
        order_2_id=order_sell.id,
        amount=amount,
        price=price,
        executed_at=datetime.datetime.now()
    )

    return t