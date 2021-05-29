from paho.mqtt import client as mqtt_client
from time import sleep
import random

broker = "185.224.91.138"
port = 1883
topic_input = "bigSnake/input/"
topic_output = "bigSnake/output/"
class SnakeNode:

    def __init__(self, id):
        self.id = id
        self.client = self.create_client(id)
        self.client_data = 0
    
    def connect_mqtt(self, client_id) -> mqtt_client:
        def on_connect(client, userdata, flags, rc):
            print(client_id + " connected to Broker." if rc == 0 else "Failed to connect")

        client = mqtt_client.Client(client_id)
        client.on_connect = on_connect
        client.connect(broker, port)
        return client 
    
    def subscribe(self, client: mqtt_client):
        def on_message(client, userdata, message):
            self.client_data = int(message.payload.decode())
            print("Received " + str(self.client_data) + " from " + message.topic)
            
        client.subscribe(topic_output + str(self.id))
        client.on_message = on_message
    
    def create_client(self, client_id):
        client = self.connect_mqtt(f'{client_id}')
        self.subscribe(client)
        client.loop_start()
        return client
    
    def move(self, val):
        self.client.publish(topic_input + str(self.id), str(val))
    
    def reset(self):
        # print("Resetting snake_node " + str(self.id))
        self.move(0)

class Snake:

    def __init__(self, size):
        self.size = size
        self.snake_nodes = self.create_snake(size)
    
    def create_snake(self, size):
        return [SnakeNode(i) for i in range(size)]
    
    def loop(self):
        for snake_node in self.snake_nodes:
            snake_node.client.loop()
    
    def reset_all(self):
        for snake_node in self.snake_nodes:
            snake_node.reset()
        sleep(3)
    
    def form_u_letter(self):
        for snake_node in self.snake_nodes:
            if snake_node.id % 2 == 0:
                snake_node.move(250)
        sleep(3)

    def form_u_letter_inverse(self):
        for snake_node in self.snake_nodes:
            if snake_node.id % 2 == 0:
                snake_node.move(-250)
        sleep(3)

    def slither(self):
        for snake_node in self.snake_nodes:
            snake_node.move(snake_node.client_data + random.randint(-100,100))
        sleep(3)

def run():
    snake = Snake(11)
    snake.reset_all()
    while True:
        snake.loop()
        sleep(1)

    # snake.form_u_letter()
    # snake.reset_all()
    # snake.form_u_letter_inverse()

if __name__ == '__main__':
    run()
