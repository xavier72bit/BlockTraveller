# std import
import sys
import argparse

# local import
from blockchain.roles.node.http_node import NodeHttpSingle


parser = argparse.ArgumentParser(description="Run the blockchain component.")
parser.add_argument(
    "-r", "--role",
    type=str,
    required=True,
    choices=["wallet", "miner", "node"],
    help="Choose a role: wallet / miner / node"
)

def run_wallet():
    pass

def run_miner():
    pass

def run_node():
    NodeHttpSingle().run()

def main():
    args = parser.parse_args()

    if args.role == "wallet":
        run_wallet()
    elif args.role == "miner":
        run_miner()
    elif args.role == "node":
        run_node()
    else:
        print("Invalid role specified.", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
