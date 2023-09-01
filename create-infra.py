import json
import boto3

class QueueDTO:
    def __init__(self, Name, DeadLetter):
        self.Name = Name
        self.DeadLetter = DeadLetter

class TopicDTO:
    def __init__(self, Name, Queues):
        self.Name = Name
        self.Queues = [QueueDTO(**queue) for queue in Queues]

class BucketDTO:
    def __init__(self, Name):
        self.Name = Name

class SecretDTO:
    def __init__(self, Name, Content, Description):
        self.Name = Name
        self.Content = Content
        self.Description = Description

class ConfigurationDTO:
    def __init__(self, AccessKey, SecretKey, ServiceUrl, Profile, Topics, Queues, Buckets, SecretsManager):
        self.AccessKey = AccessKey
        self.SecretKey = SecretKey
        self.ServiceUrl = ServiceUrl
        self.Profile = Profile
        self.Topics = [TopicDTO(**topic) for topic in Topics]
        self.Queues = [QueueDTO(**queue) for queue in Queues]
        self.Buckets = [BucketDTO(**bucket) for bucket in Buckets]
        self.SecretsManager = [SecretDTO(**secret) for secret in SecretsManager]

aws_access_key = ""
aws_secret_key = ""
aws_service_url = ""

def main():

    print("Iniciando criação dos objetos...")

    with open("infra-objects.json", "r") as json_file:
        json_data = json.load(json_file)
        config = ConfigurationDTO(**json_data)

        global aws_access_key
        global aws_secret_key
        global aws_service_url

        aws_access_key = config.AccessKey
        aws_secret_key = config.SecretKey
        aws_service_url = config.ServiceUrl

        print("############ Sumário #################")
        print("Total de topicos:", len(config.Topics))
        print("Total de filas:", len(config.Queues))
        print("Total de buckets:", len(config.Buckets))
        print("Total de secrets:", len(config.SecretsManager))
        print("######################################")
        create_topics(config.Topics)
        create_queues(config.Queues)
        create_buckets(config.Buckets)
        create_secrets(config.SecretsManager)
        print("Criação dos objetos finalizadas")

def create_topics(topics_from_json):
    print('iniciando criação de topicos...')
    for topic_from_json in topics_from_json:
        topic_from_json_name = topic_from_json.Name.strip()
        print(f'criando topico {topic_from_json_name}')
        create_topic_resp = create_topic(topic_from_json_name)
        create_queues(topic_from_json.Queues)
        subscribe_queues_to_topic(create_topic_resp['TopicArn'], topic_from_json.Queues)

def create_topic(topic_from_json):
    sns = boto3.client('sns', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key, endpoint_url=aws_service_url)
    topic_from_json_name = topic_from_json.strip()
    if topic_from_json.endswith(".fifo"):
        return sns.create_topic(Name=topic_from_json_name, Attributes={'FifoTopic': 'true'})
    sns.create_topic(Name=topic_from_json_name)

def create_queues(queues_from_json):
    print('iniciando criação de filas...')
    for queue_from_json in queues_from_json:
        queue_from_json_name = queue_from_json.Name.strip()
        queue_from_json_deadletter = queue_from_json.DeadLetter.strip()
        print(f'criando fila {queue_from_json_name}')
        create_queue_url_resp = create_queue(queue_from_json_name)
        print(f'criando deadletter {queue_from_json_deadletter}')
        create_queue_url_dlq_resp = create_queue(queue_from_json=queue_from_json_deadletter)
        print(f'criando subscricao da fila {queue_from_json_name} com a dlq {queue_from_json_deadletter}')
        subscribe_dlq(create_queue_url_resp, create_queue_url_dlq_resp)

def create_queue(queue_from_json):
    sqs = boto3.client('sqs', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key, endpoint_url=aws_service_url)
    if queue_from_json.endswith(".fifo"):
        create_queue_resp = sqs.create_queue(QueueName=queue_from_json.strip(),Attributes={'FifoQueue': 'true'} )
        return create_queue_resp['QueueUrl']

    create_queue_resp = sqs.create_queue(QueueName=queue_from_json.strip())
    return  create_queue_resp['QueueUrl']

def subscribe_queues_to_topic(topic_arn, queues_from_json):
    print('iniciando subscrição das filas ao topico ...')
    sns = boto3.client('sns', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key, endpoint_url=aws_service_url)
    sqs = boto3.client('sqs', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key, endpoint_url=aws_service_url)
    for queue_from_json in queues_from_json:
        queue_url_respo = sqs.get_queue_url(QueueName=queue_from_json.Name.strip())
        queue_attribute_respo = sqs.get_queue_attributes(QueueUrl=queue_url_respo['QueueUrl'], AttributeNames=['All'])
        sns.subscribe(TopicArn=topic_arn.strip(), Protocol='sqs', Endpoint=queue_attribute_respo['Attributes']['QueueArn'].strip())

def subscribe_dlq(queue_url, queue_url_dlq):
    print('iniciando subscrição dlq...')
    sqs = boto3.client('sqs', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key, endpoint_url=aws_service_url)
    attibutes_resp = sqs.get_queue_attributes(QueueUrl=queue_url_dlq.strip(), AttributeNames=['All'])
    redrive_policy = {
        "deadLetterTargetArn": attibutes_resp['Attributes']['QueueArn'],
        "maxReceiveCount": 3
    }
    sqs.set_queue_attributes(QueueUrl=queue_url,Attributes={'RedrivePolicy': json.dumps(redrive_policy) })

def create_buckets(buckets_from_json):
    print('iniciando criação de buckets...')
    s3 = boto3.client('s3', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key, endpoint_url=aws_service_url)
    for bucket_from_json in buckets_from_json:
        bucket_from_json_name = bucket_from_json.Name.strip()
        s3.create_bucket(Bucket=bucket_from_json_name)
        print(f'bucket criado: {bucket_from_json_name}')

def create_secrets(secrets_from_json):
    print('iniciando criação de secrets...')
    secretsmanager = boto3.client('secretsmanager', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key, endpoint_url=aws_service_url)
    for secret_from_json in secrets_from_json:
        try:
            secret_name = secret_from_json.Name.strip()
            secretsmanager.create_secret(Name=secret_name, SecretString=secret_from_json.Content, Description=secret_from_json.Description)
            print(f'secret criado: {secret_name}')
        except Exception as e:
            print(f"An exception occurred: {e}")

main()
