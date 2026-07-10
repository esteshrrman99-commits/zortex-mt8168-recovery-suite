from zortex.pipeline.runner import BLOCK_MESSAGE, execute_pipeline


def test_pipeline_remains_read_only() -> None:
    report = execute_pipeline()

    assert report["mode"] == "read-only"
    assert report["deployment_authorized"] is False
    assert report["decision"] == BLOCK_MESSAGE


def test_pipeline_creates_artifact_manifest() -> None:
    report = execute_pipeline()

    assert isinstance(report["artifacts"], list)
    assert report["artifact_count"] == len(report["artifacts"])


def test_artifacts_have_two_hashes() -> None:
    report = execute_pipeline()

    for artifact in report["artifacts"]:
        assert len(artifact["sha256"]) == 64
        assert len(artifact["sha512"]) == 128
