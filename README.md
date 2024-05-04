<div align="center">

# Internet das Coisas - Internet of things (IOT)

</div>

# Introdução

No projeto de Concorrência e Conectividade, criamos uma solução em Python. Nela, dispositivos IoT se comunicam com um broker central, que por sua vez facilita a interação com uma interface de controle. Focamos em eficiência e escalabilidade, permitindo múltiplas conexões simultâneas e assegurando uma comunicação fluida e confiável entre dispositivos e a interface do usuário. Essa abordagem não apenas reforça a conectividade na infraestrutura IoT, mas também estabelece uma base sólida para futuras expansões e inovações no campo da Internet das Coisas.

# Broker

Em geral o componente Broker serve de intermediador entre os "Clientes" e os "Dispositivos" e lida tanto com as comunicações TCP/IP e HTTP através da API.

## Arquivo Auxiliar (api.py)

Este arquivo consiste na criação das rotas para que possamos importar e executar a API no arquivo broker.py. Isto foi feito para que o arquivo broker.py não fique poluído. Ademais, vale falar que nele utilizamos rotas POST, GET, PUT e DELETE.

## Arquivo Principal (broker.py)

Agora uma breve explicação sobre cada uma das funções do broker.py.

  - ***main():*** Responsável por criar duas threads, tcp_thread e requisicao_thread, as quais executam as funções tcp_udp_server e requisicao, respectivamente. Entretanto, após isto ele ainda inicia a aplicação Flask.

  - ***tcp_udp_server():***

  - ***receberUdp():***

  - ***pegar_horario_atual_json():***

  - ***enviar_para_api(data_udp, addr):***

  - ***atualizar_dado_api(dado_udp, id):***

  - ***remover_dispositivo(dado_id):***

  - ***remover_requisicao(dado_id):***

  - ***requisicao():***

# Dispositivo

O dispositivo serve para simular um componente IoT. Neste projeto, ele é uma lâmpada que pode ser ligada, desligada ou ter seu brilho alterado remotamente.

## Arquivo Principal (dispositivo.py)

- ***main():*** Essa função é responsável por criar os sockets, iniciar uma comunicação TCP com o broker e criar três threads, que são threads das funções receberTcp, enviarDadoUdp e menu, respectivamente.
  
- ***menu():*** Essa função tem como propósito mostrar o menu de opções e esperar uma entrada do usuário.
  
- ***receberTcp(client):*** Essa função como o nome diz está responsável por aguardar mensagens do Broker e fazer alterações em variáveis quando preciso. Note também que ele recebe um argumento client, o qual guarda a conexão que ele deverá escutar.
    
- ***enviarDadoUdp(client_udp):*** Esta função como o nome fala, tem como responsabilidade enviar os dados continuamente para o Broker. Observe que ele possui um argumento client_udp, este guarda uma conexão assim como a função anterior, contudo essa conexão é UDP ao invés de TCP.

- ***limpar_terminal():*** Esta função tem como responsabilidade limpar o terminal. Para isso, ela verifica o sistema operacional para determinar qual função utilizar. Isto pois para limpar o terminal no "Windows" é diferente de limpar no "Linux".

   `Observação:` Vale ressaltar que boa parte dessas funções possuem um bloco try-catch, visto que realizam operações delicadas. Mais detalhes podem ser encontrados na documentação do código.

# Cliente

O cliente serve para simular uma interface de controle remoto, a qual pode enviar comandos para vários dispositivos com o auxílio do Broker. Observe que essa interface é uma interface de linha de comando (CLI) e não gráfica.

## Arquivo Principal (cliente.py)

- ***main():*** Essa função será responsável pela execução geral do código, incluindo a exibição do menu, a espera de entradas e o encaminhamento de requisições e solicitações para outras funções.

- ***enviarRequisicao(num, comando):*** Esta outra função, como o próprio nome indica, realiza o envio de requisições para a API, utilizando o método POST. Além disso, ela recebe os argumentos num e comando, que representam o identificador (ID) do dispositivo e o comando a ser enviado, respectivamente.

- ***verificaDados():*** Esta função tem como responsabilidade utilizar o método GET para adquirir os dados dos dispositivos, através da API.

- ***limpar_terminal():*** Esta função tem como responsabilidade limpar o terminal. Para isso, ela verifica o sistema operacional para determinar qual função utilizar. Isto pois para limpar o terminal no "Windows" é diferente de limpar no "Linux".

  `Observação:` Vale ressaltar que boa parte dessas funções também possuem um bloco try-catch, visto que realizam operações delicadas. Mais detalhes podem ser encontrados na documentação do código.

# Tecnologias utilizadas

