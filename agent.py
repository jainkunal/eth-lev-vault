import os
from datetime import datetime, timedelta
from giza.agents import AgentResult, GizaAgent
from starknet_py.contract import Contract
from starknet_py.net.account.account import Account
from starknet_py.net.models import StarknetChainId
from starknet_py.net.signer.stark_curve_signer import KeyPair
from starknet_py.net.full_node_client import FullNodeClient
from dotenv import load_dotenv
import types

from model.data import get_data

load_dotenv()

MODEL_ID = 766
VERSION_ID = 1
ENDPOINT_ID = 336
NODE_URL = "https://starknet-sepolia.g.alchemy.com/v2/NE-Z9O1CgPCq28BJiaffMf9JPzvxaNBS"
ADDRESS = "0x00eA6b9d15886250e60a2eDF0Cb0673cb94306F350f78435f7112073e251C6Ed"
PRIVATE_KEY = os.getenv("PRIVATE_KEY")

inference_endpoint = "https://endpoint-kunaljain-766-1-9dd04ab1-7i3yxzspbq-ew.a.run.app"
client = FullNodeClient(node_url=NODE_URL)

account = Account(
    address=ADDRESS,
    client=client,
    key_pair=KeyPair.from_private_key(PRIVATE_KEY),
    chain=StarknetChainId.SEPOLIA,
)


# ======= Create spurious function to please GizaAgent
def upper_method(self):
    return "ACC"


account.upper = types.MethodType(upper_method, account)
# ======= End


today = datetime.today().strftime("%Y-%m-%d")
start = (datetime.today() - timedelta(days=60)).strftime("%Y-%m-%d")

df = get_data(start=start, end=today)

agent = GizaAgent(
    id=MODEL_ID,
    version_id=VERSION_ID,
    chain=f"starknet:sepolia:{NODE_URL}",
    contracts={
        "ETH2X": "0x00af269b779a997a3fc7fe98f119f1e56f8f5546a7e1974a89698c360c2665fe"
    },
    account=account,
)

X = df.tail(1).to_numpy()
result = agent.predict(input_feed=X, verifiable=False)
print(result)

with agent.execute() as contracts:
    print(contracts)
    r = contracts.ETH2X.rebalance(result.value)
    print(r)
