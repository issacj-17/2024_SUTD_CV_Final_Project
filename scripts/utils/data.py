import os
import torch
from torch.utils.data import Dataset
from PIL import Image
import matplotlib.pyplot as plt
from torchvision import transforms

class DriverDrowsinessDataset(Dataset):
    def __init__(self, root_dir, split='train', transform=None, seq_len=16, padding_value=0.0, default_img_size=224):
        self.root_dir = root_dir
        self.split = split
        self.transform = transform
        self.seq_len = seq_len
        self.padding_value = padding_value
        self.sequences = []
        self.labels = []
        self.default_size = default_img_size

        if split not in ['train', 'val', 'test']:
            raise ValueError(f"Invalid split: {split}. Must be one of 'train', 'val', 'test'.")

        split_dir = os.path.join(root_dir, split)
        
        for label in ['pos', 'neg']:
            label_dir = os.path.join(split_dir, label)
            if not os.path.exists(label_dir):
                print(f"Warning: Directory {label_dir} not found.")
                continue
            
            for sequence in os.listdir(label_dir):
                sequence_dir = os.path.join(label_dir, sequence)
                images = sorted([
                    img for img in os.listdir(sequence_dir)
                    if img.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff'))
                ])
                
                stride = self.seq_len // 2
                for i in range(0, len(images), stride):
                    seq = images[i:i + self.seq_len]
                    if len(seq) == self.seq_len:
                        self.sequences.append([os.path.join(sequence_dir, img) for img in seq])
                        self.labels.append(1 if label == 'pos' else 0)
                    else:
                        padded_seq = seq + [None] * (self.seq_len - len(seq))
                        self.sequences.append([os.path.join(sequence_dir, img) if img is not None else None for img in padded_seq])
                        self.labels.append(1 if label == 'pos' else 0)

    def __len__(self):
        return len(self.sequences)

    def _validate_transformed_data(self, images):
        if torch.isnan(images).any() or torch.isinf(images).any():
            raise ValueError("NaN or Inf detected after transformations.")
    
    def __getitem__(self, idx):
        sequence = self.sequences[idx]
        label = self.labels[idx]
        images = []
        mask = []
        
        # Load all images first
        for img_path in sequence:
            if img_path is not None:
                try:
                    image = Image.open(img_path).convert('RGB')
                    images.append(image)
                    mask.append(1)
                except Exception as e:
                    print(f"Error loading image {img_path}: {e}")
                    dummy_image = Image.new('RGB', (self.default_size, self.default_size), color=0)
                    images.append(dummy_image)
                    mask.append(0)
            else:
                dummy_image = Image.new('RGB', (self.default_size, self.default_size), color=0)
                images.append(dummy_image)
                mask.append(0)

        if self.transform and self.split == 'train':
            # Use index to create varying but deterministic transformations
            random_state = torch.get_rng_state()
            torch.manual_seed(idx)
            
            transformed_images = []
            for image in images:
                torch.set_rng_state(random_state)
                transformed_images.append(self.transform(image))
            
            images = transformed_images
        elif self.transform:
            images = [self.transform(image) for image in images]
        else:
            to_tensor = transforms.ToTensor()
            images = [to_tensor(image) for image in images]

        images = torch.stack(images)
        self._validate_transformed_data(images)
        mask = torch.tensor(mask, dtype=torch.bool)
        return images, mask, label


def visualize_sequence(dataset, idx, rows=2):
    """
    Visualizes a sequence of images from the dataset with their masks.
    
    Args:
        dataset: DriverDrowsinessDataset instance
        idx: Index of sequence to visualize
        rows: Number of rows for subplot grid
    """
    images, mask, label = dataset[idx]
    cols = dataset.seq_len // rows
    
    # Convert tensors back to displayable format
    if isinstance(images, torch.Tensor):
        denorm = transforms.Normalize(
            mean=[-m/s for m, s in zip([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])],
            std=[1/s for s in [0.229, 0.224, 0.225]]
        )
        images = denorm(images).clip(0, 1)
    
    plt.figure(figsize=(20, 8))
    for i in range(dataset.seq_len):
        plt.subplot(rows, cols, i + 1)
        plt.imshow(images[i].permute(1, 2, 0))
        border_color = 'green' if mask[i] else 'red'
        plt.gca().spines['bottom'].set_color(border_color)
        plt.gca().spines['top'].set_color(border_color)
        plt.gca().spines['left'].set_color(border_color)
        plt.gca().spines['right'].set_color(border_color)
        plt.title(f'Frame {i}\nValid: {mask[i].item()}')
        plt.axis('off')
    
    plt.suptitle(f'Sequence {idx} - Label: {"Drowsy" if label == 1 else "Alert"}')
    plt.tight_layout()
    plt.show()