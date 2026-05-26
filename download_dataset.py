# from datasets import load_dataset

# dataset = load_dataset("DeweiFeng/SmellNet", "base_data")

# # 替换成你实际想存放的路径
# save_path = "/home/yufei/Desktops/SmellNet-main/"
# dataset.save_to_disk(save_path)


from huggingface_hub import snapshot_download

snapshot_download(
  repo_id="DeweiFeng/SmellNet",
  local_dir="/home/yufei/Desktops/SmellNet-main/",
  proxies={"https": "http://localhost:7890"},
  max_workers=8
)