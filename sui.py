```python
from dataclasses import dataclass
from datetime import datetime
import json
import logging
import uuid


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)


@dataclass
class NetworkConfig:
    name: str
    rpc_url: str
    chain_id: int


@dataclass
class AccountProfile:
    address: str


class MetadataFactory:

    def __init__(self):
        self.network = "sui"

    def create(self):

        return {
            "id": str(uuid.uuid4()),
            "network": self.network,
            "created": datetime.utcnow().isoformat()
        }


class RequestBuilder:

    def __init__(
        self,
        account,
        contract
    ):
        self.account = account
        self.contract = contract
        self.factory = MetadataFactory()

    def build(self):

        return {
            "from": self.account.address,
            "to": self.contract,
            "value": 0,
            "payload": self.factory.create()
        }


class RequestValidator:

    REQUIRED_FIELDS = [
        "from",
        "to",
        "value",
        "payload"
    ]

    @classmethod
    def validate(cls, request):

        for field in cls.REQUIRED_FIELDS:
            if field not in request:
                raise ValueError(
                    f"Missing field: {field}"
                )

        if not isinstance(
            request["payload"],
            dict
        ):
            raise TypeError(
                "Payload must be a dictionary."
            )

        return True


class Serializer:

    @staticmethod
    def encode(request):

        return json.dumps(
            request,
            indent=2,
            sort_keys=True
        )


class ContractInteraction:

    def __init__(
        self,
        config,
        account
    ):
        self.config = config
        self.account = account

    def prepare(
        self,
        contract
    ):

        builder = RequestBuilder(
            self.account,
            contract
        )

        request = builder.build()

        RequestValidator.validate(
            request
        )

        return request

    def sign_transaction(
        self,
        request
    ):
        raise NotImplementedError(
            "Signing is intentionally omitted in this educational example."
        )


class Reporter:

    @staticmethod
    def print_header():

        print("=" * 60)
        print("Interaction Preview")
        print("=" * 60)

    @staticmethod
    def print_request(request):

        print(
            Serializer.encode(
                request
            )
        )

    @staticmethod
    def print_footer():

        print("=" * 60)
        print("Preview Complete")
        print("=" * 60)


def load_configuration():

    return NetworkConfig(
        name="sui",
        rpc_url="https://example-rpc.invalid",
        chain_id=0
    )


def load_account():

    return AccountProfile(
        address="0xABCDEF1234567890ABCDEF1234567890ABCDEF12"
    )


def main():

    logging.info(
        "Loading configuration"
    )

    config = load_configuration()

    account = load_account()

    interaction = ContractInteraction(
        config,
        account
    )

    request = interaction.prepare(
        "0x1234567890123456789012345678901234567890"
    )

    Reporter.print_header()

    Reporter.print_request(
        request
    )

    Reporter.print_footer()

    print("Network:", config.name)
    print("RPC:", config.rpc_url)
    print("Chain ID:", config.chain_id)
    print("Account:", account.address)
    print("Status: Ready for review")


if __name__ == "__main__":
    main()
```
