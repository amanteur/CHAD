# CHAD: Cover and Hummings Aligned Dataset

This repository contains the official code of ["A Semi-Supervised Deep Learning Approach to Dataset Collection for Query-by-Humming Task"]() (ISMIR 2023).

The code is used for downloading the dataset from YouTube.

---
## Table of Contents

1. [ToDo](#todo)
1. [Dependencies](#dependencies)
3. [Usage](#usage)
4. [Repository structure](#structure)
5. [Citation](#cite)

---

<a name="todo"/>

## ToDo
- [x] Set up the repository
- [x] Add the dataset download pipeline
- [x] Include metadata in the download pipeline
- [x] Write the README.md
- [ ] Upload the humming part of the dataset


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
This command runs the `main.py` script, which provides the following command-line options:
```bash
Usage: main.py [OPTIONS]

Options:
  --csv_path TEXT                 Path to the CSV file containing dataset
                                  information  [required]
  --tgt_dir TEXT                  Target directory for saving audio files and
                                  fragments  [required]
  --extension TEXT                Extension of saved audio files
  --save_fragments_audios BOOLEAN
                                  Save audio fragments
  --save_full_audios BOOLEAN      Save full audio files
  --save_metadata BOOLEAN         Save YouTube metadata information
  --n_processes INTEGER           Number of processes for parallel processing
  --sr INTEGER                    Sample rate for audio
  --mono / --no-mono              Mono or stereo audio
  --help                          Show this message and exit.
```
By running this command, you initiate the download of audio files from YouTube and extraction of the necessary fragments from them.

---
<a name="structure"/>

## Dataset structure
The `metadata/dataset.csv` file provides information with the following fields:
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

---
<a name="cite"/>

## Citation
Please cite the following paper if you use the code or dataset provided in this repository.

```bibtex
@inproceedings{Amatov2023,
    title={A Semi-Supervised Deep Learning Approach to Dataset Collection for Query-by-Humming Task},
    author={Amatov, Amantur and Lamanov, Dmitry and Titov, Maksim and Vovk, Ivan and Makarov, Ilya and Kudinov, Mikhail},
    year={2023},
}
```


