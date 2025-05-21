
# 0 Introduction
This repository is belong to the NeuralImaging paper **Synthetizing SWI from 3T to 7T by generative diffusion network for deep me-dullary veins visualization**.

The repository contains a demonstration of MRI3Tto7T, including a pretrained model for quick evaluation.
![Paper comparision](assets\Comparasion.png)
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
![Sample Image](runtime\evaluation_results\visualizations\sample_result.png)

## 2-1 Quick run
```Shell
python src\testing\eval.py
```
After running the inference, you can see the result under the folder `runtime\evaluation_results\visualizations\sample_result.png`
## 2-2 Configurations
The inference configurations can be found at [test_config.yaml](configs\test_config.yaml) 

# 3 Training
**<font color="red">Attention:</font>** For additional information (e.g., training hyper-parameters), please contact the author.

