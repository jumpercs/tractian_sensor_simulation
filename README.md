# Projeto de Monitoramento de Vibração e Notificação

## Visão Geral

Este projeto consiste em um sistema de monitoramento de vibração de máquinas, incluindo a coleta de dados de vibração, armazenamento, agregação de dados históricos e envio de notificações push em caso de detecção de vibrações elevadas. A arquitetura do sistema é composta por três componentes principais:

1. **Servidor Flask**: Responsável por gerenciar as APIs REST para envio de notificações e recuperação de dados históricos.
2. **Simulador de Vibração**: Um script que simula dados de vibração em três eixos (X, Y, Z) e envia esses dados via WebSocket.
3. **Servidor WebSocket**: Recebe os dados de vibração do simulador, armazena os dados em um arquivo e envia notificações push quando são detectadas vibrações altas.

## Estrutura do Projeto

- `app.py`: Contém a implementação do servidor Flask.
- `simulate.py`: Contém a implementação do simulador de vibração.
- `server.py`: Contém a implementação do servidor WebSocket.
- `data.json`: Arquivo de armazenamento dos dados de vibração.
- `serviceAccountKey.json`: Arquivo de credenciais do Firebase.

## Requisitos

- Python 3.7+
- Flask
- Firebase Admin SDK
- websockets
- asyncio
- httpx

## Instalação

1. Clone o repositório:

   ```sh
   git clone https://github.com/jumpercs/tractian_sensor_simulation.git
   cd tractian_sensor_simulation
   ```

2. Crie um ambiente virtual e ative-o:

   ```sh
   python -m venv venv
   source venv/bin/activate  # No Windows, use `venv\Scripts\activate`
   ```

3. Instale as dependências:

   ```sh
   pip install flask firebase-admin websockets asyncio httpx
   ```

4. Adicione o arquivo de credenciais do Firebase (`serviceAccountKey.json`) na raiz do projeto.

## Uso

### Iniciar o Servidor Flask

1. No terminal, inicie o servidor Flask:

   ```sh
   python app.py
   ```

2. O servidor Flask estará disponível em `http://127.0.0.1:5000`.

### Iniciar o Simulador de Vibração

1. Em outro terminal, inicie o simulador de vibração:

   ```sh
   python simulate.py
   ```

2. O simulador começará a enviar dados de vibração para o servidor WebSocket.

### Iniciar o Servidor WebSocket

1. Em outro terminal, inicie o servidor WebSocket:

   ```sh
   python server.py
   ```

2. O servidor WebSocket começará a receber dados do simulador e armazená-los no arquivo `data.json`.

### Endpoints da API

#### Enviar Notificação

- **Rota**: `/send-notification`
- **Método**: `POST`
- **Descrição**: Envia uma notificação push se as condições permitirem.
- **Parâmetros**:
  - `device_token`: Token do dispositivo para envio da notificação.
  - `title`: Título da notificação.
  - `message`: Mensagem da notificação.

#### Recuperar Histórico de Dados

- **Rota**: `/fetch-history`
- **Método**: `GET`
- **Descrição**: Recupera os últimos 60 registros de dados de vibração armazenados.

#### Recuperar Histórico Agregado

- **Rota**: `/fetch-aggregated-history`
- **Método**: `GET`
- **Descrição**: Recupera os dados de vibração agregados em intervalos de 5 minutos para a última hora.

## Tunelamento com Ngrok

Para expor seu servidor local à internet para testes e desenvolvimento, utilize o Ngrok. Instale e configure o Ngrok seguindo os passos abaixo:

1. Instale o Ngrok seguindo as instruções em [ngrok.com](https://ngrok.com/).

2. Inicie um túnel para seu servidor Flask:

   ```sh
   ngrok http 5000
   ```

3. O Ngrok fornecerá uma URL pública que você poderá usar para acessar seu servidor Flask remotamente.

## Licença

Este projeto está licenciado sob a licença MIT. Consulte o arquivo `LICENSE` para obter mais informações.
