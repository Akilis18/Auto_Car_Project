import os
import glob
import numpy as np
import librosa

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader, random_split

# ---------------------------------------------------
# 1. Create Dataset，read and convert data to log-mel spectrogram
# ---------------------------------------------------
class SpeechCommandDataset(Dataset):
    """
    從指定資料夾中讀取 .wav 音檔，將其轉為 log-mel spectrogram，並作為 CNN 輸入。
    """
    def __init__(self, root_dir, sr, n_mels, win_length, hop_length, max_len):
        """
        Args:
            root_dir (str): 整體資料夾路徑
            sr (int): 取樣率 (sample rate)
            n_mels (int): mel filterbank 的頻率維度
            win_length (int): 每幀的取樣點數 (對應 STFT window size)
            hop_length (int): hop length
            max_len (int): 在時間維度的最大 frame 數，用於固定輸入長度
        """
        self.root_dir = root_dir
        self.classes = sorted([
            d for d in os.listdir(root_dir)
            if os.path.isdir(os.path.join(root_dir, d))
        ])

        self.filepaths = []
        self.labels = []

        self.sr = sr
        self.n_mels = n_mels
        self.win_length = win_length
        self.hop_length = hop_length
        self.max_len = max_len

        # 讀取每個類別資料夾裡的 wav 檔
        for label_idx, class_name in enumerate(self.classes):
            class_dir = os.path.join(root_dir, class_name)
            for wav_file in glob.glob(os.path.join(class_dir, "*.wav")):
                self.filepaths.append(wav_file)
                self.labels.append(label_idx)

    def __len__(self):
        return len(self.filepaths)

    def __getitem__(self, idx):
        """
        回傳 (log_mel, label)
        log_mel shape: (1, n_mels, max_len)
        """
        filepath = self.filepaths[idx]
        label = self.labels[idx]

        # 讀取音檔
        y, sr = librosa.load(filepath, sr=self.sr)

        # 計算 STFT -> Mel Spectrogram -> log scale
        #   n_fft 可以等於 win_length，讓 STFT 覆蓋整個 window。
        mel_spec = librosa.feature.melspectrogram(
            y=y,
            sr=sr,
            n_fft=self.win_length,
            win_length=self.win_length,
            hop_length=self.hop_length,
            n_mels=self.n_mels
        )
        log_mel_spec = librosa.power_to_db(mel_spec, ref=np.max)  # 轉成分貝尺度 (log scale)

        # log_mel_spec shape: (n_mels, time_frames)
        # 若 time_frames > max_len，就截斷；若不足，就補零
        if log_mel_spec.shape[1] > self.max_len:
            log_mel_spec = log_mel_spec[:, :self.max_len]
        else:
            pad_width = self.max_len - log_mel_spec.shape[1]
            log_mel_spec = np.pad(log_mel_spec, ((0, 0), (0, pad_width)), mode='constant')

        # 增加一個 channel 維度 (給 CNN 用)，shape 變成 (1, n_mels, max_len)
        log_mel_spec = np.expand_dims(log_mel_spec, axis=0)

        # 轉為 PyTorch tensor
        log_mel_spec_tensor = torch.from_numpy(log_mel_spec).float()
        label_tensor = torch.tensor(label, dtype=torch.long)

        return log_mel_spec_tensor, label_tensor