- ***Ferramantas:*** Para o desenvolvimento desta aplicação, utilizamos ferramentas como Insomnia e Visual Studio Code.

- ***Outras:*** Para a produção do código fonte, utilizamos a linguagem de programação Python, além de algumas bibliotecas dessa linguagem, tais como requests, Flask, etc.
  
# Arquitetura da solução
Sobre a arquitetura utilizada para a troca de mensagens podemos citar a conexão "Dispositivo <-> Broker" e "Broker <-> Cliente". Além disso, utilizamos três componentes, sendo eles: dispositivo, broker e cliente. Note que ambos os componentes possuem uma seção contendo mais detalhes.
  
- ***Dispositivo -> Broker:*** A comunicação entre os dispositivos e o broker para o envio de dados foi feita através de sockets, via protocolo TCP/IP. Neste caso, utilizamos o protocolo UDP, pois ao enviarmos dados, a velocidade de envio foi uma prioridade.

     `Observação:` Note que a conexão TCP é inicializada pelo dispositivo, permitindo que o broker envie requisições para os dispositivos conectados sem a necessidade de abrir múltiplas conexões pelo broker, o que demandaria a busca por diversos endereços físicos. No entanto, ele não envia dados utilizando TCP.
  
- ***Broker -> Dispositivo:*** A comunicação entre o broker e os dispositivos para o envio de comandos/requisições foi feita, assim como a comunicação do dispositivo com o broker, usando sockets, via protocolo TCP/IP. Porém, ao contrário da comunicação de dados, utilizamos o TCP, a fim de priorizar a segurança do envio de requisições.
   
- ***Broker <-> Cliente:*** A comunicação entre o broker e o cliente foi realizada por meio de rotas de uma API REST, utilizando verbos como: GET, POST, PUT E DELETE.

  `Definição:` Uma API REST (Representational State Transfer) é uma arquitetura de comunicação que utiliza os princípios do protocolo HTTP para permitir a comunicação entre sistemas distribuídos.

Ademais, ainda precisamos falar sobre a ordem que essas comunicações acontecem, para isso observe a <br/> <em>Figura 1.</em> <br/>

 <div align="center">
   
   ![Logo do Meu Projeto](Imagens/Diagrama.png)
   <br/> <em>Figura 1. Camada de Transporte.</em> <br/>
   
   </div>

Analisando a imagem, mais especificamente na parte "Envio de comandos", fica evidente que todas as informações passam pelo broker, independentemente de serem dados ou comandos. Por exemplo, se desejo enviar uma mensagem remotamente do cliente para um dispositivo, devo adicionar o comando à minha API através de uma rota. Em seguida, o broker utilizará o protocolo TCP/IP para enviar o comando ao dispositivo via TCP. Já na parte "Conexão Dispositivo -> Broker", é nos mostrado que o dispositivo inicia a comunicação TCP, a fim de que o broker identifique e armazene as conexões.
   
# Protocolo de Comunicação entre Dispositivo e Broker

- ***Camada de Aplicação:***
 
   - **Dispositivo:** Sobre o protocolo que o dispositivo utiliza para se comunicar com o broker, devemos abordar que o dispositivo começa criando uma comunicação TCP. Isto apenas para armazenar a conexão no broker. A partir desse ponto, ele cria a comunicação UDP e envia os dados continuamente a cada meio segundo para o broker.
     
       `Observação:` É válido mencionar que os dados enviados via UDP consistem em um dado, seguida pelo endereço IP do dispositivo e a porta que ele utilizou para a comunicação. Além disso, esse dado pode representar o estado de 'Desligado' ou, respectivamente, o brilho atual do dispositivo. Note que para identificar se o dispositivo está ligado basta verificar se o dado é diferente de 'Desligado'.
     
   - **Broker:** Por parte do dispositivo, ele só encaminha mensagens utilizando TCP quando necessário. Para isso, ele verifica se há alguma requisição na API. Se for o caso, ele envia o dado para o respectivo dispositivo através da conexão previamente estabelecida. Esses dados podem ser "Desligar", "Ligar" ou o brilho a ser alterado. Por outro lado, na parte da aplicação, a cada dado que chega, é verificado se o dispositivo já foi armazenado. Se não foi, todos os dados são enviados para a API, incluindo Dado, Id, Endereço e Data. Caso contrário, apenas o Dado é atualizado na API.

  - **Cliente:** O cliente envia os dados para a API quando solicitado. Nesse caso, ele fará uma requisição POST em uma determinada rota, que receberá os dados IP, Num e Dado, respectivamente. Além disso, quando for solicitado um dado de um dispositivo, o cliente apenas fará a leitura dos dados através de outra rota existente.
    
     `Observação:` Os dados do IP são preenchidos automaticamente pela API. Já o número do dispositivo será escolhido pelo usuário e o Dado pode ser "Desligar", "Ligar" ou um inteiro referente ao valor do brilho a ser alterado.
     
