from basert_agent.runner import LocalBaseRTAgent
from basert_agent.attestation import BaseRTReceipt

def test_runner():
    agent = LocalBaseRTAgent(model_id="basecompute/gemma-4-E4B-it")
    res = agent.run_task("Write a fast sorting function")
    assert res["status"] == "SUCCESS"
    assert "generated_code" in res
    assert res["receipt"]["protocol"] == "basert/hdar/v1"
    assert res["receipt"]["attestation"]["local_only"] is True

def test_receipt():
    receipt = BaseRTReceipt.generate_receipt("test", "model", "code", 12.5)
    assert "output_hash" in receipt
    assert receipt["attestation"]["verified_metal_execution"] is True
