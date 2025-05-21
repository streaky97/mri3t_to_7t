# 0 Introduction

This repository contains a demonstration of MRI3Tto7T, including a pretrained model for quick evaluation.
![Sample Image](runtime\evaluation_results\visualizations\sample_result.png)
# 1 Installation
## 1-1 Create a virtual environment
```Shell
uv venv .venv
```

## Activate the environment and install dependencies
```Shell
uv pip install -r requirements.txt
```

# 2 Sample inference
Running a Sample Inference A sample input file (.npy) is included for demonstration purposes.
## 2-1 Quick run
```Shell
python src\testing\eval.py
```
## 2-2 Configurations
The inference configurations can be found at [test_config.yaml](configs\test_config.yaml) 

# 3 Training
**<font color="red">Attention:</font>** For additional information (e.g., training hyper-parameters), please contact the author.