- ***Camada de Transporte:***

   - **Dispositivo:** Sobre o protocolo utilizado pelo dispositivo para se comunicar com o broker, é importante mencionar que foi utilizado o protocolo UDP para o envio de dados. A razão para optar pelo UDP em vez do TCP nesse caso é que o User Datagram Protocol (UDP) é caracterizado por uma baixa sobrecarga, uma vez que não incorpora mecanismos de controle de fluxo, retransmissão de pacotes ou garantias de entrega ordenada. Isso o torna mais eficiente em termos de largura de banda e tempo de latência. Além disso, sua natureza sem conexão e sem garantias proporciona uma baixa latência em comparação com o Transmission Control Protocol (TCP), tornando-o ideal para aplicativos que demandam uma resposta rápida e em tempo real, como streaming de áudio e vídeo, bem como jogos online. Em suma, mesmo que ocorra perda de dados, a velocidade de transmissão ainda compensa na maioria dos casos.
     
   - **Broker:** Falando do Broker, ele se comunica com o dispositivo utilizando o protocolo TCP para o envio de comandos. Porque, o Transmission Control Protocol (TCP) oferece confiabilidade ao garantir a entrega, ordem e integridade dos dados, utilizando mecanismos como confirmações de recebimento e retransmissões de pacotes perdidos. Além disso, o TCP inclui algoritmos para controlar o fluxo de dados entre remetente e destinatário, evitando sobrecarga do destinatário, e mecanismos para detectar e reagir a congestionamentos na rede, ajustando dinamicamente a taxa de transmissão. Outro aspecto importante é a garantia de entrega ordenada dos dados, fundamental para aplicativos que exigem essa ordem, como transferências de arquivos e streaming de mídia. Em resumo, utilizamos o TCP porque não queremos perder comandos/requisições.

# Interface da Aplicação (REST)

.....
# Formatação, Envio e Tratamento de Dados

.....
# Tratamento de Conexões Simultâneas

.....
# Desempenho

.....
# Confiabilidade da Solução
Quanto à confiabilidade da solução, ou seja, à segurança das conexões quando o acesso à Internet de um dos componentes é excluído, observa-se que o sistema continua funcionando. Isso ocorre porque há tratamento para exceções geradas ao tentar enviar dados para a API ou ao consumir, por meio do cliente, assim como ao tentar enviar dados via TCP/IP pelo dispositivo. Além disso, o broker não enfrenta esse tipo de problema, pois pode receber conexões de múltiplos dispositivos e clientes, além de substituir as conexões realizadas pela mesma maquina.

# Como Executar

## Etapas:

### 1. Configuração do Ambiente:
   - **Requisitos do Sistema:** Será preciso ter ao menos o Docker instalado na máquina para que seja possível criar a imagem e executá-la.
     
     `Observação:` Caso queira executar sem o Docker você terá que baixar a versão mais recente do Python e instalar a biblioteca requests e Flask.

### 2. Obtenção do Código Fonte:
   - **Clonagem do Repositório:** Você pode utilizar o seguinte comando no terminal para adquirir a aplicação: https://github.com/Emanuel-Antonio/PBL-Redes.git.
   - **Download do Código Fonte:** Caso não tenha o Git na máquina, você pode fazer o download desse repositório manualmente. Vá até o canto superior, selecione "Code" e depois "Download ZIP", e então extraia o arquivo ZIP na sua máquina.

### 3. Configuração da Aplicação:
   - **Arquivos de Configuração:** Abra as pastas "Cliente" e "Dispositivo" e altere nos arquivos "cliente.py" e "dispositivo.py" o endereço IP para o endereço da máquina onde o broker esteja rodando.

### 4. Execução da Aplicação:
   - **Sem Docker:**
     1. Basta ir nos arquivos "broker.py", "dispositivo.py" e "cliente.py", dentro das pastas "Broker", "Dispositivo" e "Cliente", respectivamente, e executá-los um por um no seu editor de texto ou terminal. Observe que para isso será necessário que você tenha o Python na máquina e que possua as bibliotecas requests e Flask dessa linguagem.
        
   - **Com Docker:**
     1. Execute o seguinte comando no terminal dentro das pastas Cliente, Dispositivo e Broker: "docker build -t nome_do_arquivo .", para gerar as imagens, repita três vezes.
     2. Agora execute as imagens usando o comando "docker run --network='host' -it nome_da_imagem" para executar as três imagens criadas, vale ressaltar que esse processo deve ser feito três vezes já que são três imagens distintas.

# Conclusão

.....

