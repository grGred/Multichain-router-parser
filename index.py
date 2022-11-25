from itertools import chain
import requests
API_LINK = "https://bridgeapi.anyswap.exchange/v4/tokenlistv4/"
chain_ids = [1, 56, 137, 43114, 250, 1285, 42161, 10, 1284, 100, 25, 122, 66, 42220, 288, 40, 2222, 32520, 1088, 42262, 8217, 106, 57, 53935]
# ANY_METHODS = ['anySwapOut(anytoken,toAddress,amount,toChainID)', 'anySwapOutUnderlying(anytoken,toAddress,amount,toChainID)', 'anySwapOutNative(anytoken,toAddress,toChainID,{value: amount})']
ANY_METHODS = ['Swapout(amount,toAddress)']
ids_to_routers = {}
routers = []

def is_supported_chain(chain_to_compare):
    try: 
        chain_to_compare = int(chain_to_compare)
    except ValueError: # not evm
        return False
    for chain in chain_ids:
        if chain == chain_to_compare:
            return True
    return False

def is_new_router(pending_router, chain_id):
    if pending_router in ids_to_routers[chain_id]:
        return False
    return True

for i in range(len(chain_ids)):
    ids_to_routers[str(chain_ids[i])] = []

for id in chain_ids:
    response = requests.get(API_LINK + str(id))
    response_json = response.json()

    for values in response_json.values():
        destChains = values.get('destChains')
        for network_id, values_chains in destChains.items():
            for vals in values_chains.values():
                if(is_supported_chain(vals.get('chainId'))):
                    if vals.get('routerABI') in ANY_METHODS:
                        pending_router = vals.get('router')
                        if is_new_router(pending_router, str(id)):
                            ids_to_routers[str(id)].append(pending_router)
lendsand = 0
for chain in chain_ids:
    print(chain)
    print(ids_to_routers[str(chain)])
    lendsand += len(ids_to_routers[str(chain)])
    print('---------------------------------')
    
print(lendsand)
