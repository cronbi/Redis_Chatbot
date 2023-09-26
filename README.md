# Chatbot Project README

## Overview
This chatbot project utilizes Redis as a backend data store to enable real-time messaging and user interactions. The chatbot supports a variety of commands and features, including weather updates, fun facts, user identification, and messaging in different channels.

## Table of Contents
- [Setup](#setup)
- [Usage](#usage)
- [Monitoring](#monitoring)
- [Example](#example)

## Setup

### Prerequisites
- Docker: Ensure you have Docker installed and running on your machine.
- Python: Make sure you have Python 3.x installed.

### Running the Chatbot
1. Clone this repository to your local machine: `git clone <repository_url>`

2. Navigate to the project directory: `cd <chatbot-project-path>`

3. Build and start the Docker containers: `docker-compose up -d`

4. Access the chatbot by running the following command in another terminal: `docker-compose exec <you-python-app-name> bash` `python <mp1.py>`

## Usage

### Main Menu
When you start the chatbot, you'll be presented with a main menu that offers several options. Here's how to use them:

- `1: Identify yourself`: Initialize user details.
- `2: Join a channel`: Join a channel and view previous messages.
- `3: Leave a channel`: Leave a previously joined channel.
- `4: Send a message to a channel`: Send a message to a channel.
- `5: Get info about a user`: Retrieve user information.
- `6: Exit`: Exit the chatbot.

### Chat Channels
- After joining a channel, you can send and receive messages within that channel.
- If previous messages exist in the channel, they will be displayed when you join.

### Special Commands
The chatbot supports special commands:
- `!help`: List available commands.
- `!weather`: Get a weather update for a city of choice.
- `!fact`: Receive a random fun fact.
- `!whoami`: Display user information.

## Monitoring

You can monitor interactions in real-time. Here's how to do it:

1. Open a new terminal.

2. Run the following command to start monitoring Redis interactions: `redis-cli monitor`

3. In your chatbot terminal, initiate interactions (e.g., join a channel, send messages).

4. Observe the real-time output in the Redis monitor terminal. Screenshot the output for at least three different user inputs to your bot.

## Example

Below are a few examples of how to run this chatbot:

![Example 1](https://imgur.com/a/9m9revD)

![Example 2](https://imgur.com/a/8YrbZeq)

![Example 3](https://imgur.com/a/rMjialb)

![Example 4](https://i.imgur.com/4SOIhix)