# ---------------------------------------------------
# 2. Define CNN model
# ---------------------------------------------------
class CNNClassifier(nn.Module):
    def __init__(self, num_classes, in_channels=1, n_mels=40, time_frames=80):
        """
        Args:
            num_classes (int): 類別數量
            in_channels (int): 輸入的頻道數（log-mel 是 1 channel）
            n_mels (int): 頻率維度大小
            time_frames (int): 時間維度大小 (max_len)
        """
        super(CNNClassifier, self).__init__()

        # 這裡示範一個簡單的 CNN 架構，可自行加深或加寬
        self.conv1 = nn.Conv2d(in_channels, 16, kernel_size=3, stride=1, padding=1)
        self.bn1 = nn.BatchNorm2d(16)
        self.pool1 = nn.MaxPool2d(kernel_size=2, stride=2)

        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, stride=1, padding=1)
        self.bn2 = nn.BatchNorm2d(32)
        self.pool2 = nn.MaxPool2d(kernel_size=2, stride=2)

        # 計算通過兩次 pooling 之後的特徵圖大小
        #   初始: (batch, 1, n_mels, time_frames)
        #   1st pool -> (batch, 16, n_mels/2, time_frames/2)
        #   2nd pool -> (batch, 32, n_mels/4, time_frames/4)
        reduced_mels = n_mels // 4
        reduced_time = time_frames // 4

        # 全連接層
        self.fc1 = nn.Linear(32 * reduced_mels * reduced_time, 64)
        self.fc2 = nn.Linear(64, num_classes)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.3)

    def forward(self, x):
        # x shape: (batch_size, 1, n_mels, time_frames)
        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu(x)
        x = self.pool1(x)

        x = self.conv2(x)
        x = self.bn2(x)
        x = self.relu(x)
        x = self.pool2(x)

        # 攤平
        x = x.view(x.size(0), -1)

        x = self.dropout(self.relu(self.fc1(x)))
        x = self.fc2(x)
        return x


# ---------------------------------------------------
# 3.  Train and Evaluate
# ---------------------------------------------------
def train_one_epoch(model, loader, criterion, optimizer, device):
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0

    for inputs, labels in loader:
        inputs, labels = inputs.to(device), labels.to(device)

        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        running_loss += loss.item() * inputs.size(0)
        _, preds = torch.max(outputs, 1)
        correct += (preds == labels).sum().item()
        total += labels.size(0)

    epoch_loss = running_loss / total
    epoch_acc = 100.0 * correct / total
    return epoch_loss, epoch_acc


def evaluate(model, loader, criterion, device):
    model.eval()
    running_loss = 0.0
    correct = 0
    total = 0

    with torch.no_grad():
        for inputs, labels in loader:
            inputs, labels = inputs.to(device), labels.to(device)
            outputs = model(inputs)
            loss = criterion(outputs, labels)

            running_loss += loss.item() * inputs.size(0)
            _, preds = torch.max(outputs, 1)
            correct += (preds == labels).sum().item()
            total += labels.size(0)

    epoch_loss = running_loss / total
    epoch_acc = 100.0 * correct / total
    return epoch_loss, epoch_acc


def main():
    # Parameters setting
    # dataset_path = "/content/drive/MyDrive/samples/dataset"    # Data path
    dataset_path = "./dataset"
    sr = 44100
    n_mels = 40
    win_length = 400
    hop_length = 160
    max_len = 256
    batch_size = 16
    num_epochs = 25
    learning_rate = 1e-3
    test_ratio = 0.2

    # Create Dataset
    full_dataset = SpeechCommandDataset(
        root_dir=dataset_path,
        sr=sr,
        n_mels=n_mels,
        win_length=win_length,
        hop_length=hop_length,
        max_len=max_len
    )

    num_classes = len(full_dataset.classes)
    print("資料類別:", full_dataset.classes)
    print("總資料筆數:", len(full_dataset))

    # Split train / test
    test_size = int(len(full_dataset) * test_ratio)
    train_size = len(full_dataset) - test_size
    train_dataset, test_dataset = random_split(full_dataset, [train_size, test_size])

    # Create DataLoader
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    test_loader  = DataLoader(test_dataset,  batch_size=batch_size, shuffle=False)

    # Create CNN 模型
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = CNNClassifier(num_classes=num_classes, in_channels=1, n_mels=n_mels, time_frames=max_len)
    model.to(device)

    # Define loss function and optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

    # Start training
    for epoch in range(num_epochs):
        train_loss, train_acc = train_one_epoch(model, train_loader, criterion, optimizer, device)
        test_loss, test_acc = evaluate(model, test_loader, criterion, device)

        print(f"[Epoch {epoch+1}/{num_epochs}] "
              f"Train Loss: {train_loss:.4f}, Train Acc: {train_acc:.2f}% | "
              f"Test Loss: {test_loss:.4f}, Test Acc: {test_acc:.2f}%")

    # Save model parameters
    torch.save(model.state_dict(), "cnn_logmel_model.pth")
    print("訓練完成，模型已儲存為 cnn_logmel_model.pth")


if __name__ == "__main__":
    main()
