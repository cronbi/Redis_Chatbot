import redis
import json
import random

class Chatbot:
    def __init__(self, host='my-redis', port=6379): # Default host and port
        self.client = redis.StrictRedis(host=host, port=port) # Connect to Redis
        self.pubsub = self.client.pubsub() # Create a pubsub object
        self.username = None 

    def introduce(self):
        # Provide an introduction and list of commands
        intro = """ 
        Hello! I'm your friendly Redis chatbot.
        Here are the commands you can use:
        !help: List of commands
        !weather: Weather update
        !fact: Random fun fact
        !whoami: Your user information
        """
        print(intro)

    def identify(self, username, age, gender, location):
        # Store user details in Redis
        user_key = "user:{}".format(username) # Create user key
        self.client.hset(user_key, mapping={ # Set user details
            "name": username, 
            "age": age,
            "gender":gender,
            "location": location
        })
        self.username = username # Set username
        print("You have been identified as {}".format(username))
        

    #def join_channel(self, channel):
        # # Join a channel
        # channel_key = "channel:{}".format(channel)
        # self.client.sadd(channel_key, self.username) # Add user to channel
        # self.pubsub.subscribe(channel_key) # Subscribe to channel
        # print("You have joined the channel {}".format(channel))

        # for message in self.pubsub.listen():
        #     if message['type'] == 'message':
        #         print(f"[{channel}] {message['data'].decode('utf-8')}")
    
    def join_channel(self, channel):
        # Join a channel
        channel_key = "channel:{}".format(channel)
        self.client.sadd(channel_key + ":members", self.username) # Add user to channel members set
        self.pubsub.subscribe(channel_key) # Subscribe to channel
        print("You have joined the channel {}".format(channel))

        # Retrieve and display existing messages
        channel_messages = self.client.lrange(channel_key + ":messages", 0, -1)
        if channel_messages:
            print("Channel History:")
            for message in channel_messages:
                message_data = json.loads(message.decode("utf-8"))
                print(f"Message from {message_data['username']} in {channel}: {message_data['message']}")
        else:
            print("No previous messages in this channel")

    def leave_channel(self, channel):
        # Leave a channel
        channels_key = f"channels:{self.username}" # Get user's channels
        self.client.srem(channels_key, channel) # Remove channel from user's channels
        print(f"You have left the {channel} channel")

    def send_message(self, channel, message):
    # Send a message to a channel
        message_obj = {
            "username": self.username,
            "message": message
        } # Create message object
        
        channel_key = "channel:{}".format(channel)
        
        self.client.lpush(channel_key + ":messages", json.dumps(message_obj)) # Add message to the beginning of the list
        self.client.publish(channel, "New message available") # Publish message to channel
        print(f"Message sent to {channel}")

        
    # def read_message(self, channel):
    #     # Read messages from a channel
    #     # message = self.pubsub.get_message() # Get message from channel
    #     # if message:
    #     #     print(message['data']) # Print message
    #     # else:
    #     #     print("No messages yet")

    #     for item in self.pubsub.listen(): # Listen for messages
    #         if item['type'] == 'message': # If message received
    #             message_data = json.loads(item['data']) # Load message data
    #             print(f"Message from {message_data['from']} in {channel}: {message_data['message']}") 
        
    def weather_city(self, city):
        # Get mock weather update for a city
        cities = {
            "Nashville": {"temperature": 75, "condition": "sunny"},
            "New York": {"temperature": 60, "condition": "cloudy"},
            "San Francisco": {"temperature": 55, "condition": "rainy"},
            "London": {"temperature": 50, "condition": "cloudy"},
        } 
        if city in cities:
            weather = cities[city] # Get weather for city
            print(f"The weather in {city} is {weather['temperature']} degrees and {weather['condition']}")
        else:
            print("City not found")
        
    def get_weather_city(self):
        available_cities = ['Nashville', "New York", "San Francisco", "London" ]
        
        print("Available cities for weather update:")
        for index, city in enumerate(available_cities, start=1):
            print(f"{index}: {city}")

        try: 
            choice = int(input("Enter the number of the city you want to check: "))
            if 1 <= choice <= len(available_cities):
                city = available_cities[choice - 1]
                self.weather_city(city)  # Call weather method with the selected city
            else:
                print("Invalid choice. Please select a valid city.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    def fact(self):
        # Get a random fun fact
        fun_facts = [
            "The first oranges weren't orange",
            "The state of Florida is bigger than England",
            "Ants stretch when they wake up in the morning",
            "Hot water freezes faster than cold water",
        ]
        fact = random.choice(fun_facts) # Get random fact
        print(fact)
    
    def whoami(self, username=None):
        # Get user information
        if username:
            user = self.client.hgetall(f"user:{username}")  # Get user details
            if user:  # If user exists
                print(f"User Information for {username}:")
                for key, value in user.items():
                    key = key.decode("utf-8")  # Decode bytes to string
                    value = value.decode("utf-8")  # Decode bytes to string
                    print(f"{key}: {value}")
            else:
                print(f"User '{username}' not found")
        elif self.username:
            user = self.client.hgetall(f"user:{self.username}")  # Get user details
            if user:  # If user exists
                print("User Information:")
                for key, value in user.items():
                    key = key.decode("utf-8")  # Decode bytes to string
                    value = value.decode("utf-8")  # Decode bytes to 
                    print(f"{key}: {value}")
            else:
                print(f"User '{self.username}' not found")
        else:
            print("You have not been identified yet")

    def direct_message(self, message):
        # Send a direct message to the chatbot
        if self.username is None and message != '1':
            print("You need to identify yourself first (Option 1) before using other commands.")
            return
    
        if message == '1':
            username = input("Enter your username: ")
            age = input("Enter your age: ")
            gender = input("Enter your gender: ")
            location = input("Enter your location: ")
            self.identify(username, age, gender, location)
        
        # Join a channel
        elif message == '2':
            channel_to_join = input("Enter the name of the channel you want to join: ")
            self.join_channel(channel_to_join)
            #self.read_message(channel_to_join)
        
        # Leave a channel
        elif message == '3':
            channel_to_leave = input("Enter the name of the channel you want to leave: ")
            self.leave_channel(channel_to_leave)
        
        # Send a message to a channel
        elif message == '4':
            channel = input("Enter channel name: ")
            message = input("Enter your message: ")
            self.send_message(channel, message)

        # Get info about a user
        elif message == '5':
            user_to_get_info = input("Enter username to get info about: ")
            self.whoami(user_to_get_info)

        elif message == '6':
            exit()
        
        # Handle special commands
        elif message.startswith('!'):
            self.process_commands(message)
        
        else:
            print("Invalid choice. Please select a valid option or enter a special command.")

    def process_commands(self, message):
        # Handle special chatbot commands
        if message.startswith("!"):
            if message == "!help":
                self.introduce() # Provide introduction
            elif message == "!weather": 
                self.get_weather_city() # Get weather
            elif message == "!fact":
                self.fact()  # Get fact
            elif message == "!whoami":
                self.whoami() # Get user information
            else:
                print("Command not recognized")
        else:   
            print("Message not recognized")
            

if __name__ == "__main__":
    bot = Chatbot()
    bot.introduce()
    # Main interaction loop here
    while True:
        # Display options
        print("")
        print("Options:")
        print("1: Identify yourself")
        print("2: Join a channel")
        print("3: Leave a channel")
        print("4: Send a message to a channel")
        print("5: Get info about a user")
        print("6: Exit")

        user_input = input("Enter your choice: ") # Get message from user
        bot.direct_message(user_input) # Process commands

