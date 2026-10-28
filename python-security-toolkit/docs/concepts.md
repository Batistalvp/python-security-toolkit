# Conceitos do Python Security Toolkit

Texto para quem está começando ADS. A ideia é ligar o que você vê no código com o que aparece em redes, Linux, Cloud e segurança.

## Python (o essencial deste projeto)

- **Variável**: nome que guarda um valor, por exemplo `port = 8080`.
- **Tipos**: `str` (texto), `int` (inteiro), `bool` (verdadeiro/falso), `list`, `dict`.
- **Condicional**: `if` / `elif` / `else` escolhem um caminho.
- **Loop**: `for` percorre linhas de um log ou itens de uma lista.
- **Função**: bloco reutilizável (`def nome():`). Facilita testar o programa.
- **Lista**: sequência, como a lista de portas `[22, 80]`.
- **Dicionário**: pares chave → valor, como o JSON de Cloud virando `config["storage_public"]`.
- **Módulo**: outro arquivo Python que você importa (`import hashlib`).
- **Arquivos**: `open` / `Path` para ler logs e JSON.
- **JSON**: texto estruturado que vira dicionário com `json.load`.
- **Exceções**: `try/except` quando o arquivo não existe ou o IP é inválido.
- **CLI**: `argparse` lê `--file` e `--port` digitados no terminal.

Classes foram evitadas de propósito. Funções e dicionários bastam e são mais fáceis de explicar em entrevista.

## Redes, IP, TCP e portas

Um **endereço IPv4** tem quatro números de 0 a 255, como `192.168.0.10`.

- **Privado**: redes internas (`10.x`, `192.168.x`, `172.16–31.x`).
- **Público**: endereços roteáveis na internet.
- **Loopback**: `127.0.0.1` é “esta própria máquina”.

**Porta** é o número do serviço. HTTP costuma usar 80, HTTPS 443, SSH 22. O **TCP** tenta estabelecer uma conexão: se alguém está escutando, a porta “aceita”; se não, a conexão é recusada ou o tempo esgota.

O Port Checker testa **uma** porta em localhost. Isso é diagnóstico, não ataque. Varredura de várias portas em redes alheias é uso indevido.

## Hashes e integridade

Um **hash** (aqui, SHA-256) é uma impressão digital do conteúdo:

1. O mesmo arquivo gera o mesmo hash.
2. Qualquer alteração muda o hash.
3. Você não “desfaz” o hash para obter o arquivo original.

**Integridade** é a pergunta: “isto ainda é o mesmo conteúdo?”. Hash igual → provavelmente sim. Hash diferente → o arquivo mudou (edição, corrupção ou troca).

Hashes **não** substituem autenticação e **não** devem ser usados como forma de “descobrir senha”.

## Logs e monitoramento

**Log** é um diário do sistema: horário, tipo (INFO, WARN, ERROR) e mensagem.

Em segurança, analisar logs ajuda a ver:

- muitas falhas de login seguidas;
- o mesmo IP repetido;
- erros de banco ou firewall.

No laboratório usamos `examples/sample.log`, com dados **fictícios**. Em um emprego, logs reais podem conter IPs e usuários: trate com cuidado e permissão.

## Cloud (versão laboratório)

Na nuvem, um bucket público, uma porta 22 aberta para `0.0.0.0/0` ou autenticação desligada são erros clássicos.

Este projeto **não liga** na AWS/Azure/GCP. Ele lê um JSON e aplica regras simples, como um checklist. Isso ensina o raciocínio. Auditoria de verdade usa contas, IAM, APIs e evidências.

## Linux e automação

No Linux (e no Windows) você abre o terminal, ativa o `.venv` e roda `python tools/...`. Automatizar é transformar um checklist mental em comando repetível, com testes para não quebrar no próximo exercício.

## Boas práticas de segurança neste repositório

- Só localhost no teste de porta.
- Nada de senha, token ou chave no Git.
- Sem força bruta, malware ou exploração.
- Sempre avisar que o uso é educacional.

Quando for explicar o projeto em um estágio, conte: o problema, o comando, a função principal e o conceito (hash, IP, TCP, log ou configuração de Cloud). Isso mostra que você entende o código, não só copiou a pasta.
