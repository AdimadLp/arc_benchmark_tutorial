import torch
import matplotlib.pyplot as plt
import json
import os
import test_gpt2
import numpy as np
import seaborn as sns
import pandas as pd

def heatmap(graph_name, data, temperature, iteration=1):
    print(f"Visualizing example {iteration} of model {graph_name} with temperature {temperature}")

    # Create a grid of subplots
    figure, axis = plt.subplots(len(data), 2)
    # Iterate over each item in the data list
    for i in range(0, len(data)):

        # Get the input and output data
        input = data[i]['input']
        output = data[i]['output']

        # Create a heatmap of the input data
        axis[i, 0].imshow(input, cmap='rainbow')

        # Hide x-axis and y-axis ticks of the input heatmap
        axis[i, 0].set_xticks([])
        axis[i, 0].set_yticks([])

        # Create a heatmap of the output data
        axis[i, 1].imshow(output, cmap='rainbow')

        # Hide x-axis and y-axis ticks of the output heatmap
        axis[i, 1].set_xticks([])
        axis[i, 1].set_yticks([])

    # Save the output heatmap
    os.makedirs(f'plots/{graph_name}', exist_ok=True)
    plt.savefig(f'plots/{graph_name}/test_{temperature}_{iteration}.png')
    
    # Close the figure
    plt.close(figure)

def graph(model_name, learning_rate, stats):
    print(f"Visualizing stats of model {model_name}")

    # Create a list of epochs
    epochs = [stat['epoch'] for stat in stats]
    # Create a list of correct size tests
    correct_size_tests = [stat['correct_size_tests'] for stat in stats]
    # Create a list of visualizable tests
    visualizable_tests = [stat['visualizable_tests'] for stat in stats]

    # Create a figure and a set of subplots
    fig, ax = plt.subplots()

    # Plot the data for correct size tests
    ax.plot(epochs, correct_size_tests, color='blue', label='Correct size tests')

    # Plot the data for visualizable tests
    ax.plot(epochs, visualizable_tests, color='red', label='Visualizable tests')

    # Set the title
    ax.set_title("Correct Size vs Visualizable tests")

    # Set the x-axis label
    ax.set_xlabel("Epoch")

    # Set the y-axis label
    ax.set_ylabel("tests")

    # Add a legend
    ax.legend()

    # Save the figure
    os.makedirs(f'stats', exist_ok=True)
    plt.savefig(f'stats/{model_name}_{learning_rate}.png')

    # Close the figure
    plt.close(fig)

def avg_graph(model_name, learning_rate, stats):
    print(f"Visualizing stats of model {model_name}")

    # Create a list of epochs
    epochs = [stat['epoch'] for stat in stats]
    # Create a list of correct size tests
    correct_size_tests = [stat['correct_size_tests'] for stat in stats]
    # Create a list of visualizable tests
    visualizable_tests = [stat['visualizable_tests'] for stat in stats]
    # Calculate the difference between visualizable_tests and correct_size_tests
    difference = np.array(visualizable_tests) - np.array(correct_size_tests)

    def moving_average(data) :
        # Compute the window size as a percentage of the total number of data points
        window_size = int(len(data) * 0.1)
        if window_size == 0:
            window_size = 1
        return np.convolve(data, np.ones(window_size), 'valid') / window_size
    
    # Calculate the moving averages
    correct_size_tests_avg = moving_average(correct_size_tests)
    visualizable_tests_avg = moving_average(visualizable_tests)
    difference_avg = moving_average(difference)

    # Adjust epochs for moving average
    epochs_avg = epochs[len(epochs) - len(correct_size_tests_avg):]

    # Create a figure and a set of subplots
    fig, ax = plt.subplots()

    # Plot the moving averages
    ax.plot(epochs_avg, correct_size_tests_avg, color='blue', label='Correct size tests')
    ax.plot(epochs_avg, visualizable_tests_avg, color='red', label='Visualizable tests')
    ax.plot(epochs_avg, difference_avg, color='purple', label='Difference between correct size and visualizable tests')

    # Set the title
    ax.set_title("Moving Average of Model Performance Metrics Over Epochs")

    # Set the x-axis label
    ax.set_xlabel("Epoch")

    # Set the y-axis label
    ax.set_ylabel("tests")

    # Add a legend
    ax.legend()

    # Save the figure
    os.makedirs(f'stats', exist_ok=True)
    plt.savefig(f'stats/{model_name}_{learning_rate}_avg.png')

    # Close the figure
    plt.close(fig)