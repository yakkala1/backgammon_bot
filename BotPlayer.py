import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import numpy as np
from backgammon import Backgammon

class NeuralNetwork(nn.Module):
    """
    Responsible for approximating the value function using a neural network.
    """

    def __init__(self, input_dim, hidden_units):
        super(NeuralNetwork, self).__init__()
        self.hidden = nn.Linear(input_dim, hidden_units)
        self.output = nn.Linear(hidden_units, 1)

    def forward(self, x):
        x = F.relu(self.hidden(x))
        x = self.output(x)
        return x

class BotPlayer:
    """
    Responsible for the behavior of the bot player, including action selection and weight updates using TD learning.
    """

    def __init__(self, exploration_rate, input_dim, hidden_units, learning_rate, gamma):
        # Define properties and initialization logic for the bot player
        self.exploration_rate = exploration_rate
        self.gamma = gamma
        self.neural_network = NeuralNetwork(input_dim, hidden_units)
        self.optimizer = optim.SGD(self.neural_network.parameters(), lr=learning_rate)
        self.replay_memory = []

    def select_action(self, state: BackGammon, available_actions):
        # Select an action using exploration and exploitation strategies
        if np.random.rand() < self.exploration_rate:
            # Exploration: Choose a random action from the available actions
            chosen_action = np.random.choice(available_actions)
        else:
            # Exploitation: Simulate each available action, obtain predicted probabilities for resulting next states, and select action with maximum probability
            max_prob = -np.inf
            chosen_action = None

            for action in available_actions:
                # Create a deep copy of the current state
                next_state = copy.deepcopy(state)
                
                # Execute the action on the copied state
                next_state.execute_play(current_player, action)
                
                # Convert the next_state to tensor
                next_state_tensor = torch.Tensor(self._reshape_state(next_state))
                
                # Obtain the predicted probabilities for the next_state using the neural network
                prob = self.neural_network(next_state_tensor).item()
                
                # Update the chosen action if the probability is higher
                if prob > max_prob:
                    max_prob = prob
                    chosen_action = action

        return chosen_action

    def update_weights(self, state, reward, next_state):
        # Store the current state, reward, and next state in replay memory
        self.replay_memory.append((state, reward, next_state))

    def train(self):
        if len(self.replay_memory) == 0:
            return

        # Shuffle the replay memory to process steps in random order
        np.random.shuffle(self.replay_memory)

        # Extract states, rewards, and next states from replay memory
        states, rewards, next_states = zip(*self.replay_memory)

        states = torch.Tensor(states)
        next_states = torch.Tensor(next_states)

        # Compute the predicted values for the states and next states
        values = self.neural_network(states)
        values_next = self.neural_network(next_states)

        # Compute the TD targets using the TD learning update rule
        targets = torch.Tensor(rewards)
        targets += self.gamma * values_next

        # Compute the loss and perform gradient descent
        loss = F.mse_loss(values, targets)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        # Clear the replay memory
        self.replay_memory = []

    def _reshape_state(self, state):
        

