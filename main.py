from brownie import Contract, network
from csv import DictWriter
from constants import v2_pool_contracts as V2_ADDRESSES
import os
import datetime
import pandas as pd

def add_header(csv, header):
    df = pd.read_csv(csv, header=None)
    df.columns = header
    df.to_csv(csv, index=False) 

def get_stats(address):
    contract = Contract.from_explorer(address)
    return {
        # POOL PARAMETERS
        # FEE METRICS
        "fee_pct": contract.fee() / 1e8,
        "mid_fee_pct": contract.mid_fee() / 1e8,
        "out_fee_pct": contract.out_fee() / 1e8,
        "admin_fee_pct": contract.admin_fee() / 1e8,
        "fee_gamma_unscaled": contract.fee_gamma() / 1e18,
        # "ma_half_time": contract.ma_half_time(),
        # "adjustment_step": contract.adjustment_step(),
        # "allowed_extra_profit": contract.allowed_extra_profit(),
        # "gamma": contract.gamma(),

        # CONTRACT PARAMETERS
        # "D_unscaled": contract.D() / 1e18,
        # "A": contract.A(),
        # "xcp_profit": contract.xcp_profit(),
        # "virtual_price": contract.get_virtual_price() / 1e18,
        # "price_oracle": contract.price_oracle() / 1e18,
        # "price_scale": contract.price_scale() / 1e18,
        # "lp_price": contract.lp_price()
    }

if __name__ == "__main__":

    network.connect('mainnet')
    os.environ['ETHERSCAN_TOKEN'] = "AQ32B1YDEU89MN994AXWYFKQ1ZHY7RHHWC" # this is bad. remove this.

    # provider = Contract('0x0000000022D53366457F9d5E68Ec105046FC4383')
    # registry = Contract.from_explorer(provider.get_registry())
    # registry does not appear to have v2 pools linked yet. sad.
    
    # V2_ADDRESSES = {"eurtusd": "0x9838eCcC42659FA8AA7daF2aD134b53984c9427b"}
    for pool_name, address in V2_ADDRESSES.items():
        filepath = f"./data/{pool_name}.csv"
        print(f"Fetching stats for {pool_name}.")
        stats = get_stats(address)
        stats['timestamp'] = int(datetime.datetime.now().timestamp())
        print(f"Writing to {filepath}.", end="\n\n")
        with open(filepath, 'a', newline='') as file:
            dictwriter = DictWriter(file, fieldnames=stats.keys())
            dictwriter.writerow(stats)
            file.close()
        with open(filepath) as file:
            first_char = file.read(1)
            if first_char in '.-0123456789':
                add_header(filepath, stats.keys())
        