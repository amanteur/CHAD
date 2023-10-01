import logging
import subprocess
from ast import literal_eval
from multiprocessing import cpu_count
from multiprocessing.dummy import Pool
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple

import pandas as pd
import yt_dlp
from more_itertools import chunked
from tqdm import tqdm

YDL_OPTS: Dict[str, Any] = {
    "format": "bestaudio/best",
    "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }
    ],
    "quiet": True,
    "noprogress": True,
}

YDL_INFO_KEYS: List[str] = [
    "id",
    "title",
    "channel_id",
    "channel",
    "uploader",
    "uploader_id",
    "duration",
    "asr",
    "availability",
]

N_CPUS: int = cpu_count()
RETRIEVE_ONLY_AVAILABLE_VIDEOS: bool = True

logger: logging.Logger = logging.getLogger(__name__)


class DatasetDownloader:
    """
    DatasetDownloader Class for downloading CHAD dataset.
    """

    def __init__(
        self,
        csv_path: str,
        tgt_dir: str,
        extension: str = '.mp3',
        save_fragments_audios: bool = True,
        save_full_audios: bool = False,
        save_metadata: bool = True,
        n_processes: Optional[int] = None,
        sr: int = 16000,
        mono: bool = True,
    ) -> None:
        """
        Initializes DatasetDownloader object.

        :param csv_path: Path to the CSV file.
        :param tgt_dir: Target directory for saving metadata.
        :param save_fragments_audios: Whether to save audio fragments.
        :param save_full_audios: Whether to save full audios.
        :param save_metadata: Whether to save YouTube metadata information.
        :param n_processes: Number of parallel processes.
        :param sr: Sample rate for audio.
        :param mono: Whether to convert audio to mono.
        """
        self.retrieve_only_available: bool = RETRIEVE_ONLY_AVAILABLE_VIDEOS

        self._setup_paths(csv_path, tgt_dir, extension)
        self._setup_flags(save_fragments_audios, save_full_audios, save_metadata)
        self._display_status_messages()

        self.df: pd.DataFrame = self._load_csv(csv_path)
        self.n_processes: int = (
            N_CPUS if n_processes is None else min(n_processes, N_CPUS)
        )

        self.sr: int = sr
        self.mono: bool = mono

    def _setup_paths(self, csv_path: str, tgt_dir: str, extension: str) -> None:
        """
        Prepares dataset paths and creates directories.

        :param csv_path: Path to the CSV file.
        :param tgt_dir: Path to the target directory.
        :param extension: Extension of saved audio file.
        """
        self.csv_path: str = csv_path
        self.tgt_dir: Path = Path(tgt_dir)
        self.extension: str = extension
        self.audio_dir: Path = self.tgt_dir / "youtube_audios"
        self.fragment_dir: Path = self.tgt_dir / "fragments"
        self.save_metadata_path = self.tgt_dir / "yt_metadata.csv"
        self.fragment_path_template: str = str(
            (self.fragment_dir / "{group_id}" / "{fragment_id}" / "{id}").with_suffix(self.extension)
        )
        self.audio_dir.mkdir(parents=True, exist_ok=True)
        self.fragment_dir.mkdir(parents=True, exist_ok=True)
        return None

    def _setup_flags(
        self, save_fragments_audios: bool, save_full_audios: bool, save_metadata: bool
    ) -> None:
        """
        Set flags for saving options and display status messages.
        """
        self.save_full_audios: bool = save_full_audios
        self.save_fragments_audios: bool = save_fragments_audios
        self.save_audios: bool = save_full_audios or save_fragments_audios
        self.save_metadata: bool = save_metadata
        self.dry_mode: bool = not (self.save_audios or self.save_metadata)
        return None

    def _display_status_messages(self) -> None:
        """
        Displays status messages based on saving options.
        """
        if self.save_fragments_audios:
            logger.info("Saving dataset's fragments...")
        if self.save_full_audios:
            logger.info("Saving audios from given YouTube links...")
        if self.save_metadata:
            logger.info("Saving YouTube videos metadata information...")
        if self.dry_mode:
            logger.info("Running in dry mode...")
        return None

    def _load_csv(self, csv_path: str) -> pd.DataFrame:
        """
        Loads CSV file and returns a DataFrame.

        :param csv_path: Path to the CSV file.
        :return: Loaded DataFrame.
        """
        df = pd.read_csv(csv_path)
        if self.retrieve_only_available:
            df = df[df["is_available"] & ~df["youtube_id"].isna()]
        df["interval"] = df["interval"].apply(literal_eval)
        return df

    def _download_audio(self, youtube_id: str) -> Dict[str, Any]:
        """
        Downloads audio from a YouTube link and returns its metadata.

        :param youtube_id: YouTube video ID.
        :return: Dictionary containing YouTube video metadata.
        """
        ydl_opts = {
            "outtmpl": f"{str(self.audio_dir)}/{youtube_id}.%(ext)s",
            **YDL_OPTS,
        }
        try:
            with yt_dlp.YoutubeDL(params=ydl_opts) as ydl:
                info_dict = ydl.extract_info(youtube_id, download=self.save_audios)
            info_dict = {k: info_dict[k] for k in info_dict if k in YDL_INFO_KEYS}
        except Exception as e:
            logger.warning(e)
            info_dict = {"id": youtube_id}
        return info_dict

    def _extract_fragments_from_audio(
        self,
        input_path: Path,
        path2intervals: List[Tuple[Path, Tuple[int, int]]],
    ) -> None:
        """
        Extract audio fragments from an MP3 file based on specified intervals and save to output paths.

        :param input_path: Path to the input MP3 file.
        :param path2intervals: List of tuples containing output paths and corresponding intervals.
        """
        codec: str = "libmp3lame" if self.extension == ".mp3" else "pcm_s16le"

        for output_path, interval in path2intervals:
            output_path.parent.mkdir(parents=True, exist_ok=True)

            start_time = str(int(interval[0]))
            end_time = str(int(interval[1]))

            # Run FFmpeg command to extract audio fragment
            ffmpeg_command = [
                "ffmpeg",
                "-v",
                "quiet",
                "-i",
                input_path,
                "-ss",
                start_time,
                "-to",
                end_time,
                "-c:a",
                codec,
                "-ar",
                str(self.sr),
                "-ac",
                "1" if self.mono else "2",
                "-y",
                output_path,
            ]
            subprocess.run(ffmpeg_command)

        # Remove the input file if save_full_audios is False
        if not self.save_full_audios:
            input_path.unlink()
        return None

    def _generate_paths_and_intervals(
        self,
    ) -> List[Tuple[Path, List[Tuple[Path, Tuple[int, int]]]]]:
        """
        Generate a list of tuples containing audio paths and corresponding intervals for fragment extraction.

        :return: List of tuples containing audio paths and intervals.
        """
        list_path2interval = []
        for audio_path in self.audio_dir.glob("*.mp3"):
            path2interval = []
            df_subset = self.df[self.df["youtube_id"].eq(audio_path.stem)]
            for i, r in df_subset.iterrows():
                output_path = Path(
                    self.fragment_path_template.format(
                        group_id=r["group_id"], fragment_id=r["fragment_id"], id=r["id"], extension=self.extension
                    )
                )
                intervals = r["interval"]
                path2interval.append((output_path, intervals))
            list_path2interval.append((audio_path, path2interval))
        return list_path2interval

    def _extract_all_fragments(self) -> None:
        """
        Extract all audio fragments from MP3 files based on intervals and save them.
        """
        batches = [
            b for b in chunked(self._generate_paths_and_intervals(), n=self.n_processes)
        ]
        with Pool(self.n_processes) as pool:
            for batch in batches:
                pool.starmap(self._extract_fragments_from_audio, batch)
        return None

    def _download_all_audios(self) -> pd.DataFrame:
        """
        Downloads audio from all YouTube links, extracts fragments,
        and returns a DataFrame containing metadata.

        :return: DataFrame containing metadata of downloaded YouTube videos.
        """
        # Split youtube_ids into batches for parallel downloading
        batches: list = [
            b
            for b in chunked(
                self.df["youtube_id"].unique().tolist(), n=self.n_processes
            )
        ]
        n_batches: int = len(batches)
        outputs: List = []

        # Use multiprocessing to download audio in parallel
        with Pool(self.n_processes) as pool:
            for i, batch in tqdm(enumerate(batches), total=n_batches):
                output = pool.map(self._download_audio, batch)
                outputs.extend(output)
                if self.save_fragments_audios:
                    self._extract_all_fragments()
                if (i + 1) % (n_batches // 20) == 0:
                    logger.info(f"Downloading of {i+1}/{n_batches} is complete...")

        # Create a DataFrame from the downloaded metadata
        yt_metadata_df = pd.DataFrame(outputs)
        return yt_metadata_df

    def _save_yt_metadata(self, yt_metadata_df: pd.DataFrame) -> None:
        """
        Save YouTube video metadata to a CSV file.

        :param yt_metadata_df: DataFrame containing YouTube video metadata.
        """
        yt_metadata_df.to_csv(self.save_metadata_path, index=False)
        return None

    def run(self) -> None:
        """
        Run the dataset preparation process.

        :return: DataFrame containing YouTube videos' metadata information if available.
        """
        logger.info("Starting dataset preparation...")
        if self.dry_mode:
            logger.info("dry_mode is enabled. Exiting...")
            return None

        # Download YouTube audios' metadata
        logger.info("Downloading audios from YouTube...")
        try:
            yt_metadata_df = self._download_all_audios()
        except Exception as e:
            logger.error(f"Error while downloading YouTube audios: {e}")
            return None

        # Save YouTube videos' metadata information if requested
        if self.save_metadata:
            logger.info("Saving YouTube metadata to csv...")
            try:
                self._save_yt_metadata(yt_metadata_df)
            except Exception as e:
                logger.error(f"Error while saving YouTube metadata: {e}")

        # Delete empty directory
        if not self.save_full_audios:
            try:
                self.audio_dir.rmdir()
            except Exception as e:
                logger.warning(f"Error while removing audio directory: {e}")

        logger.info("Dataset preparation completed!")
        return None
