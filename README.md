# ROS2/Arduino Serial Motor Demo

Esta é uma demonstração do funcionamento de uma nova versão do projeto SciCoBot, uma interface ROS 2 para um Arduino que executa código de controle de motor diferencial com um módulo L298N. O código correspondente para o Arduino pode ser encontrado [aqui](https://github.com/RoboPatos/scicobot_2ino).

## Componentes

O pacote `serial_motor_demo` consiste em três arquivos,`driver.py`, `gui.py` e `find_ports`. A ideia é que o driver possa ser executado em um Raspberry Pi. Já o GUI fornece uma interface simples para o desenvolvimento e teste de tal sistema. Ela publica e se inscreve nos tópicos apropriados enviando a velocidade e o sentido para os dois motores.

O GUI envia os valores diretamente para o `driver`, portanto devem ser executados juntos, porém pela falta de interface no ROS2, se faz necessário duas máquinas. O `driver` roda diretamente no raspberry PI com o Arduino em sua porta serial e o `gui` roda em um computador físico Ubuntu 22.04. O arquivo `find_ports` serve apenas para verificar se o arduino consegue ser lido pelo minicomputador e ajudar a configurar os parâmetros de conexão do `driver`.

## Buildando os pacotes

 * Para instalar, primeiro forneça sua instalação do ROS 2:
```
source /opt/ros/humble/setup.bash
```
 * Crie um diretório para o projeto:
```
mkdir -p ~/scicobot/src
cd ~/scicobot/src
```
 * Baixe o projeto com:
```
git clone https://github.com/Robopatos/serial_motor_demo.git
```
 * Volte para a pasta root com:
```
cd ..
```
 * Verifique as dependências com:
```
rosdep install -i --from-path src --rosdistro humble -y
```
 * Caso tenha sucesso, contrua o projeto com:
```
colcon build --symlink-install
```
 * Nota: Devido a limitação de hardware do raspberry o processo de build pode travar. Para esse caso, use a solução descrita [aqui](https://answers.ros.org/question/407554/colcon-build-freeze-a-raspberry-pi/). Essa solução altera o build em paralelo, padrão do colcon, para um build sequencial:
```
colcon build --executor sequential
```
Termine com:
```
source install/setup.bash
```

## Driver

 * O driver possui alguns parâmetros:

- `serial_port` - Porta serial para conectar (padrão `/dev/ttyUSB0`)
- `baud_rate` - Taxa de transmissão serial (padrão `9600`)
- `serial_debug` - Ativa a depuração de comandos seriais (padrão `false`)

 * Execute com:

```
ros2 run serial_motor_demo driver --ros-args -p serial_port:=/dev/ttyUSB0 -p baud_rate:=9600
```

## GUI

* Interface gráfica onde pode-se controlar dois motores de forma independente, por entrada PWM (-255 a 255), definindo assim sua orientação e velocidade.Pode ser acessada com:

```
ros2 run serial_motor_demo gui
```

## Find_ports

 * Isso imprimirá no terminal os caminhos e nomes das portas disponíveis no raspberry PI. Você pode executá-lo com:
    ```
    ros2 run serial_motor_demo find_ports
    ```

## Referências
 * ROS/Arduino Serial Motor Demo - [aqui](https://github.com/joshnewans/serial_motor_demo.git);
 * Aros2duino - [aqui](https://github.com/erenkarakis/Aros2duino.git);

## Montagem

O conteudo relacionado à montagem e os scrips para o Arduino podem ser encontrados[aqui](https://github.com/RoboPatos/scicobot_2ino). Para um melhor entendimento do circuito, acompanhe a tabela e a figura abaixo:

            TABELA DE LIGAÇÃO

      Arduino      |     Ponte H
      --------------------------------
         5V        |       +12V
      --------------------------------
        GND        |        GND
      --------------------------------
         5V        |        +5V
      --------------------------------
         D3        |        IN2
      --------------------------------
         D4        |        IN1
      --------------------------------
         D5        |        ENB
      --------------------------------
         D6        |        ENA
      --------------------------------
         D7        |        IN4
      --------------------------------
         D8        |        IN3
      --------------------------------
       * Remover jumper do VLogic

<p align="center">
  <img src="https://github.com/RoboPatos/scicobot_2ino/blob/main/outros_arquivos/Montagem_comentada.png"/ height="700" width="1080">
</p>

## Nota de desenvolvimento - Melhorias

 * Adicionar botôes `Dinâmico` e `Parar dinâmico` que enviam automaticamente os valores para ambos motores, sem a necessidade de apertar o botão enviar o tempo todo.
 * Implementar código que escreve envia números de 1 a 7 na porta serial selecionada para comunicar com o projeto [scicobot_1-7](https://github.com/RoboPatos/scicobot_2ino/blob/main/outros_c%C3%B3digos/scicobot_1-7/scicobot_1-7.ino).
 * Implementar código para leitura de dados de algum sensor ligado no Arduino.
