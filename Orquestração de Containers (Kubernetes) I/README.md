## Instalando o Kubernetes através do Kind e criando um cluster

Digitar no terminal

```bash

# Verifica se o Kind está instalado
kind

# Verifica se o kubectl está instalado
kubectl

# Cria um cluster Kubernetes utilizando o Kind
kind create cluster

# Exibe as informações do cluster criado e verifica se o contexto foi configurado corretamente
kubectl cluster-info --context kind-kind

# Lista os nós disponíveis no cluster
kubectl get nodes

# Verifica os containers do cluster executando no Docker
docker ps -a

# Deleta o cluster criado com nome kind-kind
kind delete cluster --name kind-kind

```

## Criando Cluster com múltiplos nós utilizando o Kind

Digitar no terminal

```bash

# Entra no diretório onde está o arquivo de configuração do cluster
cd 1.criar-cluster

# Cria o cluster com 1 nó de controle e 3 nós workers, conforme o arquivo cluster.yaml
kind create cluster --config=cluster.yaml --name=k8s-cluster

# Exibe informações do cluster usando o contexto apropriado
kubectl cluster-info --context kind-k8s-cluster

# Lista os nós disponíveis
kubectl get nodes

# Lista todos os containers do cluster no Docker
docker ps -a

```

## Criando o primeiro Pod no cluster Kubernetes com a aplicação

Digitar no terminal

```bash

# Volta para o diretório raiz
cd ..

# Acessa o diretório de criação do Pod
cd 2.criar-pod

# Acessa o diretório da aplicação
cd aplicacao

# Testa a aplicação localmente com Docker Compose
docker compose up -d

# Derruba a aplicação
docker compose down -v

# Cria a imagem Docker da aplicação
docker build . -t helderprado/servidor-python:1.0

# Envia a imagem para o Docker Hub
docker push helderprado/servidor-python:1.0

# Volta ao diretório do Pod
cd ..

# Aplica o arquivo de secrets
kubectl apply -f secret.yaml

# Cria o Pod com base no manifesto YAML
kubectl apply -f pod.yaml

# Lista os pods atuais
kubectl get pods

# Exibe detalhes do pod criado
kubectl describe pod servidor-python

# Visualiza os logs do pod
kubectl logs servidor-python

# Faz o redirecionamento de porta para acessar a aplicação
kubectl port-forward pod/servidor-python 8000:8000

# Interrompe o redirecionamento
ctrl+c

# Exclui o pod criado
kubectl delete pod servidor-python

```

## Criando o primeiro ReplicaSet da aplicação

Digitar no terminal

```bash

# Volta um diretório
cd ..

# Acessa a pasta de criação do ReplicaSet
cd 3.criar-replicaset

# Cria o ReplicaSet com 5 réplicas da aplicação
kubectl apply -f replicaset.yaml

# Lista os ReplicaSets existentes
kubectl get replicaset

# Lista os pods gerenciados pelo ReplicaSet
kubectl get pods

# Deleta um pod aleatório (será recriado automaticamente)
kubectl delete pod `NOME_DO_POD`

# Lista novamente os pods para verificar recriação
kubectl get pods

# Atualiza a aplicação para a versão 2.0
cd aplicacao-atualizada
docker build . -t helderprado/servidor-python:2.0

# Roda o container localmente para verificar a nova imagem
docker run --rm -p 8000:8000 --env-file .env helderprado/servidor-python:2.0

# Encerra o container
ctrl+c

# Envia a nova imagem para o Docker Hub
docker push helderprado/servidor-python:2.0

# Volta ao diretório do ReplicaSet
cd ..
kubectl apply -f replicaset.yaml

# Lista os pods atualizados
kubectl get pods

# Exibe detalhes de um pod específico
kubectl describe pod `NOME_DO_POD`

# Deleta um pod do ReplicaSet para observar a recriação
kubectl delete pod `NOME_DO_POD`

# Lista os pods novamente
kubectl get pods

# Exibe detalhes do novo pod criado
kubectl describe pod `NOME_DO_POD_MAIS_NOVO`

# Deleta o ReplicaSet
kubectl delete replicaset servidor-python

# Verifica que os pods foram encerrados
kubectl get pods

```

## Criando o primeiro Deployment da aplicação

Digitar no terminal

```bash

# Volta um diretório
cd ..

# Acessa o diretório de criação do Deployment
cd 4.criar-deployment

# Cria o Deployment com 5 réplicas da aplicação
kubectl apply -f deployment.yaml

# Lista os pods criados pelo Deployment
kubectl get pods

# Lista os Deployments
kubectl get deployments

# Lista os ReplicaSets associados ao Deployment
kubectl get replicasets

# Atualiza a versão da aplicação no arquivo YAML e aplica novamente
kubectl apply -f deployment.yaml

# Exibe detalhes de um pod específico
kubectl describe pod `NOME_DO_POD`

# Lista novamente os ReplicaSets (para ver atualização)
kubectl get replicasets
```

