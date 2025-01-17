import torch.nn as nn
import torch


class Content_Loss(nn.Module):

    def __init__(self, target):
        super(Content_Loss, self).__init__()
        self.target = target.detach()
        self.criterion = nn.MSELoss()

    def forward(self, input):
        self.loss = self.criterion(input , self.target)
        out = input.clone()
        return out

    def backward(self, retain_graph=True):
        self.loss.backward(retain_graph=True)
        return self.loss



class Gram(nn.Module):
    def __init__(self):
        super(Gram, self).__init__()

    def forward(self, input):
        a, b, c, d = input.size()
        feature = input.view(a * b, c * d)
        gram = torch.mm(feature, feature.t())
        gram /= (a * b * c * d)
        return gram


class Style_Loss(nn.Module):
    def __init__(self, target):
        super(Style_Loss, self).__init__()
        self.target = target.detach()
        self.gram = Gram()
        self.criterion = nn.MSELoss()

        
    def forward(self, input):
        G = self.gram(input)
        self.loss = self.criterion(G, self.target)
        out = input.clone()
        return out

    
    def backward(self, retain_graph=True):
        self.loss.backward(retain_graph=True)
        return self.loss