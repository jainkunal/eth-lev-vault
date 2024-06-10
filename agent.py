import asyncio
import math
import os
from datetime import datetime, timedelta
from giza.agents.model import GizaModel
from sklearn.discriminant_analysis import StandardScaler
from starknet_py.net.account.account import Account
from starknet_py.net.models import StarknetChainId
from starknet_py.net.signer.stark_curve_signer import KeyPair
from starknet_py.net.full_node_client import FullNodeClient
from dotenv import load_dotenv
import types
import contract_abi
from starknet_py.serialization.factory import serializer_for_function_v1
from starknet_py.net.client_models import Call

from model.data import get_data

load_dotenv()

MODEL_ID = 766
VERSION_ID = 1
ENDPOINT_ID = 336
NODE_URL = "https://starknet-sepolia.g.alchemy.com/v2/NE-Z9O1CgPCq28BJiaffMf9JPzvxaNBS"
ADDRESS = "0x00eA6b9d15886250e60a2eDF0Cb0673cb94306F350f78435f7112073e251C6Ed"
PRIVATE_KEY = os.getenv("PRIVATE_KEY")

client = FullNodeClient(node_url=NODE_URL)


async def rebalance():
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
    start = (datetime.today() - timedelta(days=90)).strftime("%Y-%m-%d")

    df = get_data(start=start, end=today)

    model = GizaModel(
        id=MODEL_ID,
        version=VERSION_ID,
    )
    df.loc[df.index[-1], "Chikou_Span"] = 0

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df)

    X = X_scaled[-1]
    result = model.predict(
        input_feed={"X": X}, verifiable=True, dry_run=True, model_category="XGB"
    )
    print(result)
    prediction = result[0]
    final_score = 1 / (1 + math.exp(-prediction))

    rebalance_function = serializer_for_function_v1(
        contract_abi.abi.interfaces["vault::vault::IRebalanceTrait"].items["rebalance"]
    )

    await account.execute_v1(
        calls=[
            Call(
                to_addr=int(
                    0x00AF269B779A997A3FC7FE98F119F1E56F8F5546A7E1974A89698C360C2665FE
                ),
                selector=int(
                    0xC208A167AB75A6661E860105174F4451C43E691D80C61030D220A52B8174D5
                ),
                calldata=rebalance_function.serialize(final_score >= 0.7),
            )
        ],
        max_fee=170351367819270,
    )


if __name__ == "__main__":
    asyncio.run(rebalance())
