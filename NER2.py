import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
import numpy as np


# Positional Encoding (same as before)
class PositionalEncoding(nn.Module):
    def __init__(self, d_model, max_len=5000):
        super(PositionalEncoding, self).__init__()
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-np.log(10000.0) / d_model))
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        pe = pe.unsqueeze(0).transpose(0, 1)
        self.register_buffer('pe', pe)

    def forward(self, x):
        x = x + self.pe[:x.size(0), :]
        return x


# Transformer Model for NER
class TransformerNERModel(nn.Module):
    def __init__(self, input_dim, model_dim, num_classes, num_heads, num_layers, dropout=0.1):
        super(TransformerNERModel, self).__init__()
        self.embedding = nn.Embedding(input_dim, model_dim)
        self.positional_encoding = PositionalEncoding(model_dim)
        encoder_layers = nn.TransformerEncoderLayer(d_model=model_dim, nhead=num_heads, dropout=dropout)
        self.transformer_encoder = nn.TransformerEncoder(encoder_layers, num_layers=num_layers)
        self.fc = nn.Linear(model_dim, num_classes)
        self.dropout = nn.Dropout(dropout)

    def forward(self, src, src_mask=None):
        src = self.embedding(src) * np.sqrt(self.embedding.embedding_dim)
        src = self.positional_encoding(src)
        transformer_output = self.transformer_encoder(src, src_mask)
        output = self.fc(self.dropout(transformer_output))
        return output


# NER Dataset
class NERDataset(Dataset):
    def __init__(self, texts, labels):
        self.texts = texts
        self.labels = labels

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        text = self.texts[idx]
        labels = self.labels[idx]

        text_ids = [ord(char) for char in text]  # Convert characters to ASCII
        label_ids = [label2id[label] for label in labels]

        return torch.tensor(text_ids, dtype=torch.long), torch.tensor(label_ids, dtype=torch.long)


# Custom collate function to pad sequences in each batch
def pad_sequences(batch):
    texts, labels = zip(*batch)

    max_len = max([len(seq) for seq in texts])

    padded_texts = [torch.cat([seq, torch.zeros(max_len - len(seq), dtype=torch.long)]) for seq in texts]
    padded_labels = [torch.cat([label, torch.zeros(max_len - len(label), dtype=torch.long)]) for label in labels]

    return torch.stack(padded_texts), torch.stack(padded_labels)


# Prepare Data Loader
def prepare_data(texts, labels, batch_size):
    dataset = NERDataset(texts, labels)
    data_loader = DataLoader(dataset, batch_size=batch_size, shuffle=True, collate_fn=pad_sequences)
    return data_loader


# Training Function
def train(model, data_loader, optimizer, criterion, device):
    model.train()
    total_loss = 0
    for texts, labels in data_loader:
        texts = texts.to(device)
        labels = labels.to(device)

        optimizer.zero_grad()

        outputs = model(texts)
        outputs = outputs.view(-1, outputs.shape[-1])
        labels = labels.view(-1)

        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        total_loss += loss.item()

    return total_loss / len(data_loader)


# Training Loop
def train_ner_model(train_texts, train_labels, val_texts, val_labels, label2id, num_classes, epochs=5, batch_size=32, max_len=128, lr=1e-4):
    input_dim = 256  # Max character ASCII value
    model_dim = 128
    num_heads = 8
    num_layers = 4
    dropout = 0.1

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    model = TransformerNERModel(input_dim, model_dim, num_classes, num_heads, num_layers, dropout).to(device)
    optimizer = optim.Adam(model.parameters(), lr=lr)
    criterion = nn.CrossEntropyLoss()

    train_loader = prepare_data(train_texts, train_labels, batch_size)
    val_loader = prepare_data(val_texts, val_labels, batch_size)

    for epoch in range(epochs):
        train_loss = train(model, train_loader, optimizer, criterion, device)
        # Add validation logic as needed

        print(f'Epoch {epoch + 1}/{epochs}, Train Loss: {train_loss:.4f}')

    return model


# Example usage
if __name__ == '__main__':
    # Example data (replace with your own dataset)
    train_texts = [
        ["John", "lives", "in", "New", "York", "City", "and", "works", "at", "Google"],
        ["Mary", "visited", "the", "Statue", "of", "Liberty", "in", "New", "York"]
    ]
    train_labels = [
        ["B-PER", "O", "O", "B-LOC", "I-LOC", "I-LOC", "O", "O", "O", "B-ORG"],
        ["B-PER", "O", "O", "B-LOC", "I-LOC", "I-LOC", "O", "B-LOC", "I-LOC"]
    ]

    val_texts = [["Tesla", "is", "based", "in", "Palo", "Alto"]]
    val_labels = [["B-ORG", "O", "O", "O", "B-LOC", "I-LOC"]]

    label2id = {"O": 0, "B-PER": 1, "I-PER": 2, "B-LOC": 3, "I-LOC": 4, "B-ORG": 5, "I-ORG": 6}
    num_classes = len(label2id)

    trained_model = train_ner_model(train_texts, train_labels, val_texts, val_labels, label2id, num_classes)
