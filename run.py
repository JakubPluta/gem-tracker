import argparse
import os
from app import generate


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--token_address",
        dest="token_address",
        type=str,
        help="token address",
        required=True,
    )
    parser.add_argument(
        "--api_key",
        dest="api_key",
        type=str,
        help="api key for ethplorer",
        required=True,
    )

    args = parser.parse_args()
    generate(str(args.token_address), str(args.api_key))
