# ROS2/Arduino Serial Motor Demo

Esta é uma demonstração do funcionamento de uma nova versão do projeto SciCoBot, uma interface ROS 2 para um Arduino que executa código de controle de motor diferencial com um módulo L298N. O código correspondente para o Arduino pode ser encontrado [aqui](https://github.com/NatanaelAmil/scicobot_2ino).

## Componentes

O pacote `serial_motor_demo` consiste em quatro nós,`driver.py`, `gui.py`, `find_ports` e `serial_teste`. A ideia é que o driver possa ser executado em um PC embarcado dentro de um robô (por exemplo, um Raspberry Pi), fazendo a interface com o hardware de baixo nível. O driver expõe o controle do motor através de tópicos ROS (veja abaixo), que devem ser publicados pelo software do usuário. Já o GUI fornece uma interface simples para o desenvolvimento e teste de tal sistema. Ela publica e se inscreve nos tópicos apropriados enviando a velocidade e o sentido para os dois motores.

## Driver configuration & usage

O driver possui alguns parâmetros:

- `serial_port` - Porta serial para conectar (padrão `/dev/ttyUSB0`)
- `baud_rate` - Taxa de transmissão serial (padrão `9600`)
- `serial_debug` - Ativa a depuração de comandos seriais (padrão `false`)

Para executar, por exemplo:

```
ros2 run serial_motor_demo driver --ros-args -p serial_port:=/dev/ttyUSB0 -p baud_rate:=9600
```

Ele utiliza os seguintes tópicos:
- `motor_command` -  Inscreve um `MotorCommand`, em rad/s para cada um dos dois motores.

## GUI Usage

Interface gráfica onde pode-se controlar dois motores de forma independente, por entrada PWM (-255 a 255), definindo assim sua orientação e velocidade.

## Find_ports

 * YVocê precisa encontrar a porta serial correta para usar o pacote. Para facilitar, escrevi o `find_ports`. Você pode executá-lo com:
    ```sh-session
    ros2 run serial_motor_demo find_ports
    ```
    Isso imprimirá os caminhos e nomes das portas disponíveis.

## serial_teste

* Para executar este código, você precisa saber o endereço da porta USB (padrão `/dev/ttyUSB0`), a taxa de transmissão (padrão `9600`) e, se quiser usar a escrita serial, precisa saber o nome do tópico para se inscrever (padrão `None`):
    ```sh-session
    ros2 run serial_motor_demo serial_teste --ros-args -p serial_port:=/dev/ttyUSB0 -p baud_rate:=9600 -p subscribe_to:=None
    ```

## TODO

- Update code for send messages for RAW BITES (int ao inves de string)
- Make it work 
