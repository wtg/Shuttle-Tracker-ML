# Thanks to guide:
# https://www.kaggle.com/code/shrutimechlearn/pytorch-custom-model-step-by-step#6.-Instantiating-the-Custom-Model

import torch 
import torch.nn as nn

Input_StartTime = []
Input_DayOfWeek = []
Input_SecondsInDay = []
Input_DeltaTime = []
Output_FinalTime = []

f = open(input("Datafile: "), "r")
for line in f:
    line = line.replace("\n","")
    Input_StartTime.append(float(line.split(",")[0]))
    Input_DayOfWeek.append(float(line.split(",")[1]))
    Input_SecondsInDay.append(float(line.split(",")[2]))
    Input_DeltaTime.append(float(line.split(",")[3]))
    Output_FinalTime.append(float(line.split(",")[4]))
f.close()

Inputs = torch.tensor([[float(Input_StartTime[i]), float(Input_DayOfWeek[i]), float(Input_SecondsInDay[i]), float(Input_DeltaTime[i])] for i in range(len(Input_StartTime))])
Outputs = torch.tensor(Output_FinalTime)

class SimpleModel(nn.Module):
    def __init__(self):
        super(SimpleModel, self).__init__()
        self.fc = nn.Linear(4, 1)

    def forward(self, x):
        x = self.fc(x)
        return x

model = SimpleModel()
loss_func = nn.MSELoss()

nn_model = SimpleModel()
nn_model, nn_model.state_dict()
nn_model.to("cpu") #need "cuda"
optimizer = torch.optim.SGD(params= nn_model.parameters(), lr= 0.001)

for epoch in range(200):
    model.train()
    pred = model(Inputs)
    loss = loss_func(pred, Outputs)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    print("Epoch #" + str(epoch) + ": " + str(loss.item()))