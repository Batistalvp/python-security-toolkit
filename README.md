# Python Security Toolkit

Toolkit educacional em Python para estudantes de Análise e Desenvolvimento de Sistemas (ADS). O foco é mostrar, com programas pequenos e legíveis, como automatizar tarefas ligadas a segurança, redes, Linux e Cloud.

## Sobre

O `python-security-toolkit` reúne seis ferramentas de linha de comando. Cada uma resolve um problema simples (gerar hash, validar IP, checar uma porta, ler um log, conferir um arquivo, revisar um JSON de Cloud) e explica o conceito por trás.

O projeto é **defensivo e educacional**. Ele não explora vulnerabilidades, não quebra senhas, não faz varredura em massa e não se conecta a contas reais de nuvem.

## Objetivos

O toolkit combina, na prática:

- **Python**: scripts, funções, arquivos, JSON, exceções e argumentos de linha de comando.
- **Segurança**: hashes, integridade, análise de logs e revisão de configuração.
- **Redes**: IPv4, endereços privados/públicos, TCP e portas.
- **Linux**: a mesma pasta roda no terminal Linux (e também no Windows).
- **Cloud**: leitura de um JSON fictício com erros comuns de configuração.
- **Automação**: tarefas repetitivas viram um comando, em vez de checagem manual.

## Ferramentas

### Hash Generator

Gera SHA-256 de um texto ou de um arquivo. Mostra como hashes ajudam a conferir se um conteúdo mudou. Não recupera o texto original e não quebra senhas.

### IP Validator

Recebe um IPv4, valida o formato e informa se o endereço é privado, público ou loopback. Usa a biblioteca padrão `ipaddress`.

### Port Checker

Tenta **uma** conexão TCP em `127.0.0.1` ou `localhost`, com timeout. Serve para ver se um serviço local está escutando. Não é scanner e recusa hosts não autorizados.

### Log Analyzer

Lê um log fictício, conta eventos, IPs, logins e erros, e destaca padrões repetidos. Mostra a ideia de monitoramento sem usar dados reais de terceiros.

### File Integrity

Calcula SHA-256 de arquivos e compara dois arquivos (ou um arquivo com um hash esperado). Deixa claro se o conteúdo foi alterado.

### Cloud Config Checker

Analisa um JSON de laboratório (armazenamento público, autenticação, criptografia, portas, redes). É uma **simulação**. Não acessa AWS, Azure nem Google Cloud.

## Tecnologias

- Python 3 (biblioteca padrão)
- Git e GitHub (versionamento)
- Linux / Windows (terminal)
- Conceitos de Cloud (configuração, não SDK)

## Instalação

Clone ou abra a pasta do projeto e crie um ambiente virtual.

### Windows (PowerShell)

```powershell
cd python-security-toolkit
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python --version
```

Se a execução de scripts estiver bloqueada no PowerShell, use:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

### Linux

```bash
cd python-security-toolkit
python3 -m venv .venv
source .venv/bin/activate
python --version
```

Instale dependências (neste projeto a lista está vazia de propósito; usamos só a biblioteca padrão):

```bash
python -m pip install -r requirements.txt
```

## Utilização

Execute os comandos a partir da **raiz do projeto**.

### Hash Generator

```bash
python tools/hash_generator.py --text "laboratorio ads" --explain
python tools/hash_generator.py --file examples/sample.log
```

### IP Validator

```bash
python tools/ip_validator.py 192.168.0.10
python tools/ip_validator.py 127.0.0.1
```

### Port Checker

Somente localhost. Exemplo com uma porta qualquer (pode estar fechada):

```bash
python tools/port_checker.py --host 127.0.0.1 --port 8080 --timeout 2
```

### Log Analyzer

```bash
python tools/log_analyzer.py --file examples/sample.log
```

### File Integrity

```bash
python tools/file_integrity.py --file examples/sample.log
python tools/file_integrity.py --file examples/sample.log --compare examples/sample_cloud_config.json
```

### Cloud Config Checker

```bash
python tools/cloud_config_checker.py --file examples/sample_cloud_config.json
```

## Testes

Os testes usam `unittest`, que já vem com o Python.

Na raiz do projeto:

```bash
python -m unittest discover -s tests -v
```

## Estrutura

```
python-security-toolkit/
├── README.md
├── requirements.txt
├── .gitignore
├── tools/                 # programas principais
├── tests/                 # testes automatizados
├── examples/              # log e JSON fictícios
└── docs/                  # conceitos em linguagem simples
```

- `tools/`: código que você executa no terminal.
- `tests/`: verifica entradas válidas, inválidas e erros.
- `examples/sample.log`: log inventado para estudo.
- `examples/sample_cloud_config.json`: configuração de Cloud inventada.
- `docs/concepts.md`: teoria resumida para ADS.

## Conceitos aprendidos

- **Python**: variáveis, tipos, `if`, `for`, funções, listas, dicionários, módulos, arquivos, JSON, `try/except`, `argparse`.
- **Redes**: o que é um endereço IP e a diferença entre rede interna e internet.
- **TCP**: protocolo de conexão usado para “conversar” com um serviço em uma porta.
- **IP**: identificador da máquina na rede; neste projeto trabalhamos com IPv4.
- **Portas**: número (1–65535) que indica qual serviço deve receber a conexão.
- **Hashes**: resumo fixo de um conteúdo; SHA-256 é um algoritmo comum.
- **Integridade**: garantia de que o arquivo não mudou desde a última medição.
- **Logs**: registros de eventos do sistema; base do monitoramento.
- **JSON**: formato de dados usado em APIs e arquivos de configuração.
- **Segurança**: pensar em acesso, alteração e exposição de dados.
- **Cloud**: recursos (armazenamento, portas, autenticação) configurados por política.
- **Automação**: um script reduz trabalho manual e deixa o processo repetível.

## Segurança

Use as ferramentas **somente** em ambientes próprios ou com autorização explícita (seu computador, laboratório da faculdade, VM que você administra).

Não aponte o verificador de porta para redes de terceiros. Não coloque senhas, tokens ou chaves neste repositório. O `.gitignore` já ignora `.env`, chaves e credenciais.

Este projeto **não** inclui exploração de vulnerabilidades, força bruta, malware, evasão ou ataque a sistemas alheios.

## O que este projeto demonstra

Capacidade de usar Python para criar automações pequenas e úteis em segurança, infraestrutura e Cloud: ler arquivos, validar dados, gerar hashes, interpretar JSON e explicar o resultado com clareza — o tipo de habilidade pedida em estágios de ADS.

## Próximos passos

Ideias para evoluir **depois** (não implementadas neste repositório):

- AWS SDK / boto3 para ler buckets e políticas com credenciais de laboratório.
- Azure SDK para o mesmo tipo de checagem em outro provedor.
- Consumo de APIs HTTP de monitoramento.
- Empacotar as ferramentas em **Docker**.
- **CI/CD** (GitHub Actions) para rodar os testes a cada commit.
- **Terraform** para descrever infraestrutura como código.
- Envio de alertas para um painel de monitoramento.
- Guardar resultados em um banco de dados.

Esses itens exigem contas, permissões e cuidado extra com segredos. Comece sempre em ambiente de estudo.
