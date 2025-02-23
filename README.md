# G-Code Injection: Ataque de Negação de Serviço a Impressora 3D

## 1. Aviso Legal
Este documento é fornecido apenas para fins educacionais e de pesquisa em hardware hacking. O uso indevido das informações aqui contidas pode ser ilegal e resultar em penalidades criminais. O autor e colaboradores deste repositório não se responsabilizam pelo uso inadequado das informações.

## 2. Entendendo as Limitações da Comunicação Host-to-Host e Dispositivo-Dispositivo no USB
O USB segue uma arquitetura rígida de **host-dispositivo**, onde:
- Um **host (mestre)** gerencia a comunicação e atribui endereços;
- Um **dispositivo (escravo)** responde às solicitações do host, mas não pode iniciar a comunicação;
- Dois **hosts** não podem se comunicar diretamente devido às restrições do protocolo;
- Dois **dispositivos** não podem se comunicar entre si sem um host intermediário.

### 2.1 Por que Dois Hosts USB ou Dois Dispositivos Não Podem se Comunicar?
1. **Ausência de Mecanismo de Negociação** → O USB não possui um protocolo embutido para comunicação direta entre hosts ou entre dispositivos sem um host;
2. **Conflito de Controle do Barramento** → Apenas um host pode gerenciar o barramento USB e atribuir endereços;
3. **Restrições de Hardware e Software** → Os controladores USB geralmente são projetados para atuar como hosts ou dispositivos, mas não ambos simultaneamente.

### 2.2 Alternativas para Comunicação Direta no USB
- **USB OTG (On-The-Go)**: Permite que certos dispositivos alternem entre os papéis de host e dispositivo;
- **USB Bridge (Cabo de Transferência de Arquivos)**: Utiliza um chip intermediário para permitir a comunicação entre hosts;
- **Conversão de Protocolo**: Adaptadores USB-para-Ethernet ou USB-para-Serial podem permitir a comunicação indireta;
- **USB Type-C Dual Role (DRD)**: Permite alternância dinâmica entre host e dispositivo.

## 3. Ataque G-Code Injection como Negação de Serviço
O ataque **G-Code Injection** explora vulnerabilidades na comunicação USB entre um **Banana Pi M2 Zero** e uma impressora 3D para enviar comandos maliciosos, causando falhas no sistema ou danos físicos.

### 3.1 Características do Ataque G-Code Injection
O G-Code Injection é um ataque de **negação de serviço (Denial of Service - DoS)** que visa interromper o funcionamento normal da impressora 3D. Ele pode ser realizado de diferentes formas:
1. **Modificação Persistente**: Alteração de configurações críticas como passos por unidade dos motores (M92), velocidades máximas (M203), aceleração (M201) e parâmetros de PID do hotend (M301);
2. **Substituição Temporária**: Inserção de comandos em tempo real para desativar eixos, alterar temperatura ou provocar falhas de movimentação;
3. **Ataques Randômicos**: Introdução de valores aleatórios para criar falhas imprevisíveis, dificultando a detecção e correção.

### 3.2 Como Funciona o Ataque
A técnica consiste em utilizar o **Banana Pi M2 Zero** como um dispositivo de ataque para interceptar e modificar a comunicação entre um computador e a impressora 3D via USB. O dispositivo atua como um **host USB malicioso**, enviando comandos G-Code que alteram parâmetros críticos da máquina, resultando em falhas na impressão, superaquecimento, colisões mecânicas e até danos físicos à impressora.

