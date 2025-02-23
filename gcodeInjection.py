
import serial
import glob
import time
import random

BAUDRATE = 115200                                                                   # Baudrate para comunicação serial
DELAY = 500                                                                         # Delay em ms entre um comando e outro.      

ENABLE_ALL =                                     False                              # Habilita todas as funçoes (menos a randomica). 
RANDOM_VALUES =                                  False                              # Habilita valores randomicos.
DISABLE_LIMIT_SWITCH =                           False                              # Desabilita fim de curso.
SAVE_EEPROM =                                    False                              # Salva todas as alterações na EEPROM da impressora.
CALIBRATE_ALL_MOTORS =                           False                              # Calibra passos de todos os motores.
CALIBRATE_MAX_FEEDRATES =                        False                              # Calibra valores máxima de feedrates.
CALIBRATE_MAX_ACCELERATION =                     False                              # Calibra valores máxima aceleração.
CALIBRATE_ACCELERATION =                         False                              # Calibra aceleração.
CALIBRATE_ADVANCED =                             False                              # Permite ajustar parâmetros avançados, como jerk.
CALIBRATE_HOME_OFFSET =                          False                              # Habilita o ajuste dos offsets de origem dos eixos para corrigir a posição inicial.
CALIBRATE_HOTEND_PID =                           False                              # Ativa a calibração do PID para controle de temperatura do hotend.
CALIBRATE_Z_PROBLE_OFFSET =                      False                              # Configura o offset da sonda de nivelamento automático em relação ao bico da impressora.
                   
if ENABLE_ALL:                                                                      # Força habilitar todas as funcionalidades caso não estejam habilitadas.
  if CALIBRATE_ALL_MOTORS == False:
    CALIBRATE_ALL_MOTORS = True
  if CALIBRATE_MAX_FEEDRATES == False:
    CALIBRATE_MAX_FEEDRATES = True
  if CALIBRATE_MAX_ACCELERATION == False:
    CALIBRATE_MAX_ACCELERATION == True
  if CALIBRATE_ACCELERATION == False:
    CALIBRATE_ACCELERATION == True
  if CALIBRATE_ADVANCED == False:
    CALIBRATE_ADVANCED == True
  if CALIBRATE_HOME_OFFSET == False:
    CALIBRATE_HOME_OFFSET == True
  if CALIBRATE_HOTEND_PID == False:
    CALIBRATE_HOTEND_PID == True
  if CALIBRATE_Z_PROBLE_OFFSET == False:
    CALIBRATE_Z_PROBLE_OFFSET == True
  if SAVE_EEPROM == False:
    SAVE_EEPROM == True
  if DISABLE_LIMIT_SWITCH == False:
    DISABLE_LIMIT_SWITCH == True


CALIBRATE_X =                                    80                                 # Passos por unidade do eixo X
CALIBRATE_Y =                                    80                                 # Passos por unidade do eixo Y
CALIBRATE_Z =                                    400                                # Passos por unidade do eixo Z
CALIBRATE_E =                                    93                                 # Passos por unidade da extrusora

CALIBRATE_MAX_FEEDRATES_X =                      500                                # Feedrate padrão para o eixo X (500 mm/s).    
CALIBRATE_MAX_FEEDRATES_Y =                      500                                # Feedrate padrão para o eixo Y (500 mm/s).
CALIBRATE_MAX_FEEDRATES_Z =                      5                                  # Feedrate padrão para o eixo Z (5 mm/s).
CALIBRATE_MAX_FEEDRATES_E =                      25                                 # Feedrate padrão para o extrusor (25 mm/s).

CALIBRATE_MAX_ACCELERATION_X =                   500                                # Define o valor máximo de aceleração para o eixo X.
CALIBRATE_MAX_ACCELERATION_Y =                   500                                # Define o valor máximo de aceleração para o eixo Y.
CALIBRATE_MAX_ACCELERATION_Z =                   100                                # Define o valor máximo de aceleração para o eixo Z.
CALIBRATE_MAX_ACCELERATION_E =                   5000                               # Define o valor máximo de aceleração para o eixo E.

CALIBRATE_ACCELERATION_P =                       500                                
CALIBRATE_ACCELERATION_R =                       500                                
CALIBRATE_ACCELERATION_T =                       500                                

CALIBRATE_ADVANCED_B =                           20000                              # Configura o parâmetro 'B' para ajustes avançados.
CALIBRATE_ADVANCED_S =                           0.00                               # Configura o parâmetro 'S' para ajustes avançados.
CALIBRATE_ADVANCED_T =                           0.00                               # Configura o parâmetro 'T' para ajustes avançados.
CALIBRATE_ADVANCED_J =                           0.08                               # Configura o parâmetro 'J' para ajustes avançados.

