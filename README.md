# Projeto Flask de Análise de Prêmios Oscar

Este projeto é uma aplicação Flask que lê dados de um arquivo CSV e os insere em um banco de dados SQLite. A aplicação possui um endpoint que retorna informações sobre o intervalo de tempo entre prêmios ganhos por produtores. Além disso, há um conjunto de testes de integração que garantem a funcionalidade correta da aplicação.

## Estrutura do Projeto
─ script.py
─ test_integration.py
─ archive/
  ─ the_oscar_award.csv
  ─ database.db

## Requisitos

- Python 3.x
- pip (gerenciador de pacotes do Python)
- Flask
- pandas
- pytest

## Configuração do Ambiente Virtual

É altamente recomendável usar um ambiente virtual para isolar as dependências do projeto. Siga as instruções abaixo para configurar um ambiente virtual:

### Windows

1. Crie o ambiente virtual:
```
python -m venv venv
```

2. Ative o ambiente virtual:
```
.\venv\Scripts\activate
```

## Instalação das Dependências
Com o ambiente virtual ativado, instale as dependências necessárias:
```
pip install Flask pandas pytest
```

## Executando a Aplicação
1. Certifique-se de que o arquivo CSV the_oscar_award.csv está no diretório archive.

2. Execute o script principal da aplicação:
```
python script.py
```

A aplicação estará disponível em http://127.0.0.1:5000.

### Endpoint Disponível
GET /award_interval: Retorna o intervalo de tempo entre prêmios ganhos por produtores, bem como o ano do prêmio mais recente e do mais antigo.


## Executando os Testes de Integração
1. Certifique-se de que o pytest está instalado:
```
pip install pytest
```

2. Execute os testes de integração:
``` 
pytest test_integration.py
```

# Arquivo script.py
Este é o arquivo principal da aplicação Flask. Preencha com o conteúdo do script principal.

# Arquivo test_integration.py
Este é o arquivo de teste de integração. Preencha com o conteúdo do arquivo de testes de integração.
