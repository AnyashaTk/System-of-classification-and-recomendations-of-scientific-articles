import torch
import transformers
from torch.utils.data import Dataset, DataLoader
from transformers import RobertaModel, RobertaTokenizer
import json
import os
import pandas as pd
from torch import cuda
device = 'cuda:0' if cuda.is_available() else 'cpu'
print(device)


torch.manual_seed(42)
torch.cuda.manual_seed(42)
torch.backends.cudnn.deterministic = True


EPOCHS = 5
MAX_LEN = 256
BATCH_SIZE = 4
LEARNING_RATE = 1e-05
BEST_LOSS = 99.99
# загружаем токенизатор роберты
tokenizer = RobertaTokenizer.from_pretrained('roberta-base', truncation=True, do_lower_case=True)

# параметры обучения
train_params = {'batch_size': BATCH_SIZE,
                'shuffle': True,
                'num_workers': 0
                }

test_params = {'batch_size': BATCH_SIZE,
               'shuffle': True,
               'num_workers': 0
               }
