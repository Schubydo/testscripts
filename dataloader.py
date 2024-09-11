import torch
from torch.utils.data import DataLoader, Dataset
from collections import defaultdict


# Build vocabulary from the dataset
def build_vocab(texts):
    word2idx = defaultdict(lambda: len(word2idx))
    word2idx["<PAD>"] = 0  # Padding token
    word2idx["<UNK>"] = 1  # Unknown token for words not in vocabulary

    for sentence in texts:
        for word in sentence:
            word2idx[word]
    
    return dict(word2idx)


# NER Dataset with vocab and label2id mapping
class NERDataset(Dataset):
    def __init__(self, texts, labels, vocab, label2id):
        self.texts = texts
        self.labels = labels
        self.vocab = vocab
        self.label2id = label2id

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        text = self.texts[idx]
        labels = self.labels[idx]

        # Convert each word in the text to its corresponding index in the vocabulary
        text_ids = [self.vocab.get(word, self.vocab["<UNK>"]) for word in text]
        label_ids = [self.label2id[label] for label in labels]

        return torch.tensor(text_ids, dtype=torch.long), torch.tensor(label_ids, dtype=torch.long)


# Custom collate function to pad sequences in each batch
def pad_sequences(batch):
    texts, labels = zip(*batch)

    max_len = max([len(seq) for seq in texts])

    padded_texts = [torch.cat([seq, torch.zeros(max_len - len(seq), dtype=torch.long)]) for seq in texts]
    padded_labels = [torch.cat([label, torch.zeros(max_len - len(label), dtype=torch.long)]) for label in labels]

    return torch.stack(padded_texts), torch.stack(padded_labels)


# Prepare Data Loader
def prepare_data(texts, labels, batch_size, vocab, label2id):
    dataset = NERDataset(texts, labels, vocab, label2id)
    data_loader = DataLoader(dataset, batch_size=batch_size, shuffle=True, collate_fn=pad_sequences)
    return data_loader


# Example usage:
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
vocab = build_vocab(train_texts + val_texts)

# Prepare data loaders
batch_size = 32
train_loader = prepare_data(train_texts, train_labels, batch_size, vocab, label2id)
val_loader = prepare_data(val_texts, val_labels, batch_size, vocab, label2id)
