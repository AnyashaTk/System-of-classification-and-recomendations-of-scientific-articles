from constants import *

from utils import *
from dataset import DatasetAbstract
from model import RobertaClass


data = load_json_data()

print(data['label'].unique().shape, type(data['label'].unique()))

labels = data['label'].unique()

# делим датасет на тренировочный и тестовый
train_size = 0.7
train_data = data.sample(frac=train_size, random_state=200)
val_data = data.drop(train_data.index).reset_index(drop=True)
train_data = train_data.reset_index(drop=True)

# выводим информацию о датасетах
print("FULL Dataset: {}".format(data.shape))
print("TRAIN Dataset: {}".format(train_data.shape))
print("TEST Dataset: {}".format(val_data.shape))

# токенизируем датасет
training_set = DatasetAbstract(train_data, tokenizer, MAX_LEN)
testing_set = DatasetAbstract(val_data, tokenizer, MAX_LEN)


train_loader = DataLoader(training_set, **train_params)
val_loader = DataLoader(testing_set, **test_params)

model = RobertaClass()
model.to(device)


criterion = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(params=model.parameters(), lr=LEARNING_RATE)


train_loss = []
val_loss = []
train_acc = []
val_acc = []

for epoch in range(EPOCHS):
    print(f"Epoch {epoch + 1} of {EPOCHS}")
    train_epoch_accuracy, train_epoch_loss = train_model(model, train_loader, criterion, True, optimizer)
    val_epoch_accuracy, val_epoch_loss = train_model(model, val_loader, criterion, False)

    train_acc.append(train_epoch_accuracy)
    val_acc.append(val_epoch_accuracy)
    train_loss.append(train_epoch_loss)
    val_loss.append(val_epoch_loss)

    print(f"Train Acc: {train_epoch_accuracy:.4f}")
    print(f"Train Loss: {train_epoch_loss:.4f}")
    print(f'Val Acc: {val_epoch_accuracy:.4f}')
    print(f'Val Loss: {val_epoch_loss:.4f}')


