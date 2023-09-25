from constants import RESOLUTION
from func_utils import get_ISO_Times
import pandas as pd
import numpy as np
import time
from pprint import pprint

# Get relevant time period from ISO from and to
ISO_TIMES = get_ISO_Times()

pprint(ISO_TIMES)

# Construct market prices

def construct_market_prices(client):
    pass