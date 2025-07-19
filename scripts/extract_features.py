import os #fiel and fodler operations 
import torch # core PyTorch library 
import numpy as np #hold arrays on the CPU and save them later on 
from torchvision import models, transforms # Pretrained CNN like ResNet; image preprocessing steps (resize, normalise, etc) 
from PIL import Image #load JPEG/PNG files 
from tqdm import tqdm #progress bar wrapper 

# Set up the pre‑trained model ResNet50
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
resnet = models.resnet50(pretrained=True) #pre-trained 50-layer ResNet trained on ImageNet 
resnet.fc = torch.nn.Identity()   # replace final fully‑connected layer; classification layer 
resnet = resnet.to(device).eval() #move to GPU/CPU to set inference mode; content feature extraction 

# Define the image transforms to match ResNet’s training
tfm = transforms.Compose([
    transforms.Resize((224,224)), #resize to 224x224 
    transforms.ToTensor(), #convert to PyTorch tensor in the shape of 3, 224, 224 
    transforms.Normalize( #normalsie each rgb channel 
      mean=[0.485, 0.456, 0.406],
      std =[0.229, 0.224, 0.225]
    )
])

def extract_split(split_dir):
    X, y = [], []
    # classes in folder names
    for cls_idx, cls in enumerate(["benign","malignant"]): #benign - label 0; malignant - label 1 
        cls_folder = os.path.join(split_dir, cls)
        for fname in os.listdir(cls_folder):
            path = os.path.join(cls_folder, fname)
            img = Image.open(path).convert("RGB")
            
            #preprocess and add batch dimension 
            inp = tfm(img).unsqueeze(0).to(device)   # shape: [1,3,224,224] [batch, 2048, H, W] 
            # 224 x 224 image size 
            # 3 - red, green, blue colour channels 
            # 1 - a batch - one picture 
            # shrink the photo to 224x224 colour square, wrap in a one-picture parcel 
            
            #forward pass without computing gradients because we are just extracting the features
            # 2048 number that are important about the image - ResNet feature vector by default 
            with torch.no_grad():
                feat = resnet(inp)  # shape: [1, 2048] - ome picture, 2048 numbers 
                feat= feat.cpu().numpy().squeeze()  # shape: [2048] 2048-dimensional vector  
            X.append(feat) #features 
            y.append(cls_idx) #label 0 or 1 
    return np.stack(X), np.array(y) #collect all feature vectors into x and lables into y 

if __name__ == "__main__":
    # point these at your folders
    train_dir = "data/melanoma_cancer_dataset/train"
    test_dir  = "data/melanoma_cancer_dataset/test"

    print("Extracting train features…")
    X_train, y_train = extract_split(train_dir)
    print("Extracting test features…")
    X_test,  y_test  = extract_split(test_dir)

    # Save everything in zip-like folder in NumPy arrays and compress to save space 
    np.savez_compressed(
      "data/cnn_features.npz",
      X_train=X_train, y_train=y_train,
      X_test =X_test,  y_test =y_test
    )
    print("Saved features to data/cnn_features.npz")
