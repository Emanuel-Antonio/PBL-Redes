# Internet das Coisas - IOT

# Introdução

.....
# Broker

.....
# Dispositivo

.....
# Cliente

.....
# Como Executar

## Etapas:

### 1. Configuração do Ambiente:
   - **Requisitos do Sistema:** Será preciso ter ao menos o Docker instalado na máquina para que seja possível criar a imagem e executá-la.

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

