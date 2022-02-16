from brownie import Contract, network
from constants import v2_pool_contracts
network.connect('mainnet')
provider = Contract('0x0000000022D53366457F9d5E68Ec105046FC4383')  # Curve Registry's Address Provider
registry = Contract.from_explorer(provider.get_registry())
fees = [registry.get_fees(contract) for contract in v2_pool_contracts.values()]
[print(f"{name}: {fee*1e-8} {admin_pct*1e-8}") for name, (fee, admin_pct) in zip(v2_pool_contracts.keys(), fees)]
