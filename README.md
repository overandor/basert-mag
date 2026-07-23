# BaseRT Local Coding Agent (`basert-agent`) 🚀

Fastest LLM inference runtime & local coding agent plugin for Apple Silicon via native Metal, with verifiable HDAR attestation receipts. Zero API keys, 100% on-device data privacy.

## Quick Start

```bash
# 1. Install basert-agent
pip install basert-agent

# 2. Serve a model locally on Apple Silicon Metal
basert-agent serve basecompute/gemma-4-E4B-it

# 3. Run pi-basert local coding agent
pi-basert "Refactor local workspace modules"
```

## Features

- ⚡ **Native Metal Apple Silicon Acceleration**: High-throughput local LLM inference.
- 🔒 **Zero Data Leakage**: No external API keys required; 100% on-device execution.
- 🛡️ **Verifiable HDAR Attestation Receipts**: Every code generation produces cryptographic SHA-256 integrity proofs and Merkle roots.

## License
MIT License
