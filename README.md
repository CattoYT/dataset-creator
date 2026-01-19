# Dataset-creator (Koequet)

The $\displaystyle{\lim_{n \to \infty}}$ best audio dataset formatter!

This is currently compatible with datasets from [Ai Hobbyist's datasets](https://github.com/AI-Hobbyist/StarRail_Datasets), but in the future will be compatible with as many formats as I care about.  
This currently supports exporting to parquet (hence the shit name), with LJSpeech coming soon!

# Installation
## Method 1: uv
1. Download the src
2. run ```uv sync``` to download dependencies for your GPU
3. run ```uv run src/main.py``` to start!

## Method 2: pre-built nuitka binary
1. Download the binary
2. Pray
3. Run the .exe
4. pray
5. ???
6. profit?

Please just do method 1. Also method 2 is already outdated 💀  
Method 2 is also completely untested on any device other than my own soooooo your mileage may vary. I can guarantee method 1 works though.


## Feature list
- Manual quick sorting ui
- Parquet exporter
- Audio reformatter
- ML audio processing (its just uvr lmao)

## How 2 use for dummies
1. Import dataset directory
2. Press 1
3. Go through using W, E, R to process the dataset
4. Finish sorting
5. Press 3 to export or 2 to process the poor quality files before exporting (doesn't guarantee the files become good)
6. Export the parquet file to HF or something idk