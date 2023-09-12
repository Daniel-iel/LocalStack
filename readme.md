# Instalação e Configuração do Localstack

## Pré-Requisitos

As ferramentas do aws cli e docker são pré-requitos para trabalhar com o localstack.

- [Docker](https://docs.docker.com/get-docker/)
- [AWS CLI](https://docs.aws.amazon.com/pt_br/cli/latest/userguide/getting-started-install.html)

Se o uso do Docker não for viável, uma alternativa é utilizar o Podman. Para empregar o Podman, será necessário instalar o Python3 e o pip3.

- [PodMan](https://podman.io/)
- [Python](https://www.python.org/downloads/)
- [Pip3](https://www.temok.com/blog/how-to-install-pip3/)

## Configuração AWS CLI

Antes de começar, verifique se o AWS CLI foi instalado corretamente usando o comando `aws -h`. Se a instalação foi bem-sucedida, você verá o output abaixo no terminal.

```cmd
usage: aws [-h] [--profile PROFILE] [--debug]

options:
  -h, --help         show this help message and exit
  --profile PROFILE
  --debug
```

### Configuração do AWS Profile

```bash
aws configure --profile <nome do profile>
```

Quando você executar o comando `aws configure`, o terminal vai pedir para você fornecer alguns dados importantes, como o *"AWS Access Key ID"*, *"AWS Secret Access Key"*, *"Default region name"* e *"Default output format"*.

---
**NOTE**

Os seguintes valores devem ser escolhidos para os inputs *Default region name* e *Default output format*.

- *Default region name:* us-east-1
- *Default output format:* json ou yaml

---

## Inicializando LocalStack (Docker)

Todas as configurações do LocalStack estão definidas no arquivo docker-compose.yml. Para iniciar o container, siga as etapas abaixo:

1. Abra o terminal e navegue até a pasta onde o arquivo docker-compose.yml está localizado.
2. Inicie uma nova instância da imagem executando o comando `docker-compose up -d`.
3. Utilize o comando `docker ps` para confirmar que o container está em execução.
4. Se o container estiver em funcionamento, o seguinte resultado será exibido no terminal.

```shell
CONTAINER ID   IMAGE                   COMMAND                  CREATED        STATUS                  PORTS                                             NAMES
cb2ddd8afe5f   localstack/localstack   "docker-entrypoint.sh"   30 hours ago   Up 30 hours (healthy)   0000-0000/tcp, 0000/tcp, 0.0.0.0:0000->0000/tcp   localstack-localstack-1
```

## Inicializando LocalStack (Podman)

Todas as configurações do LocalStack estão definidas no arquivo docker-compose.yml. Para iniciar o container, siga as etapas abaixo:

1. Abra o terminal e navegue até a pasta onde o arquivo docker-compose.yml está localizado.
2. Execute o comando `pip3 install podman-compose`.
3. Inicie uma nova instância da imagem executando o comando `podman-compose up -d`.
4. Utilize o comando `podman ps` para confirmar que o container está em execução.
5. Se o container estiver em funcionamento, o seguinte resultado será exibido no terminal.

```shell
CONTAINER ID  IMAGE                                   COMMAND     CREATED         STATUS                    PORTS                    NAMES
5b328d9c69c2  docker.io/localstack/localstack:latest              33 minutes ago  Up 31 seconds (starting)  0.0.0.0:00000->0000/tcp  localstack_localstack_1
```

## Provisionando da infraestrutura local no localstack

O provisionamento para criar os objetos no LocalStack é realizado por meio de um script em Python.

1. Verifique se todos os recursos, como SQS, SNS, S3 e Secret Manager, estão devidamente configurados no arquivo `infra-objects.json`.
2. Abra um terminal na raiz do seu projeto, onde se encontram arquivos como `docker-compose.yml, create-infra.py`.
3. Execute o comando para instalar o boto 3 `pip3 install boto3`.
4. Execute o comando python `create-infra.py` para criar os objetos no localstack.
5. Se tudo estiver configurado corretamente, você verá a mensagem `Criação dos recursos concluída` exibida no terminal.

# Getting Started

Ao realizar interações com o LocalStack por meio da linha de comando, é fundamental que os atributos *--endpoint-url http://localhost:4566 e --profile nome do perfil* estejam sempre vinculados aos comandos. Isso permite que a interface de linha de comando da AWS reconheça que o comando está sendo executado em uma instância local do AWS.

## Simple Queue Service (SQS)

O primeiro passo ao trabalhar com o SQS é se familiarizar com a [documentação](https://aws.amazon.com/pt/sqs/).

Ao interagir com o comando `aws sqs`, você terá acesso às seguintes opções. Embora não iremos nos aprofundar em todas elas, é útil conhecer quais são essas opções.

```shell
add-permission                           | change-message-visibility
change-message-visibility-batch          | create-queue
delete-message                           | delete-message-batch
delete-queue                             | get-queue-attributes
get-queue-url                            | list-dead-letter-source-queues
list-queue-tags                          | list-queues
purge-queue                              | receive-message
remove-permission                        | send-message
send-message-batch                       | set-queue-attributes
tag-queue                                | untag-queue
```

### Criando Fila

Utilizado para criar uma nova fila (fila de mensagens) no Amazon Simple Queue Service (SQS).

```shell
# fila standard
aws sqs create-queue <nome da fila> --endpoint-url http://localhost:4566 --profile  <nome do profile>

# fila fifo
aws sqs create-queue <nome da fila> --endpoint-url http://localhost:4566 --profile  <nome do profile> --attributes FifoQueue=true
```

---
**NOTE**

Para filas do tipo FIFO, é necessário que o nome da fila termine com .fifo, e é essencial incluir a tag *--attributes FifoQueue=true* ao utilizar o comando `aws sqs create-queue`.

---

### Deletando Fila

Usado para excluir uma fila (fila de mensagens) específica no Amazon Simple Queue Service (SQS).

```shell
aws sqs delete-queue --queue-url <url da fila> --endpoint-url http://localhost:4566 --profile <nome do profile>
```

### Deletando Mensagem

Utilizado para remover uma mensagem específica de uma fila no Amazon Simple Queue Service (SQS), é fundamental fornecer a URL da fila e o identificador de recebimento (receipt handle) da mensagem nos parâmetros *--queue-url* e *--receipt-handle*, respectivamente.

```shell
aws sqs delete-message --queue-url <url da fila> --receipt-handle <receipt-handle da mensagem> --endpoint-url http://localhost:4566 --profile <nome do profile>
```

### Listando Filas

Usado para listar as filas (filas de mensagens) existentes no Amazon Simple Queue Service (SQS).

```shell
aws sqs list-queues --endpoint-url http://localhost:4566 --profile <nome do profile>
```

### Receber Mensagens

Usado para recuperar mensagens da fila (fila de mensagens) no Amazon Simple Queue Service (SQS), é imprescindível indicar a URL da fila no parâmetro *--queue-url*.

```shell
aws sqs receive-message --queue-url <url da fila> --endpoint-url http://localhost:4566 --profile <nome do profile>
```

### Enviando uma mensagem

Usado para enviar uma mensagem para uma fila (fila de mensagens) no Amazon Simple Queue Service (SQS), é imprescindível indicar a URL da fila no parâmetro *--queue-url*..

```shell
aws sqs send-message --queue-url <url da fila> --message-body "<mensagem>" --endpoint-url http://localhost:4566 --profile <nome do profile>
```

---
**NOTE**

Se o seu processo de leitura de mensagens requer informações adicionais, como o nome do evento, por exemplo, esses detalhes podem ser incluídos usando uma tag *--message-attributes '{"AttributeName":{"DataType":"String","StringValue":"AttributeValue"}}'*

---

### Configuração da Fila

Usado para obter os atributos de uma fila Amazon Simple Queue Service (SQS).

```shell
aws sqs get-queue-attributes --queue-url <url da fila> --endpoint-url http://localhost:4566 --profile <nome do profile>
```

### Dead-Letter Queue (DQL)

Para configurar o redirecionamento de mensagens para uma DLQ (Dead-Letter Queue), é importante que ambas as filas sejam do mesmo tipo, seja Standard ou FIFO. Além disso, é necessário se familiarizar com essa funcionalidade por meio da [documentação](https://docs.aws.amazon.com/pt_br/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-dead-letter-queues.html).

```shell
# Criar fila
aws sqs create-queue <nome da fila> --endpoint-url http://localhost:4566 --profile  <nome do profile>

# Criar fila Morta
aws sqs create-queue <nome da fila morta> --endpoint-url http://localhost:4566 --profile  <nome do profile>

aws sqs set-queue-attributes \
--queue-url <url da fila> \
--attributes '{
    "RedrivePolicy": "{\"deadLetterTargetArn\":\"<ARN da fila morta>\",\"maxReceiveCount\":\"3\"}",
    "VisibilityTimeout": "90"
}'
```

---
**NOTE**

O comando `aws sqs set-queue-attributes` permite configurar a fila principal para redirecionar mensagens após 3 tentativas.

---

## Simple Notification Service (SNS)

O primeiro passo ao trabalhar com o SNS é se familiarizar com a [documentação](https://aws.amazon.com/pt/sns/).

Ao interagir com o comando `aws sns`, você terá acesso às seguintes opções. Embora não iremos nos aprofundar em todas elas, é útil conhecer quais são essas opções.

```shell
add-permission                           | check-if-phone-number-is-opted-out
confirm-subscription                     | create-platform-application
create-platform-endpoint                 | create-sms-sandbox-phone-number
create-topic                             | delete-endpoint
delete-platform-application              | delete-sms-sandbox-phone-number
delete-topic                             | get-data-protection-policy
get-endpoint-attributes                  | get-platform-application-attributes
get-sms-attributes                       | get-sms-sandbox-account-status
get-subscription-attributes              | get-topic-attributes
list-endpoints-by-platform-application   | list-origination-numbers
list-phone-numbers-opted-out             | list-platform-applications
list-sms-sandbox-phone-numbers           | list-subscriptions
list-subscriptions-by-topic              | list-tags-for-resource
list-topics                              | opt-in-phone-number
publish                                  | publish-batch
put-data-protection-policy               | remove-permission
set-endpoint-attributes                  | set-platform-application-attributes
set-sms-attributes                       | set-subscription-attributes
set-topic-attributes                     | subscribe
tag-resource                             | unsubscribe
untag-resource                           | verify-sms-sandbox-phone-number
```

### Criando Tópico

Usado para criar um novo tópico (topic) no Amazon Simple Notification Service (SNS).

```shell
# tópico standard
aws sns create-topic --name <nome do tópico> --endpoint-url http://localhost:4566 --profile  <nome do profile>

# tópico fifo
aws sns create-topic --name <nome do tópico> --endpoint-url http://localhost:4566 --profile  <nome do profile> --attributes FifoTopic=true
```

---
**NOTE**

1. No caso de tópicos do tipo FIFO, é fundamental que o nome do tópico seja finalizado com a extensão ".fifo". Além disso, ao utilizar o comando `aws sns create-topic`, é essencial adicionar a tag *--attributes FifoTopic=true*.
2. É importante destacar que apenas é viável associar filas e tópicos que compartilhem o mesmo tipo: tópicos FIFO devem ser vinculados a filas FIFO, enquanto tópicos do tipo standard devem ser conectados a filas do tipo standard.

---

### Deletando Tópico

Utilizado para excluir um tópico (topic) específico do Amazon Simple Notification Service (SNS).

```shell
aws sns delete-topic --topic-arn <arn do topic> --endpoint-url http://localhost:4566 --profile <nome do profile>
```

### Listando Tópicos

Usado para listar os tópicos (topics) existentes no Amazon Simple Notification Service (SNS).

```shell
aws sns list-topics --endpoint-url http://localhost:4566 --endpoint-url http://localhost:4566 --profile <nome do profile>
```

### Conectando uma fila a um tópico

Para estabelecer uma conexão entre uma fila SQS e um tópico, proceda com o comando abaixo.

```shell
aws sns subscribe --topic-arn <arn do topico> --protocol sqs --notification-endpoint <arn da fila> --endpoint-url http://localhost:4566 --profile <nome do profile>
```

---
**NOTE**

Após realizar a inscrição, será necessário confirmá-la, o que pode ser feito ao listar todas as mensagens presentes na fila.

```shell
aws sqs receive-message --queue-url <url da fila> --endpoint-url http://localhost:4566 --profile <nome do profile>
```

---

### Enviando mensagem

Utilizado para publicar (enviar) uma mensagem para um tópico (topic) no Amazon Simple Notification Service (SNS),

```shell
aws sns publish --topic-arn <arn do topico> --message "<mensagem>" --endpoint-url http://localhost:4566 --profile <nome do profile>
```

---
**NOTE**

Se o seu processo de leitura de mensagens requer informações adicionais, como o nome do evento, por exemplo, esses detalhes podem ser incluídos usando uma tag *--message-attributes '{"AttributeName":{"DataType":"String","StringValue":"AttributeValue"}}'*

---

## Simple Storage Service (S3)

O primeiro passo ao trabalhar com o S3 é se familiarizar com a [documentação](https://aws.amazon.com/pt/s3/).

Ao interagir com o comando `aws S3api`, você terá acesso às seguintes opções. Embora não iremos nos aprofundar em todas elas, é útil conhecer quais são essas opções.

```shell
abort-multipart-upload                   | complete-multipart-upload
copy-object                              | create-bucket
create-multipart-upload                  | delete-bucket
delete-bucket-analytics-configuration    | delete-bucket-cors
delete-bucket-encryption                 | delete-bucket-intelligent-tiering-configuration
delete-bucket-inventory-configuration    | delete-bucket-lifecycle
delete-bucket-metrics-configuration      | delete-bucket-ownership-controls
delete-bucket-policy                     | delete-bucket-replication
delete-bucket-tagging                    | delete-bucket-website
delete-object                            | delete-object-tagging
delete-objects                           | delete-public-access-block
get-bucket-accelerate-configuration      | get-bucket-acl
get-bucket-analytics-configuration       | get-bucket-cors
get-bucket-encryption                    | get-bucket-intelligent-tiering-configuration
get-bucket-inventory-configuration       | get-bucket-lifecycle
get-bucket-lifecycle-configuration       | get-bucket-location
get-bucket-logging                       | get-bucket-metrics-configuration
get-bucket-notification                  | get-bucket-notification-configuration
get-bucket-ownership-controls            | get-bucket-policy
get-bucket-policy-status                 | get-bucket-replication
get-bucket-request-payment               | get-bucket-tagging
get-bucket-versioning                    | get-bucket-website
get-object                               | get-object-acl
get-object-attributes                    | get-object-legal-hold
get-object-lock-configuration            | get-object-retention
get-object-tagging                       | get-object-torrent
get-public-access-block                  | head-bucket
head-object                              | list-bucket-analytics-configurations
list-bucket-intelligent-tiering-configurations | list-bucket-inventory-configurations
list-bucket-metrics-configurations       | list-buckets
list-multipart-uploads                   | list-object-versions
list-objects                             | list-objects-v2
list-parts                               | put-bucket-accelerate-configuration
put-bucket-acl                           | put-bucket-analytics-configuration
put-bucket-cors                          | put-bucket-encryption
put-bucket-intelligent-tiering-configuration | put-bucket-inventory-configuration
put-bucket-lifecycle                     | put-bucket-lifecycle-configuration
put-bucket-logging                       | put-bucket-metrics-configuration
put-bucket-notification                  | put-bucket-notification-configuration
put-bucket-ownership-controls            | put-bucket-policy
put-bucket-replication                   | put-bucket-request-payment
put-bucket-tagging                       | put-bucket-versioning
put-bucket-website                       | put-object
put-object-acl                           | put-object-legal-hold
put-object-lock-configuration            | put-object-retention
put-object-tagging                       | put-public-access-block
restore-object                           | select-object-content
upload-part                              | upload-part-copy
write-get-object-response                | wait
```

### Listando Buckets

Utilizado para listar todos os buckets (recipientes de armazenamento) presentes no s3 associada ao profile configurado.

```shell
aws s3api list-buckets --endpoint-url http://localhost:4566 --profile <nome do profile>
```

### Listando Objeto do Bucket

Usado para listar os objetos (arquivos) armazenados em um bucket específico no s3.

```shell
aws s3api list-objects --bucket <nome do bucket> --endpoint-url http://localhost:4566 --profile <nome do profile>
```

### Criando Bucket

Utilizado para criar um novo bucket (recipientes de armazenamento) no s3.

```shell
aws s3api create-bucket --bucket <nome do bucket> --endpoint-url http://localhost:4566 --profile <nome do profile>
```

### Deletando Bucket

Usado para excluir um bucket (recipientes de armazenamento) específico no s3.

```shell
aws s3api delete-bucket --endpoint-url http://localhost:4566 --profile <nome do profile>
```

### Enviando Arquivo

Utilizado para criar ou substituir um objeto (arquivo) em um bucket específico no s3.

```shell
aws s3api put-object --bucket <nome do bucket> --key <path do arquivo no bucket> --body <path do arquivo da maquina local> --endpoint-url http://localhost:4566 --profile <nome do profile>
```

### Deletando Arquivo

Usado para excluir um objeto (arquivo) específico em um bucket no s3.

```shell
aws s3api delete-object --bucket <nome do bucket> --key <path do arquivo no bucket> --endpoint-url http://localhost:4566 --profile <nome do profile>
```

## Secrets Manager

O primeiro passo ao trabalhar com o Secrets Manager é se familiarizar com a [documentação](https://aws.amazon.com/pt/secrets-manager/).

Ao interagir com o comando `aws secretsmanager`, você terá acesso às seguintes opções. Embora não iremos nos aprofundar em todas elas, é útil conhecer quais são essas opções.

```shell
cancel-rotate-secret                     | create-secret
delete-resource-policy                   | delete-secret
describe-secret                          | get-random-password
get-resource-policy                      | get-secret-value
list-secret-version-ids                  | list-secrets
put-resource-policy                      | put-secret-value
remove-regions-from-replication          | replicate-secret-to-regions
restore-secret                           | rotate-secret
stop-replication-to-replica              | tag-resource
untag-resource                           | update-secret
update-secret-version-stage              | validate-resource-policy
```

### Criando Secret

Usado para criar um novo segredo (informação sensível) no Secrets Manager.

```shell
aws secretsmanager create-secret --name <nome da secret> --secret-string "<texto do segredo>" --endpoint-url http://localhost:4566 --profile <nome do profile>
```

### Listando Secret

Utilizado para listar os segredos (informações sensíveis) armazenados no Secrets Manager.

```shell
aws secretsmanager list-secrets --endpoint-url http://localhost:4566 --profile <nome do profile>
```

### Deletando Secret

Usado para excluir um segredo (informação sensível) específico do Secrets Manager.

```shell
aws secretsmanager delete-secret --secret-id <nome da secret> --endpoint-url http://localhost:4566 --profile <nome do profile>
```

### Consulta Valor da Secret

Utilizado para recuperar o valor de um segredo específico do Secrets Manager.

```shell
aws secretsmanager get-secret-value --secret-id <nome da secret> --endpoint-url http://localhost:4566 --profile <nome do profile>
```
