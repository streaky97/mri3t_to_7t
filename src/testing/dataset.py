import glob
import numpy as np
from PIL import Image
import cv2
import torch
import os
import json

class mriDataset(torch.utils.data.Dataset):
    """Initialize a mri Dataset
    Args:
        torch (_type_): _description_
    """
    def __init__(self,json_path,resized=None,clip=True) -> None:

        super().__init__()
        # Reading image path from json.
        with open(json_path,"r") as f:
            img_dict = json.load(f)
        self.mri3TPath = img_dict["Test"]["3T"]
        self.resized = resized if resized is not None else None
        self.clip = clip
        assert len(self.mri3TPath) !=0, f"The mri3TPath: {self.mri3TPath} not exist!"

    def __getitem__(self,index,mode="RGB"):
        index=0
        imgId = os.path.basename(self.mri3TPath[index]).split(".")[0]
        # MRI data is uint16 type (H,W,C)
        mri3TImg = np.load(self.mri3TPath[index])

        if self.resized is not None:
            mri3TImg = cv2.resize(mri3TImg,self.resized,interpolation=cv2.INTER_NEAREST)

        if mode == "RGB":
            mri3TImg = np.array(mri3TImg,dtype=np.float32).transpose(2,1,0)[1]
        else:
            print("Current function didn't finish yet!")

        clipValue = 500
        if self.clip:
            #NOTE: current clip value is 500 
            mri3TImg[mri3TImg>clipValue] = clipValue 

        # Normalization part
        mri3TTensor = torch.from_numpy(mri3TImg.astype(np.float32)/clipValue).view(1,mri3TImg.shape[0],mri3TImg.shape[1])

        return imgId, mri3TTensor

    def __len__(self):
        return len(self.mri3TPath)