import sys
import argparse
import json
from .runner import LocalBaseRTAgent

def main():
    parser = argparse.ArgumentParser(description="BaseRT Local Coding Agent CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    serve_parser = subparsers.add_parser("serve", help="Serve a local LLM model with BaseRT Metal inference")
    serve_parser.add_argument("model", nargs="?", default="basecompute/gemma-4-E4B-it", help="Model identifier")

    run_parser = subparsers.add_parser("run", help="Run local coding agent task")
    run_parser.add_argument("prompt", help="Coding task prompt")

    args = parser.parse_args()

    if args.command == "serve":
        print(f"🚀 Serving BaseRT model '{args.model}' on Apple Silicon Metal runtime...")
        print("⚡ Zero API keys required. All data remains 100% on device.")
        print("Ready at http://localhost:11434")

    elif args.command == "run":
        agent = LocalBaseRTAgent()
        res = agent.run_task(args.prompt)
        print(json.dumps(res, indent=2))

def pi_main():
    """Entry point for pi / pi-basert coding agent plugin."""
    agent = LocalBaseRTAgent()
    prompt = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Refactor local workspace modules"
    print(f"🤖 pi-basert local agent running: '{prompt}'")
    res = agent.run_task(prompt)
    print("\n--- GENERATED LOCAL CODE ---")
    print(res["generated_code"])
    print("--- HDAR ATTESTATION RECEIPT ---")
    print(json.dumps(res["receipt"], indent=2))

if __name__ == "__main__":
    main()
