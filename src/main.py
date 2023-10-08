import logging

import click

from downloader import DatasetDownloader
from utils import setup_logging, download_and_extract_hf_dataset

setup_logging()
logger: logging.Logger = logging.getLogger(__name__)


@click.command()
@click.option(
    "--csv-path",
    required=True,
    help="Path to the CSV file containing dataset information",
)
@click.option(
    "--tgt-dir",
    required=True,
    help="Target directory for saving audio files and fragments",
)
@click.option(
    "--extension",
    default=".mp3",
    help="Extension of saved audio files",
)
@click.option(
    "--download-hf-dataset",
    is_flag=True,
    type=bool,
    help="Download hummings subset from HuggingFace",
)
@click.option(
    "--save-fragments-audios", is_flag=True, type=bool, help="Save audio fragments"
)
@click.option(
    "--save-full-audios", is_flag=True, type=bool, help="Save full audio files"
)
@click.option(
    "--save-metadata", is_flag=True, type=bool, help="Save YouTube metadata information"
)
@click.option(
    "--n-processes",
    default=8,
    type=int,
    help="Number of processes for parallel processing",
)
@click.option("--sr", default=16000, type=int, help="Sample rate for audio")
@click.option("--mono/--no-mono", default=True, type=bool, help="Mono or stereo audio")
def main(
    csv_path: str,
    tgt_dir: str,
    extension: str,
    download_hf_dataset: bool,
    save_fragments_audios: bool,
    save_full_audios: bool,
    save_metadata: bool,
    n_processes: int,
    sr: int,
    mono: bool,
):
    if download_hf_dataset:
        logger.info("Starting downloading hummings subset from HuggingFace...")
        try:
            download_and_extract_hf_dataset(tgt_dir)
        except Exception as e:
            logger.exception(
                "An error occurred during downloading dataset from HuggingFace: %s",
                str(e),
            )

    logger.info("Starting downloading cover subset from YouTube...")
    try:
        downloader = DatasetDownloader(
            csv_path=csv_path,
            tgt_dir=tgt_dir,
            extension=extension,
            save_fragments_audios=save_fragments_audios,
            save_full_audios=save_full_audios,
            save_metadata=save_metadata,
            n_processes=n_processes,
            sr=sr,
            mono=mono,
        )
        downloader.run()

    except Exception as e:
        logger.exception(
            "An error occurred during downloading dataset from YouTube: %s", str(e)
        )
    return None


if __name__ == "__main__":
    main()
