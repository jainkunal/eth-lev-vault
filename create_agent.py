import os
from giza.cli.client import AgentsClient
from starknet_py.net.account.account import Account
from starknet_py.net.models import StarknetChainId
from starknet_py.net.signer.stark_curve_signer import KeyPair
from starknet_py.net.full_node_client import FullNodeClient
from giza.cli.schemas.agents import AgentCreate
from dotenv import load_dotenv

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

agent_create = AgentCreate(
    name="lev-eth",
    description="predicts if should leverage up eth or not",
    parameters={
        "model_id": MODEL_ID,
        "version_id": VERSION_ID,
        "endpoint_id": ENDPOINT_ID,
        "account": ADDRESS,
        "account_data": PRIVATE_KEY,
    },
)
client = AgentsClient("https://api.gizatech.xyz")
agent = client.create(agent_create)

print(agent.model_dump_json())
