

import uuid
from datetime import datetime
import httpx
from fastapi import FastAPI
from .models import OrderData, order_with_price
import heapq

from .database import sell_orders,buy_orders

# Min heap for buy orders and max heap for sell orders



async def push_message_to_oms_and_mds(data: dict):
    # URL of the tes service endpoint
    oms_service_url = "http://oms:8000/kafka/kafka-trade-done"
    async with httpx.AsyncClient() as client:
        response = await client.post(oms_service_url, json=data)

    mds_service_url = "http://mds:8002/kafka/kafka-order-trade-happened"
    async with httpx.AsyncClient() as client:
        response = await client.post(mds_service_url, json=data)


async def match_order(order):
    # Generate a unique identifier for this order operation


    message = {}
    if order["is_active"]:
        if order["side"] == 1:
            # For buy orders, check if there's a matching sell order
            while sell_orders and order["quantity"] > 0:
                best_sell = heapq.heappop(sell_orders)
                if order["price"] >= best_sell.price:
                    # Execute trade
                    traded_quantity = min(order["quantity"], best_sell.data["quantity"])
                    order["quantity"] -= traded_quantity
                    best_sell.data["quantity"] -= traded_quantity

                    # Update message with traded orders
                    message[str(uuid.uuid4())] = {
                        "bid_order":order,
                        "ask_order":best_sell.data,
                        "timestamp":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "price": order["price"], # this amount need to be pay
                        "trade_quantity": traded_quantity
                    }

                    if best_sell.data["quantity"] > 0:
                        heapq.heappush(sell_orders, best_sell)

                else:
                    heapq.heappush(sell_orders, best_sell)
                    break

            if order["quantity"] > 0:
                heapq.heappush(buy_orders, order_with_price(order, -order["price"]))  # Use negative price for max heap

        elif order["side"] == -1:
            # For sell orders, check against buy orders

            while buy_orders and order["quantity"] > 0:

                best_buy = heapq.heappop(buy_orders)

                if order["price"] <= best_buy.data['price']:
                    # Execute trade
                    traded_quantity = min(order["quantity"], best_buy.data["quantity"])
                    order["quantity"] -= traded_quantity
                    best_buy.data["quantity"] -= traded_quantity

                    # Update message with traded orders
                    message[str(uuid.uuid4())] = {
                        "bid_order": best_buy.data,
                        "ask_order": order,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "price": order["price"], # this amount need to be pay
                        "trade_quantity": traded_quantity
                    }

                    if best_buy.data["quantity"] > 0:
                        heapq.heappush(buy_orders, best_buy)

                else:
                    heapq.heappush(buy_orders, best_buy)
                    break

            if order["quantity"] > 0:
                heapq.heappush(sell_orders, order_with_price(order, order["price"]))

    if message:
        await push_message_to_oms_and_mds(message)



import heapq
from typing import List, Tuple, Optional

def delete_order(order: dict, ) -> Optional[dict]:
    order_id = order['order_id']
    orders_heap = buy_orders if order['side'] == 1 else sell_orders

    # Find the index of the order in the heap
    order_index = None
    for i, order in enumerate(orders_heap):
        if order.data["order_id"] == order_id:
            order_index = i
            break

    if order_index is None:
        print(f"Order with ID {order_id} not found.")
        return None

    # Retrieve the order to delete
    order_to_delete = orders_heap[order_index]

    # Remove the order from the heap
    del orders_heap[order_index]
    heapq.heapify(orders_heap)  # Re-heapify the list to maintain the heap property

    print(f"Order with ID {order_id} deleted.")
    return order_to_delete.data

