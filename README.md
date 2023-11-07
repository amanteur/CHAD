# CHAD: Cover and Hummings Aligned Dataset

> This repository contains the official code of the paper ["A Semi-Supervised Deep Learning Approach to Dataset Collection for Query-by-Humming Task"](https://archives.ismir.net/ismir2023/paper/000077.pdf) published in the Proceedings of the [24th International Society for Music Information Retrieval (ISMIR) Conference, Milan, 2023](https://ismir2023.ismir.net).

The code is used for downloading the cover part of the dataset.

UPD:

The hummings subset of the dataset is now available on [HuggingFace](https://huggingface.co/datasets/amanteur/CHAD_hummings)!

---
## Table of Contents

1. [ToDo's](#todo)
2. [Dependencies](#dependencies)
3. [Usage](#usage)
4. [Dataset Structure](#structure)
   - [Hummings Subset](#hummings)
5. [Citation](#cite)

---

<a name="todo"/>

## ToDo's
- [x] Set up the repository
- [x] Add the dataset download pipeline
- [x] Include metadata in the download pipeline
- [x] Write the README.md
- [x] Upload the humming part of the dataset to HuggingFace


---

<a name="dependencies"/>

## Dependencies

To install all dependencies, run this command:
```bash
pip install -r requirements.txt
```

---
<a name="usage"/>

## Usage
To download the dataset, you can use the following command:
```bash
bash run.sh
```
This command runs the [`main.py`](src/main.py) script, which provides the following command-line options:
```
Usage: main.py [OPTIONS]

Options:
  --csv-path TEXT          Path to the CSV file containing dataset information
                           [required]
  --tgt-dir TEXT           Target directory for saving audio files and
                           fragments  [required]
  --extension TEXT         Extension of saved audio files
  --download-hf-dataset    Download hummings subset from HuggingFace
  --save-fragments-audios  Save audio fragments
  --save-full-audios       Save full audio files
  --save-metadata          Save YouTube metadata information
  --n-processes INTEGER    Number of processes for parallel processing
  --sr INTEGER             Sample rate for audio
  --mono / --no-mono       Mono or stereo audio
  --help                   Show this message and exit.
```
By running this command, you initiate the download of audio files firstly, from HuggingFace repo, and secondly, 
from YouTube and extraction of the necessary fragments from them.

In addition, there is a Jupyter Notebook [`notebooks/show_examples.ipynb`](notebooks/show_examples.ipynb), 
which displays random excerpts from the dataset.

---
<a name="structure"/>

## Dataset Structure
The [`metadata/dataset.csv`](metadata/dataset.csv) file provides information with the following fields:
- `group_id`: An identification code that serves as an identifier for a group of fragments. Essentially, it represents a unique track.
- `fragment_id`: An identification code assigned to each fragment within a group. A single group can contain multiple fragment IDs.
- `id`: An identification code that represents a specific version of a fragment, which can be a humming, cover, or the original track fragment.
- `audio_type`: This field indicates the type of the fragment, which could be categorized as 'original,' 'cover,' or 'humming'.
- `youtube_id`: A unique YouTube ID that links to the corresponding video.
- `interval`: The interval represents the left and right timestamp boundaries of the fragment within the full audio.
- `correlation`: Correlation value from 0 to 1 indicates the degree of similarity between a cover fragment and its original version.
- `check_by_crowdsource`: A boolean flag indicating whether the fragment underwent additional crowdsource assessment to determine its similarity to the original.
- `is_available`: This field specifies whether the YouTube video related to the fragment is currently available or not.
- `duration`: Duration denotes the length of the fragment in seconds.

The downloaded dataset is structured as follows:
```
├── {GROUP_ID}             
│   ├── {FRAGMENT_ID}        
│       ├── {ID}.{EXTENSION}
│       └── ...
│   └── ...
└── ...
```
This structured hierarchy organizes the audio files and fragments, making it easier to navigate and work with the dataset.

<a name="hummings"/>

### Hummings Subset

You can download the dataset directly via [HF](https://huggingface.co/datasets/amanteur/CHAD_hummings) or using `main.py` with the flag `--download-hf-dataset`. 

The `tar.gz` filestructure is the same as in the whole dataset. 

---
<a name="cite"/>

## Citation
Please cite the following paper if you use the code or dataset provided in this repository.

```bibtex
@inproceedings{Amatov2023,
    title={A Semi-Supervised Deep Learning Approach to Dataset Collection for Query-by-Humming Task},
    author={Amatov, Amantur and Lamanov, Dmitry and Titov, Maksim and Vovk, Ivan and Makarov, Ilya and Kudinov, Mikhail},
    booktitle={Proceedings of the 24th International Society for Music Information Retrieval Conference {(ISMIR)}},
    year={2023},
    url={https://archives.ismir.net/ismir2023/paper/000077.pdf},
}
```


