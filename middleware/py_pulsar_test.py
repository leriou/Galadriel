import pulsar 

client = pulsar.Client('pulsar://localhost:6650')
producer = client.create_producer('test-pulsar')
consumer = client.subscribe('test-pulsar', subscription_name='test-pulsar-sub')

for i in range(1000):
    producer.send(('hello-pulsar-%d' % i).encode('utf-8'))

n = 0
while n < 999:
    msg = consumer.receive()
    print("Received message: '%s'" % msg.data())
    consumer.acknowledge(msg)
    n += 1

client.close()