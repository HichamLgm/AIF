
import argparse
import torch
import torchvision.transforms as transforms
from flask import Flask, jsonify, request
from PIL import Image
import io
from model import MNISTNet

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

app = Flask(__name__)


parser = argparse.ArgumentParser()
parser.add_argument('--model_path', type=str, default = 
                    '/home/n7student/Bureau/cours/2A MODIA/S2/Infra IA/TP/TP01/AIF/developpement/MNIST/mnist_net.pth'
                    , help='PATH to model')
args = parser.parse_args()
model_path = args.model_path


model = MNISTNet().to(device)
# Load the model
model.load_state_dict(torch.load(model_path))
model.eval()

transform = transforms.Compose([
    transforms.Resize((28, 28)),
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])

@app.route('/predict', methods=['POST'])
def predict():
    img_binary = request.data
    img_pil = Image.open(io.BytesIO(img_binary))

    # Transform the PIL image
    tensor = transform(img_pil).to(device)
    tensor = tensor.unsqueeze(0)  # Add batch dimension

    # Make prediction
    with torch.no_grad():
        outputs = model(tensor)
        _, predicted = outputs.max(1)

    return jsonify({"prediction": int(predicted[0])})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)