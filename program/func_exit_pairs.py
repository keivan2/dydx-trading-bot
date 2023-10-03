from constants import CLOSE_AT_ZSCORE_CROSS
from func_utils import format_number
from func_public import get_candles_recent
from func_cointegration import calculate_zscore
from func_private import place_market_order
import json
import time

from pprint import pprint


# Close positions
def manage_trade_exits(client):

    """
        Manage exiting open positions
        Based upon criteria set in constants
    """

    # Initialize saving output
    save_output = []

    # Opening JSON file
    try:
        open_positions_file = open("bot_agents.json")
        open_positions_dict = json.load(open_positions_file)

    except:
        return "complete"
    
    # Guard: Exit if no open positions in file
    if len(open_positions_dict) < 1:
        return "complete"
    
    # Get all open positions per tarding platform
    exchange_pos = client.private.get_positions(status="OPEN")
    all_exc_pos = exchange_pos.data["positions"]
    markets_live = []
    for p in all_exc_pos:
        markets_live.append(p["market"])

    # Protect API
    time.sleep(1)

    # Check all saved postions match order record
    # Exit trade according t oan exit tarde rules
    for position in open_positions_dict:
        
        # Initilize is_close trigger
        is_close = False

        # Extract position matching information from file - market 1
        position_market_m1 = position["market_1"]
        position_size_m1 = position["oder_m1_size"]
        position_side_m1 = position["order_m1_side"]

        # Extract position matching information from file - market 1
        position_market_m2 = position["market_2"]
        position_size_m2 = position["oder_m2_size"]
        position_side_m2 = position["order_m2_side"]


        # Protect API
        time.sleep(0.5)

        # Get order info m1 per exchange
        order_m1 = client.private.get_order_by_id(position["order_id_m1"])
        order_market_m1 = order_m1.data["order"]["market"]
        order_size_m1 = order_m1.data["order"]["size"]
        order_side_m1 = order_m1.data["order"]["side"]


        # Protect API
        time.sleep(0.5)

        # Get order info m2 per exchange
        order_m2 = client.private.get_order_by_id(position["order_id_m2"])
        order_market_m2 = order_m2.data["order"]["market"]
        order_size_m2 = order_m2.data["order"]["size"]
        order_side_m2 = order_m2.data["order"]["side"]


        # Perform matching checks
        check_m1 = position_market_m1 == order_market_m1 and position_size_m1 == order_size_m1 and position_side_m1 == order_side_m1
        check_m2 = position_market_m2 == order_market_m2 and position_size_m2 == order_size_m2 and position_side_m2 == order_side_m2
        check_live = position_market_m1 in markets_live and position_market_m2 in markets_live

        # Gurad: If not all match exit with error
        if not check_m1 or not check_m2 or not check_live:
            print(f"Warning: Not all open positions match exchange records for {position_market_m1} and {position_market_m2}")
            continue


        # Get prices
        series_1 = get_candles_recent(client, position_market_m1)
        time.sleep(0.2)
        series_2 = get_candles_recent(client, position_market_m2)
        time.sleep(0.2)

        # Get Market for reference of tick size
        markets = client.public.get_markets().data

        # protect API
        time.sleep(0.2)

        # trigger close based on Z-score
        if CLOSE_AT_ZSCORE_CROSS:
            continue