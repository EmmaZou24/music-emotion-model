# music-emotion-model

source venv/bin/activate

## Data Setup

1. Clone the MTG-Jamendo dataset repository and copy `autotagging_moodtheme.tsv` and `raw.meta.tsv` from the data folder into the `data/raw/` folder of this repo.

2. CDownload the mood/theme subset with the following command. You may stop it after the first 35 tar files are downloaded.
```bash
  git clone https://github.com/MTG/mtg-jamendo-dataset.git
  cd mtg-jamendo-dataset
  python3 ../mtg-jamendo-dataset/scripts/download/download.py \
    --dataset autotagging_moodtheme \
    --type melspecs \
    --unpack --remove \
    ../music-emotion-model/data/raw/
```

3. Unpack the .tar files into .npy files via this command. Delete the .tar files once done!
```bash
for f in data/raw/*.tar; do
    tar -xf "$f" -C data/raw/melspecs/
done
```