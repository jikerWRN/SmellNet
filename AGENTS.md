# Repository Guidelines

## Project Structure & Module Organization
SmellNet is a Python and Arduino research repository for smell sensing, model training, and analysis. Core training and evaluation code lives in `models/`, with entry points such as `models/run.py` and `models/run_mixture.py`. Data preparation utilities are in `preprocessing/`, experiment wrappers in `scripts/`, and notebooks plus plotting scripts in `analysis/`. GC-MS processing code and generated figures are under `gcms_analysis/`. Sensor collection helpers are in `data_collection/`, firmware and vendored Arduino libraries in `Arduino/`, and README images in `assets/`. Large datasets such as `base_data/` and `gcms_processed/` are expected locally but are not tracked in Git.

## Build, Test, and Development Commands
Install Python dependencies with:

```bash
pip install -r requirements.txt
```

Run the base classification workflow from the repository root:

```bash
cd models
python run.py --train-dir ../base_data/training --test-dir ../base_data/testing --real-test-dir ../base_data/testing --gcms-csv ../gcms_processed/gcms_food_vectors.csv --models transformer --epochs 90 --batch-size 32 --lr 0.001
```

Run mixture prediction with `python models/run_mixture.py`; use `scripts/run_experiment.bash` for fuller experiment templates. Regenerate analysis artifacts with scripts such as `python analysis/generate_pca_iclr.py` when required local data is present.

## Coding Style & Naming Conventions
Use Python 3.10+ syntax where existing code does, including type hints such as `str | None`. Follow the current style: 4-space indentation, `snake_case` for functions, files, and variables, and `PascalCase` for model classes. Keep command-line scripts based on `argparse`, prefer `pathlib.Path` for new paths, and avoid hard-coded absolute paths. Preserve module boundaries: training in `models/`, preprocessing in `preprocessing/`, and analysis in `analysis/` or `gcms_analysis/`.

## Testing Guidelines
There is no dedicated test suite or coverage configuration. Before submitting changes, run the smallest relevant script with a lightweight local dataset or reduced arguments, and document the command used. For model changes, verify importability and one short training/evaluation path. If adding tests, place them in `tests/` and name files `test_*.py`.

## Commit & Pull Request Guidelines
The visible Git history does not define a strong commit convention, so use concise imperative subjects such as `Add mixture evaluation summary` or `Fix GC-MS CSV loading`. Pull requests should describe the motivation, list changed modules, note required local data paths, and include plots or screenshots when analysis output changes. Mention commands run and any skipped because datasets were unavailable.

## Security & Configuration Tips
Do not commit downloaded sensor datasets, generated large artifacts, credentials, or machine-specific paths. Keep third-party Arduino libraries under `Arduino/libraries/` only when they are required for reproducible firmware builds.