### 3.3 Configuração do Ataque no Banana Pi M2 Zero
Para configurar corretamente o ataque no Banana Pi M2 Zero, é necessário ajustar os seguintes parâmetros no código:
- **BAUDRATE**: Define a taxa de transmissão serial com a impressora. O valor padrão é **115200**, mas pode variar conforme o firmware da impressora;
- **DELAY**: Define o tempo de espera (em milissegundos) entre cada comando enviado;
- **ENABLE_ALL**: Se ativado, habilita todas as funções do ataque automaticamente;
- **RANDOM_VALUES**: Se ativado, gera valores aleatórios para os parâmetros de calibração, causando efeitos imprevisíveis na impressora;
- **DISABLE_LIMIT_SWITCH**: Se ativado, desabilita os switches de fim de curso, impedindo a detecção de limites dos eixos;
- **SAVE_EEPROM**: Se ativado, salva todas as alterações diretamente na EEPROM da impressora, tornando as mudanças permanentes;
- **CALIBRATE_ALL_MOTORS**: Se ativado, modifica os passos por unidade de todos os motores da impressora;
- **CALIBRATE_MAX_FEEDRATES**: Se ativado, altera as taxas máximas de deslocamento da impressora;
- **CALIBRATE_MAX_ACCELERATION**: Se ativado, modifica os valores máximos de aceleração dos eixos;
- **CALIBRATE_ACCELERATION**: Se ativado, ajusta a aceleração geral da impressora;
- **CALIBRATE_ADVANCED**: Se ativado, permite ajustar parâmetros avançados, como "jerk";
- **CALIBRATE_HOME_OFFSET**: Se ativado, altera os offsets de origem dos eixos para corrigir a posição inicial da impressão;
- **CALIBRATE_HOTEND_PID**: Se ativado, calibra o PID do hotend para controle de temperatura;
- **CALIBRATE_Z_PROBE_OFFSET**: Se ativado, configura o offset da sonda de nivelamento automático em relação ao bico da impressora.

Além dessas configurações, os seguintes valores podem ser ajustados para definir os parâmetros específicos:
- **Passos por unidade**: `CALIBRATE_X`, `CALIBRATE_Y`, `CALIBRATE_Z`, `CALIBRATE_E`;
- **Taxas máximas de deslocamento**: `CALIBRATE_MAX_FEEDRATES_X`, `CALIBRATE_MAX_FEEDRATES_Y`, `CALIBRATE_MAX_FEEDRATES_Z`, `CALIBRATE_MAX_FEEDRATES_E`;
- **Acelerações máximas**: `CALIBRATE_MAX_ACCELERATION_X`, `CALIBRATE_MAX_ACCELERATION_Y`, `CALIBRATE_MAX_ACCELERATION_Z`, `CALIBRATE_MAX_ACCELERATION_E`;
- **Offsets de origem**: `CALIBRATE_HOME_OFFSET_X`, `CALIBRATE_HOME_OFFSET_Y`, `CALIBRATE_HOME_OFFSET_Z`.
- **Configurações do PID do hotend**: `CALIBRATE_P`, `CALIBRATE_I`, `CALIBRATE_D`.

### 3.4 Como Executar o Ataque no Banana Pi M2 Zero
1. Conecte a impressora 3D ao **Banana Pi M2 Zero** via USB.
2. Ajuste os parâmetros do código conforme desejado, modifique os valores como de calbiração por exemplo, e ao zerar desabilitará o eixo desejado.
3. Execute o código Python no **Banana Pi M2 Zero**.
4. O dispositivo atuará como um host USB, enviando comandos modificados à impressora.
5. Se `SAVE_EEPROM` estiver ativado, as alterações serão armazenadas permanentemente.

### 3.5 Consequências do Ataque
- **Superaquecimento do extrusor** devido a mudanças nas configurações de PID;
- **Aceleração extrema** pode danificar a estrutura da impressora;
- **Mudanças nos passos por unidade** podem gerar peças impressas deformadas;
- **Persistência do ataque** se as configurações forem salvas na EEPROM, exigindo um reset manual.

## 4. Vídeo Demonstrativo
Para ver o ataque G-Code Injection em ação e entender melhor seu impacto na impressora 3D, assista ao vídeo demonstrativo abaixo:

## 5. Possíveis Melhorias
- **Implementação de detecção dinâmica da taxa de transmissão (Autobaud Rate)**;
- **Sistema de Consulta M502**: Automatização de ataques com base nas respostas do comando M502;
- **Suporte a Módulos Host USB**: Melhor compatibilidade com módulos USB host externos;
- **Aprimoramento do uso do Banana Pi M2 Zero** como dispositivo host USB para ataques em impressoras 3D;
- **Adicionar compatibilidade para outros hardwares de mercado como:** M5Stack, ESP32, Flipper e etc. 

