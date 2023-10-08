import datetime
import logging
import tarfile
from pathlib import Path

from huggingface_hub import hf_hub_download

LOG_DIR: str = "./logs"
HF_REPO_ID: str = "amanteur/CHAD_hummings"
HF_FILENAME: str = "chad_hummings_subset.tar.gz"


def setup_logging() -> None:
    Path(LOG_DIR).mkdir(parents=True, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(f"{LOG_DIR}/{timestamp}.log"),
            logging.StreamHandler(),
        ],
    )


def download_and_extract_hf_dataset(tgt_dir: str) -> None:
    tgt_dir: Path = Path(tgt_dir)
    tgt_filepath: Path = tgt_dir / HF_FILENAME
    tgt_fragments_dir: Path = tgt_dir / "fragments"

    Path(tgt_dir).mkdir(parents=True, exist_ok=True)
    Path(tgt_fragments_dir).mkdir(parents=True, exist_ok=True)

    hf_hub_download(
        repo_id=HF_REPO_ID,
        filename=HF_FILENAME,
        local_dir=tgt_dir,
        repo_type="dataset",
    )

    tar = tarfile.open(tgt_filepath, "r:gz")
    tar.extractall(path=tgt_fragments_dir)
    tar.close()
