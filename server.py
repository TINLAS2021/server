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
            temp = None

        client = mqtt_client.Client(client_id)
        client.on_connect = on_connect
        client.connect(broker, port)
        return client 
    
    def subscribe(self, client: mqtt_client):
        def on_message(client, userdata, message):
            self.client_data = int(message.payload.decode()) if len(message.payload.decode()) <= 4 else self.client_data
            # print("Received " + str(self.client_data) + " from " + message.topic)
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
        self.move(0)

class Snake:

    def __init__(self, size, pos, sleep_time):
        self.size = size
        self.pos = pos
        self.sleep_time = sleep_time
        self.snake_nodes = self.create_snake(size)
        self.state = "up"
    def create_snake(self, size):
        return [SnakeNode(i) for i in range(size + 1)]
    
    def loop(self):
        for snake_node in self.snake_nodes:
            snake_node.client.loop()
    
    def reset_all(self):
        for snake_node in self.snake_nodes:
            snake_node.reset()
        sleep(2)
    
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

    def up(self, pos, sleep_time, direction_right):
        if direction_right:
            self.snake_nodes[5].move(pos)
            sleep(sleep_time)
            self.snake_nodes[6].move(-pos)
            sleep(sleep_time)
        else:
            self.snake_nodes[5].move(pos)
            sleep(sleep_time)
            self.snake_nodes[6].move(pos)
            sleep(sleep_time)
        self.snake_nodes[5].reset()
        sleep(sleep_time)
        self.snake_nodes[6].reset()
        sleep(sleep_time)
    
    def right(self, pos, sleep_time, direction_down):
        if direction_down:
            self.snake_nodes[4].move(pos)
            sleep(sleep_time)
            self.snake_nodes[3].move(pos)
            sleep(sleep_time)
        else:
            self.snake_nodes[4].move(-pos)
            sleep(sleep_time)
            self.snake_nodes[3].move(pos)
            sleep(sleep_time)
        self.snake_nodes[4].reset()
        sleep(sleep_time)
        self.snake_nodes[3].reset()
        sleep(sleep_time)
    
    def down(self, pos, sleep_time, direction_left):
        if direction_left:
            self.snake_nodes[5].move(pos)
            sleep(sleep_time)
            self.snake_nodes[6].move(-pos)
            sleep(sleep_time)
        else:
            self.snake_nodes[5].move(pos)
            sleep(sleep_time)
            self.snake_nodes[6].move(pos)
            sleep(sleep_time)
        self.snake_nodes[5].reset()
        sleep(sleep_time)
        self.snake_nodes[6].reset()
        sleep(sleep_time)
    
    def left(self, pos, sleep_time, direction_up):
        if direction_up:
            self.snake_nodes[4].move(-pos)
            sleep(sleep_time)
            self.snake_nodes[3].move(-pos)
            sleep(sleep_time)
        else:
            self.snake_nodes[4].move(-pos)
            sleep(sleep_time)
            self.snake_nodes[3].move(pos)
            sleep(sleep_time)
        self.snake_nodes[4].reset()
        sleep(sleep_time)
        self.snake_nodes[3].reset()
        sleep(sleep_time)

    def forward(self):
        pos = self.pos
        sleep_time = self.sleep_time
        self.up(pos, sleep_time, True)
        self.right(pos, sleep_time, True)
        self.down(pos, sleep_time, True)
        self.left(pos, sleep_time, True)
    
    def backward(self):
        pos = self.pos
        sleep_time = self.sleep_time
        self.up(pos, sleep_time, False)
        self.right(pos, sleep_time, False)
        self.down(pos, sleep_time, False)
        self.left(pos, sleep_time, False)

def run():
    snake = Snake(9, 150, 0.2)
    snake.reset_all()
    snake.forward()
    # snake.backward()

if __name__ == '__main__':
    run()
