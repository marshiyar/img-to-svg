# Image to SVG

Convert images (PNG, JPG, etc.) to SVG vectors.

## Installation

```bash
pip install .
```
![use demo](guide/image.png)

## Requirements

- Python 3.7+
- macOS (for run.sh script)

## Usage

**Using run.sh:**



```bash
 chmod +x run.sh
```
```bash
./run.sh path/to/image.png
```

Output SVG is saved in the same directory.

## Options
```bash
./run.sh image.png --mode maximum 
./run.sh image.png --mode high
./run.sh image.png --mode medium
./run.sh image.png --mode fast
```
