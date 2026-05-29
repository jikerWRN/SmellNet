cd models
for lr in 0.0003 0.001 0.003; do
  python run.py \
    --train-dir ../base_data/training \
    --test-dir ../base_data/testing \
    --real-test-dir ../base_data/testing \
    --gcms-csv ../gcms_processed/gcms_food_vectors.csv \
    --models transformer \
    --contrastive on \
    --window-sizes 100 \
    --gradients 25 \
    --epochs 90 \
    --batch-size 32 \
    --lr "$lr"
done
