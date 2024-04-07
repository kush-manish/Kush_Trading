from pydantic import BaseModel


class OrderData(BaseModel):
    data: dict
    type: str
    # Add other fields as necessary


class order_with_price:
    # constructor
    def __init__(self, data, price):
        self.data = data
        self.price = price

        # function for customized printing

    def __lt__(self, order):
        return self.price < order.price
