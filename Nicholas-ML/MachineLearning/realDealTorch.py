import math
import torch
import torch.nn as nn
import torch.optim as optim
from OtherFunctions import read_file
from OtherFunctions import Get_All_Points

AllData = read_file("DataTest.csv")#input("Input File: "))
IntPoints = Get_All_Points()

# Define custom loss function
def custom_loss(output, target):
    # Define your custom loss calculation here

    # print(output[0].item())
    # print(output)


    for i in range(len(output)):
        Output_int = int(output[i].item())
        Target_int = int(target[i].item())

        temp_target_coords = [IntPoints[Target_int][0], IntPoints[Target_int][1]]
        
        LengthFromValidNum = abs(Output_int) if (Output_int < 0) else abs(len(IntPoints)-Output_int)
        temp_output_coords = [100.0+LengthFromValidNum, 100.0+LengthFromValidNum]
        # if (Output_int >= 0 and Output_int < len(IntPoints)):
        #     temp_output_coords = [IntPoints[Output_int][0], IntPoints[Output_int][1]]
        
        tensor_output = torch.tensor(temp_output_coords, requires_grad=True)
        tensor_target = torch.tensor(temp_target_coords, requires_grad=True)

        temp_loss = torch.mean(torch.abs(tensor_output - tensor_target))
    #     output[i] = temp_loss.item()
    #     target[i] = 0

    loss = torch.mean(torch.abs(output - target))  # Example loss function (mean absolute error)
    # print(loss)
    # print(loss.item())
    print(loss)
    return loss

# Define your model
class CustomModel(nn.Module):
    def __init__(self):
        super(CustomModel, self).__init__()
        self.fc1 = nn.Linear(3, 64)  # 3 input features, 64 output features
        self.fc2 = nn.Linear(64, 1)   # 64 input features, 1 output feature

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x

# Example data
# input_data = torch.randn(2, 3)  # 100 samples, 3 features
# target_data = torch.randn(2, 1)  # 100 samples, 1 output
input_data = torch.tensor([[AllData[1][i], AllData[2][i], AllData[4][i]] for i in range(len(AllData[1]))], dtype=torch.float)
target_data = torch.tensor([[elem] for elem in AllData[3]], dtype=torch.float)

# Initialize model
model = CustomModel()

# Define optimizer
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Training loop
num_epochs = 2
for epoch in range(num_epochs):
    # Forward pass
    output = model(input_data)

    # Compute loss
    loss = custom_loss(output, target_data)

    # Backward pass
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    # Print progress
    if (epoch+1) % 100 == 0:
        print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}')
