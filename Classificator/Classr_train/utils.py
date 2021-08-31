from tqdm import tqdm

from constants import *


def load_json_data():
    os.chdir("/home/sparrow/PycharmProjects/SCRSA/data/")
    data = pd.DataFrame(columns=['title', 'abstract', 'label'])
    count = 0
    f = open('arxiv-metadata.json', 'r')
    for line in f:
        json_dict = json.loads(line)
        row = pd.Series([json_dict['title'], json_dict['abstract'], json_dict['categories']], index=data.columns)
        data = data.append(row, ignore_index=True)
        count += 1
        if count == 100:
            break
    return data


def train_model(model, loader, criterion, mode_train=True, optimizer=None):
    if mode_train:
        print('Training')
        model.train()
    else:
        print('Validating')
        model.eval()
    epoch_accuracy = 0.0
    epoch_loss = 0.0
    counter = 0

    for _, data in tqdm(enumerate(loader)):
        counter += 1
        ids = data['ids'].to(device, dtype=torch.long)
        mask = data['mask'].to(device, dtype=torch.long)
        token_type_ids = data['token_type_ids'].to(device, dtype=torch.long)
        targets = data['targets'].to(device, dtype=torch.long)

        outputs = model(ids, mask, token_type_ids)
        #print('Targets:\n', targets)
        #print('Outputs:\n', outputs)
        loss = criterion(outputs, targets)
        epoch_loss += loss.item()
        big_val, big_idx = torch.max(outputs.data, dim=1)
        # n_correct += calcuate_accuracy(big_idx, targets)

        if mode_train:
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

    return epoch_accuracy / counter, epoch_loss / counter