CALIBRATE_HOME_OFFSET_X =                        0                                  # Define o offset de origem para o eixo X.
CALIBRATE_HOME_OFFSET_Y =                        0                                  # Define o offset de origem para o eixo Y.
CALIBRATE_HOME_OFFSET_Z =                        0                                  # Define o offset de origem para o eixo Z.

CALIBRATE_P =                                    21.73                              # Configura o valor do coeficiente proporcional (P) do PID para o hotend.
CALIBRATE_I =                                    1.54                               # Configura o valor do coeficiente proporcional (I) do PID para o hotend.
CALIBRATE_D =                                    76.55                              # Configura o valor do coeficiente proporcional (D) do PID para o hotend.

CALIBRATE_X_OFFSET =                             -34.99                             # Define o offset para o eixo X em relação à posição padrão.
CALIBRATE_Y_OFFSET =                             -6.99                              # Define o offset para o eixo Y em relação à posição padrão.
CALIBRATE_Z_OFFSET =                             -0.38                              # Define o offset para o eixo Z em relação à posição padrão.


def find_usb_port():
    ports = glob.glob("/dev/ttyUSB*") + glob.glob("/dev/ttyACM*")
    if ports:
        return ports[0]                                                             # Retorna a primeira porta encontrada
    return None

def sendCommand(connection, command):                                               # Formata o envio das mensagens e com feedback
    connection.write("{}\n".format(command).encode())
    print("{}\n".format(command).encode())
    time.sleep(DELAY / 1000)

def formattedCommand(connection, command_template, x=0.0, y=0.0, z=0.0, e=0.0):
    command = command_template.format(x="{:.2f}".format(x), 
                                          y="{:.2f}".format(y), 
                                          z="{:.2f}".format(z), 
                                          e="{:.2f}".format(e))
    sendCommand(connection, command)

