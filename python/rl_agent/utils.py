import numpy as np
import torch
from torch.autograd import Variable
from collections import namedtuple

Transition = namedtuple('Transition',
                        ('state', 'action_logit', 'next_state', 'reward', 'value'))

State = namedtuple('State', ('visual', 'instruction'))

def mse_loss(predicted, target):
    return torch.sum((predicted - target) ** 2)

class ReplayMemory(object):

    def __init__(self, capacity):
        self.capacity = capacity
        self.memory = []

    def push(self, *args):
        self.memory.append(Transition(*args))
        
        while len(self.memory) > self.capacity:
            self.memory.pop(0)

    def sample(self, batch_size):
        start_index = np.random.randint(0, len(self.memory) - batch_size)
        return self.memory[start_index : start_index + batch_size]

    def __len__(self):
        return(len(self.memory))
    
    def full(self):
        if (len(self.memory) >= self.capacity):
            return True
        return False
    
    def clear(self):
        self.memory = []
    
class FakeEnvironment(object):
    def __init__(self):
        pass
    
    def reset(self):
        return self.generate_state()
    
    def step(self, action):
        return self.generate_state(), 2, False, 1
        
    def generate_state(self):
        vision = Variable(torch.randn(1, 3, 84, 84))
        instruction = Variable(torch.LongTensor(np.random.randint(1, 100, size=(1, 10))))
        
        return State(vision, instruction)