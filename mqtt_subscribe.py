# Importa dependências
import random
import csv
from paho.mqtt import client as mqtt_client

# Declara variáveis de conexão com o broker
broker = '127.0.0.1'
port = 1883
# Declara tópicos
topic1 = "Cabine/Disponivel"
topic2 = "Cabine/Ocupada"
topic3 = "Cabine/Oxisanitizacao"
topic4 = "Cabine/Emergencia"
# Declara variáveis que serão atribuídas as mensagens
disponivel = False
ocupada = False
oxisanitacao = False
emergencia = False

# Gera um ID de cliente randomico para clientes sem ID
client_id = f'subscribe-{random.randint(0, 100)}'

# Declara usuário e senha (não implementado)
# username = 'emqx'
# password = 'public'

# Função para conectar ao broker
def connect_mqtt() -> mqtt_client:
    # Função de tratamento de erros de conexão
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client()
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

# Função de assinatura do broker
def subscribe(client: mqtt_client):
    # Função de tratamento de mensagens
    def on_message(client, userdata, msg):
        global disponivel, ocupada, oxisanitacao, emergencia
        if msg.topic == topic1:
            disponivel = msg.payload.decode()
        elif msg.topic == topic2:
            ocupada = msg.payload.decode()
        elif msg.topic == topic3:
            oxisanitacao = msg.payload.decode()
        elif msg.topic == topic4:
            emergencia = msg.payload.decode()
        print("Disponivel: " + str(disponivel) + " / Ocupada: " + str(ocupada) + 
              " / Oxisanitacao: " + str(oxisanitacao) + " / Emergencia: " + str(emergencia))

    client.subscribe(topic1)
    client.subscribe(topic2)
    client.subscribe(topic3)
    client.subscribe(topic4)
    client.on_message = on_message

# Função principal
def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()

# Executa o programa
if __name__ == '__main__':
    run()