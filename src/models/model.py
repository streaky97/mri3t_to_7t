import torch
from torch import nn
from diffusers import UNet2DModel

class ConditionedUnet(nn.Module):
  def __init__(self,cond_emb_size=1):
    super().__init__()
    
    self.model = UNet2DModel(
        sample_size=28,           
        in_channels=1 + cond_emb_size, 
        out_channels=1,           
        layers_per_block=2,       
        block_out_channels=(32, 64, 64), 
        down_block_types=( 
            "DownBlock2D",        
            "AttnDownBlock2D",    
            "AttnDownBlock2D",
        ), 
        up_block_types=(
            "AttnUpBlock2D", 
            "AttnUpBlock2D",     
            "UpBlock2D",         
          ),
    )

  def forward(self, x, t, img_cond):
    bs, ch, w, h = x.shape

    net_input = torch.cat((x, img_cond), 1)

    return self.model(net_input, t).sample