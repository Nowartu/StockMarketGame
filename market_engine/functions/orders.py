from database.models import Order, Company
from database.session import get_db
from sqlalchemy import select, and_, func, case

def check_if_available(db):
    orders = select(
        Order.company_id,
        func.sum(case((Order.type == 'BUY', 1), else_=0)),
        func.sum(case((Order.type == 'SELL', 1), else_=0))
    ).where(and_(
        Order.done == False,
        Order.canceled == False,
    ))

    return db.execute(orders).scalars().all()


def match_orders(db, company_id):
    orders_buy = db.execute(select(Order).where(and_(
        Order.done == False,
        Order.canceled == False,
        Order.type == 'BUY',
        Order.company_id == company_id
    )).order_by(Order.price.desc())).scalars().all()
    orders_sell = db.execute(select(Order).where(and_(
        Order.done == False,
        Order.canceled == False,
        Order.type == 'SELL',
        Order.company_id == company_id
    )).order_by(Order.price.asc())).scalars().all()

    for order_buy in orders_buy:
        for order_sell in orders_sell:
            if order_buy.user_id != order_sell.user_id:
                if order_buy.price >= order_sell.price:
                    return [order_buy.id, order_sell.id]
    else:
        return None, None