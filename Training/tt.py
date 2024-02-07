import argparse
import math
import os
import random
import sys
import time
from copy import deepcopy
from datetime import datetime
from pathlib import Path

import numpy as np
import torch
import torch.distributed as dist
import torch.nn as nn
import yaml
from torch.optim import lr_scheduler
from tqdm import tqdm

FILE = Path(__file__).resolve()
ROOT = FILE.parents[1]  # YOLOv5 root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative

import torch.nn.functional as F

import segment.val as validate  # for end-of-epoch mAP
from models.experimental import attempt_load
from models.yolo import SegmentationModel
from utils.autoanchor import check_anchors
from utils.autobatch import check_train_batch_size
from utils.callbacks import Callbacks
from utils.downloads import attempt_download, is_url
from utils.general import (LOGGER, check_amp, check_dataset, check_file, check_git_status, check_img_size,
                           check_requirements, check_suffix, check_yaml, colorstr, get_latest_run, increment_path,
                           init_seeds, intersect_dicts, labels_to_class_weights, labels_to_image_weights, one_cycle,
                           print_args, print_mutation, strip_optimizer, yaml_save)
from utils.loggers import GenericLogger
from utils.plots import plot_evolve, plot_labels
from utils.segment.dataloaders import create_dataloader
from utils.segment.loss import ComputeLoss
from utils.segment.metrics import KEYS, fitness
from utils.segment.plots import plot_images_and_masks, plot_results_with_masks
from utils.torch_utils import (EarlyStopping, ModelEMA, de_parallel, select_device, smart_DDP, smart_optimizer,
                               smart_resume, torch_distributed_zero_first)

model = Model(opt.cfg).to(device)
x = torch.randn(1, 3, 640, 640).to(device)
script_model = torch.jit.trace(model, x)
script_model.save("m.pt")