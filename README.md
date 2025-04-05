# [VTFCGNet: A novel cross-modal reasoning network integrating Fourier self-attention and graph attention for visual text question answering](http://)

[**Yujie Huo, Weng Howe Chan, Song Yu and Hongyu Gao**](http://)


### For more details about the method, please refer to the paper

## Dataset Setup
You can download the data [website](https://huggingface.co/datasets/CalfKing/vtqa2023)
Unzip the files and place them as follows:
```text
data
├── images
│   ├── train
│   ├── val
│   └── test_dev
└── annotations
```
## Clone demo code
```text
cd /workspace
git clone https://github.com/ghy-yhg/VTFCGNet
```
## Config Introduction
```text
pip install -r requirements.txt
```
## Train, val & test
```text
cd /workspace
python main.py --RUN train
```
## Issue
If there is an issue, please send an email to this address，huoyujie@graduate.utm.my
## Citation
If this repository is helpful for your research, we'd really appreciate it if you could cite the following paper:

```

@article{Currently submitted to Applied Intelligence,
  author    = {Yujie Huo and Weng Howe Chan and Song Yu and Hongyu Gao},
  title     = {VTFCGNet: A novel cross-modal reasoning network integrating Fourier self-attention and graph attention for visual text question answering},
  journal   = {Applied Intelligence},
  year      = {2025},
  doi       = {We will update the above DOI after the paper is officially published}
}
```