## Criando o primeiro Service da aplicação

Digitar no terminal

```bash

# Volta um diretório
cd ..

# Acessa o diretório de criação do Service
cd 5.criar-service

# Cria o Service do tipo ClusterIP
kubectl apply -f service-cluster-ip.yaml

# Lista os serviços disponíveis
kubectl get services

# Ou usa o atalho para visualizar os serviços
kubectl get svc

# Faz redirecionamento de porta para acessar o serviço
kubectl port-forward svc/servidor-python-service 8000:80

# Interrompe o redirecionamento
ctrl+c

# Deleta o Service do tipo ClusterIP
kubectl delete svc servidor-python-service

# Cria o Service do tipo NodePort
kubectl apply -f service-node-port.yaml

# Lista novamente os serviços
kubectl get svc

# Faz redirecionamento de porta para testar o NodePort (pode variar)
kubectl port-forward svc/servidor-python-service 30001:80

# Interrompe o redirecionamento
ctrl+c

# Testa outro NodePort se necessário
kubectl port-forward svc/servidor-python-service 30002:80

# Interrompe o redirecionamento
ctrl+c

# Deleta o Service do tipo NodePort
kubectl delete svc servidor-python-service

# Cria o Service do tipo LoadBalancer (simulado localmente no Kind)
kubectl apply -f service-load-balancer.yaml

# Deleta o Service do tipo LoadBalancer
kubectl delete svc servidor-python-service

# Cria o Service do tipo ClusterIP novamente
kubectl apply -f service-cluster-ip.yaml

```

## Criando o primeiro Ingress da aplicação

Digitar no terminal

```bash

# Volta um diretório
cd ..

# Acessa o diretório de criação do Ingress
cd 6.criar-ingress

# Instala o NGINX Ingress Controller para Kind
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.10.0/deploy/static/provider/kind/deploy.yaml

# Verifica o processo de criação dos pods que gerenciam o ingress-nginx-controller

# Cria o recurso de Ingress com base no manifesto
kubectl apply -f ingress.yaml

# Acessa a aplicação via navegador: http://localhost
# OBS: Se http://localhost não funcionar, tente acessar via IP:
# http://127.0.0.1 ou http://0.0.0.0

# Testa a rotação dos pods (load balancing)
for i in {1..10}; do curl http://localhost -w "\n"; done # Linux/Mac
1..10 | ForEach-Object { curl http://localhost; Write-Host "`n" } #PowerShell

```

## Autoscaling, comunicação entre pods e teste de carga

Digitar no terminal

```bash

# Volta um diretório
cd ..

# Acessa a pasta de criação do HPA (Horizontal Pod Autoscaler)
cd 7.criar-hpa

# Acessa a subpasta do metric-server
cd metric-server

# Instala o Metric Server (necessário para HPA funcionar)
kubectl apply -f components.yaml

# Volta ao diretório raiz do HPA
cd ..

# Cria o recurso de HPA
kubectl apply -f hpa.yaml

# Monitora o HPA continuamente (modo watch)
watch -n1 kubectl get hpa # Linux
while ($true) { kubectl get hpa; Start-Sleep -Seconds 1; Clear-Host } # PowerShell

# Abra um outro terminal
# Acessa a pasta do teste de carga
cd 7.criar-hpa
cd teste-de-carga-app

# Cria a imagem Docker do teste de carga
docker build . -t helderprado/teste-carga:1.0

# (Opcional) Testa a imagem localmente, se desejar
docker run --rm -p 8089:8089 helderprado/teste-carga:1.0

# Envia a imagem para o Docker Hub
docker push helderprado/teste-carga:1.0

# Volta ao diretório raiz do HPA
cd ..

# Aplica os recursos do teste de carga (deployment e service)
kubectl apply -f teste-de-carga.yaml

# Verifica se os recursos foram criados com sucesso
kubectl get all

# Faz o redirecionamento para acessar o teste de carga via navegador
kubectl port-forward svc/teste-carga-svc 8089:80

```

## Exclusão de todos os recursos e do cluster Kind

Digitar no terminal

```bash

# Deleta todos os recursos (pods, services, deployments, replicasets, etc.) do namespace padrão
kubectl delete all --all

# Deleta o cluster Kind (substitua o nome se você usou outro)
kind delete cluster --name k8s-cluster

# Deleta todos os containers que estão rodando no Docker
docker rm -f $(docker ps -aq)

```
