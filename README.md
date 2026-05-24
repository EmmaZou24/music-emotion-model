# music-emotion-model

source venv/bin/activate

## Data Setup

1. Clone the MTG-Jamendo dataset repository and download the mood/theme subset. You may stop it after the first 35 tar files are downloaded.
```bash
  git clone https://github.com/MTG/mtg-jamendo-dataset.git
  cd mtg-jamendo-dataset
  python3 ../mtg-jamendo-dataset/scripts/download/download.py \
    --dataset autotagging_moodtheme \
    --type melspecs \
    --unpack --remove \
    ../music-emotion-model/data/raw/
```

2. Unpack the .tar files into .npy files via this command:
```bash
for f in data/raw/*.tar; do
    tar -xf "$f" -C data/raw/melspecs/
done
```