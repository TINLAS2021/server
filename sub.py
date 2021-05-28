from paho.mqtt import client as mqtt_client
from time import sleep
import random

broker = "185.224.91.138"
port = 1883
topic_input = "bigSnake/input/"
topic_output = "bigSnake/output/"
client_count = 11
client_data = [0] * client_count
clients = []


def connect_mqtt(client_id) -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print(client_id + " connected to Broker.")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client, client_id):
    def on_message(client, userdata, msg):
        client_data[client_id] = int(msg.payload.decode())
        print('Received ' + str(client_data[int(client_id)]) + ' from ' + msg.topic)

    client.subscribe(topic_output + str(client_id))
    client.on_message = on_message


def create_clients(amount):
    for client in range(amount):
        temp_client = connect_mqtt(f'{client}')
        subscribe(temp_client, client)
        temp_client.loop_start()
        clients.append(temp_client)


def run():
    create_clients(client_count)
    reset_all(clients)
    sleep(3)
    form_u_letter_inverse()
    # while(True):
    #     slither(clients)
    while True:
        for i in range(len(clients)):
            clients[i].loop()

def move(client_id, val):
    clients[client_id].publish(topic_input + str(client_id), str(val))
    sleep(0.1)

def reset(client_id):
    print("Resetting node " + str(client_id))
    move(client_id, 0)

def reset_all(clients_list):
    for i in range(len(clients_list)):
        reset(i)

def form_u_letter(clients_list):
    for i in range(len(clients_list)):
        if i % 2 == 0:
            move(i, 250)

def form_u_letter_inverse(clients_list):
    for i in range(len(clients_list)):
        if i % 2 == 0:
            move(i, -250)

def slither(clients_list):
    for i in range(len(clients_list)):
        move(i, client_data[i] + random.randint(-100,100))



if __name__ == '__main__':
    run()
