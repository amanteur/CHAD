import datetime
import logging

import click

from downloader import DatasetDownloader

LOG_DIR = "./logs"


def setup_logging():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(f"{LOG_DIR}/{timestamp}.log"),
            logging.StreamHandler(),
        ],
    )


@click.command()
@click.option(
    "--csv_path",
    required=True,
    help="Path to the CSV file containing dataset information",
)
@click.option(
    "--tgt_dir",
    required=True,
    help="Target directory for saving audio files and fragments",
)
@click.option(
    "--extension",
    default=".mp3",
    help="Extension of saved audio files",
)
@click.option(
    "--save_fragments_audios", default=True, type=bool, help="Save audio fragments"
)
@click.option(
    "--save_full_audios", default=False, type=bool, help="Save full audio files"
)
@click.option(
    "--save_metadata", default=True, type=bool, help="Save YouTube metadata information"
)
@click.option(
    "--n_processes",
    default=8,
    type=int,
    help="Number of processes for parallel processing",
)
@click.option("--sr", default=16000, type=int, help="Sample rate for audio")
@click.option("--mono/--no-mono", default=True, help="Mono or stereo audio")
def main(
    csv_path,
    tgt_dir,
    extension,
    save_fragments_audios,
    save_full_audios,
    save_metadata,
    n_processes,
    sr,
    mono,
):
    setup_logging()
    logger = logging.getLogger(__name__)

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
        logger.exception("An error occurred during dataset preparation: %s", str(e))
    return None


if __name__ == "__main__":
    main()