def main():
    while True:
        port = find_usb_port()

        if not port:
            print("Nenhuma porta USB encontrada.")
        else:
            print("Conectando na porta: {}".format(port))

            try:
                connection = serial.Serial(port, BAUDRATE, timeout=1)
                time.sleep(2)                                                       # Aguarda a inicialização
                
                if CALIBRATE_ALL_MOTORS == True and RANDOM_VALUES == False:         # CALIBRATE_ALL_MOTORS
                    formattedCommand(connection, "M92 X{x}", x=CALIBRATE_X)
                    formattedCommand(connection, "M92 Y{y}", y=CALIBRATE_Y)
                    formattedCommand(connection, "M92 Z{z}", z=CALIBRATE_Z)
                    formattedCommand(connection, "M92 E{e}", e=CALIBRATE_E)
                elif CALIBRATE_ALL_MOTORS == True and RANDOM_VALUES == True:
                    calibrate_xy = random.uniform(90, 140)
                    formattedCommand(connection, "M92 X{x}", 
                                     x=calibrate_xy)
                    formattedCommand(connection, "M92 Y{y}", 
                                     y=calibrate_xy)
                    formattedCommand(connection, "M92 Z{z}", 
                                     z=random.uniform(450, 800))
                    formattedCommand(connection, "M92 E{e}", 
                                     e=random.uniform(100, 300))

                if CALIBRATE_MAX_FEEDRATES == True and RANDOM_VALUES == False:      # CALIBRATE_MAX_FEEDRATES
                    formattedCommand(connection, "M203 X{x} Y{y} Z{z} E{e}", 
                                    x=float(CALIBRATE_MAX_FEEDRATES_X), 
                                    y=float(CALIBRATE_MAX_FEEDRATES_Y), 
                                    z=float(CALIBRATE_MAX_FEEDRATES_Z), 
                                    e=float(CALIBRATE_MAX_FEEDRATES_E))
                elif CALIBRATE_MAX_FEEDRATES == True and RANDOM_VALUES == True:
                    max_feedrates_xy = random.uniform(60, 100)
                    formattedCommand(connection, "M203 X{x} Y{y} Z{z} E{e}",
                                    x=max_feedrates_xy, y=max_feedrates_xy,
                                    z=random.uniform(3, 10), e=random.uniform(10, 40))

                if CALIBRATE_MAX_ACCELERATION == True and RANDOM_VALUES == False:   # CALIBRATE_MAX_ACCELERATION
                    formattedCommand(connection, "M201 X{x} Y{y} Z{z} E{e}", 
                                    x=float(CALIBRATE_MAX_ACCELERATION_X), 
                                    y=float(CALIBRATE_MAX_ACCELERATION_Y), 
                                    z=float(CALIBRATE_MAX_ACCELERATION_Z), 
                                    e=float(CALIBRATE_MAX_ACCELERATION_E))
                elif CALIBRATE_MAX_ACCELERATION == True and RANDOM_VALUES == True:
                    max_acceleration_xy = random.uniform(60, 100)
                    formattedCommand(connection, "M201 X{x} Y{y} Z{z} E{e}", 
                                    x=max_acceleration_xy, 
                                    y=max_acceleration_xy, 
                                    z=random.uniform(90, 100), 
                                    e=random.uniform(90, 100))

                if CALIBRATE_ACCELERATION == True and RANDOM_VALUES == False:       # CALIBRATE_ACCELERATION
                    formattedCommand(connection, "M204 P{x} R{y} T{z}", 
                                    x=float(CALIBRATE_ACCELERATION_P), 
                                    y=float(CALIBRATE_ACCELERATION_R), 
                                    z=float(CALIBRATE_ACCELERATION_T))
                elif CALIBRATE_ACCELERATION == True and RANDOM_VALUES == True:
                    acceleration_prt = random.uniform(500, 700)
                    formattedCommand(connection, "M204 P{x} R{y} T{z}", x=acceleration_prt, 
                                            y=acceleration_prt, z=acceleration_prt)

                if CALIBRATE_ADVANCED == True and RANDOM_VALUES == False:           # CALIBRATE_ADVANCED
                    formattedCommand(connection, "M205 B{x} S{y} T{z} J{e}", 
                                    x=float(CALIBRATE_ADVANCED_B), 
                                    y=float(CALIBRATE_ADVANCED_S), 
                                    z=float(CALIBRATE_ADVANCED_T), 
                                    e=float(CALIBRATE_ADVANCED_J))
                elif CALIBRATE_ADVANCED == True and RANDOM_VALUES == True:
                    calibrate_advanced_st = random.uniform(0, 20)
                    formattedCommand(connection, "M205 B{x} S{y} T{z} J{e}", 
                                    x=random.uniform(1000, 20000), 
                                    y=calibrate_advanced_st,
                                    z=calibrate_advanced_st, 
                                    e=random.uniform(0, 20))

                if CALIBRATE_HOME_OFFSET == True and RANDOM_VALUES == False:        # CALIBRATE_HOME_OFFSET
                    formattedCommand(connection, "M206 X{x} Y{y} Z{z}", 
                                    x=float(CALIBRATE_HOME_OFFSET_X), 
                                    y=float(CALIBRATE_HOME_OFFSET_Y), 
                                    z=float(CALIBRATE_HOME_OFFSET_Z))
                elif CALIBRATE_HOME_OFFSET == True and RANDOM_VALUES == True:
                    formattedCommand(connection, "M206 X{x} Y{y} Z{z}",
                                    x=random.uniform(-250, 250),
                                    y=random.uniform(-250, 250), 
                                    z=random.uniform(-250, 250))

                if CALIBRATE_HOTEND_PID == True and RANDOM_VALUES == False:         # CALIBRATE_HOTEND_PID
                    formattedCommand(connection, "M301 P{x} I{y} D{z}", 
                                    x=float(CALIBRATE_P), 
                                    y=float(CALIBRATE_I), 
                                    z=float(CALIBRATE_D))
                elif CALIBRATE_HOTEND_PID == True and RANDOM_VALUES == True:
                    formattedCommand(connection, "M301 P{x} I{y} D{z}", 
                                    x=random.uniform(0, 50),
                                    y=random.uniform(-10, 10), 
                                    z=random.uniform(-10, 100))

                if CALIBRATE_Z_PROBLE_OFFSET == True and RANDOM_VALUES == False:    # CALIBRATE_Z_PROBLE_OFFSET
                    formattedCommand(connection, "M851 X{x} Y{y} Z{z}", 
                                    x=float(CALIBRATE_X_OFFSET), 
                                    y=float(CALIBRATE_Y_OFFSET), 
                                    z=float(CALIBRATE_Z_OFFSET))
                elif CALIBRATE_Z_PROBLE_OFFSET == True and RANDOM_VALUES == True:
                    formattedCommand(connection, "M851 X{x} Y{y} Z{z}", 
                                    x=random.uniform(-250, 0),
                                    y=random.uniform(-250, 0), 
                                    z=random.uniform(-250, 0))

                
                if DISABLE_LIMIT_SWITCH == True:                                    # DISABLE_LIMIT_SWITCH
                    sendCommand(connection, "M211 S0")

                if SAVE_EEPROM == True:
                    sendCommand(connection, "M500")                                 # SAVE_EEPROM
                
                connection.close()
                print("Comandos enviados com sucesso.")

            except serial.SerialException as e:
                print("Erro ao conectar ao dispositivo: {}".format(e))
        time.sleep(5)
    
if __name__ == "__main__":
    main()
