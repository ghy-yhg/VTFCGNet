# VTFCGNet: A novel cross-modal reasoning network integrating Fourier self-attention and graph attention for visual text question answering
For more details about the method, please refer to the paper

![Model overall framework flow chart](图片链接 "图片标题")


## Dataset Setup
You can download the data [website](http://vtqa-challenge.fixtankwun.top:20010/).
Unzip the files and place them as follows:
```text
data
├── images
│   ├── train
│   ├── val
│   └── test_dev
└── annotations
```

## Config Introduction
```text
pip install -r requirements.txt
```
## Clone demo code
```text
cd /workspace
git clone https://github.com/ghy-yhg/VTFCGNet
```
## Train, val & test
```text
cd /workspace
python main.py --RUN train
```
## Citation
If this repository is helpful for your research, we'd really appreciate it if you could cite the following paper:

```

@article{Currently submitted to The visual computer,
  author    = {Yujie Huo and Weng Howe Chan and Song Yu and Hongyu Gao},
  title     = {VTFCGNet: A Fourier Frequency and Spatial Attention Filtering Mechanism for Entity Alignment and Cross-Modal Reasoning in Visual Text Question Answering},
  journal   = {The Visual Computer},
  year      = {2025},
  doi       = {We will update the above DOI after the paper is officially published}
}
```
