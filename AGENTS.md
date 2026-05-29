# Repository Guidelines

## Project Structure & Module Organization
SmellNet is a Python and Arduino research repository for smell sensing, model training, and analysis. Core code lives in `models/`, especially `models/run.py` and `models/run_mixture.py`. Data preparation is in `preprocessing/`, experiment wrappers in `scripts/`, notebooks and plots in `analysis/`, and GC-MS processing in `gcms_analysis/`. Sensor helpers are in `data_collection/`, firmware in `Arduino/`, and README images in `assets/`. Large datasets such as `base_data/` and `gcms_processed/` are local-only.

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

Run mixture prediction with `python models/run_mixture.py`; use `scripts/run_experiment.bash` for sweep templates.

## Contrastive Learning Path
Enable cross-modal training with `--contrastive on` in `models/run.py`. Sensor CSVs are baseline-corrected, windowed, and standardized as `[N, T, C]`; `gcms_food_vectors.csv` provides one fixed GC-MS vector per food class. `create_pair_data()` pairs each sensor window with the GC-MS vector for the same encoded label. Training uses a sensor encoder from `get_model()` and a `GCMSMLPEncoder`. `contrastive_train()` calls `forward_features()` on both and optimizes only `cross_modal_contrastive_loss`; no classification loss is added. `evaluate_contrastive()` predicts by embedding similarity against all GC-MS class embeddings.

## Coding Style & Naming Conventions
Use Python 3.10+ syntax where existing code does. Follow the current style: 4-space indentation, `snake_case` for functions/files/variables, and `PascalCase` for model classes. Use `argparse` for CLIs, prefer `pathlib.Path`, and avoid hard-coded absolute paths.

## Testing Guidelines
There is no dedicated test suite or coverage configuration. Before submitting changes, run the smallest relevant script with a lightweight dataset or reduced arguments. For model changes, verify importability and one short training/evaluation path. If adding tests, place them in `tests/` and name files `test_*.py`.

## Commit & Pull Request Guidelines
The visible Git history does not define a strong commit convention, so use concise imperative subjects such as `Add mixture evaluation summary`. Pull requests should describe motivation, changed modules, required data paths, changed plots, and commands run.

## Security & Configuration Tips
Do not commit downloaded sensor datasets, generated large artifacts, credentials, or machine-specific paths. Keep third-party Arduino libraries under `Arduino/libraries/` only when they are required for reproducible firmware builds.
