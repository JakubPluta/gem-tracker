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

    args = parser.parse_args()
    generate(str(args.token_address))
