import os
import pytest
import json
from script import app, sqlite_db_path, csv_2_db

@pytest.fixture
def client():
    # Use as configurações de teste
    app.config['TESTING'] = True

    # Inicialize o banco de dados de teste
    with app.app_context():
        test_db_path = './archive/test_database.db'
        app.config['sqlite_db_path'] = test_db_path
        csv_2_db()  # Carregue os dados de teste no banco de dados

    with app.test_client() as client:
        yield client

    # Após os testes, limpe o banco de dados de teste
    if os.path.exists(test_db_path):
        os.unlink(test_db_path)

def test_get_award_interval(client):
    # Teste para verificar se a rota '/award_interval' retorna o status 200 OK
    response = client.get('/award_interval')
    assert response.status_code == 200

    # Verifique se o retorno é um JSON válido
    json_data = json.loads(response.data)
    assert isinstance(json_data, dict)
    assert 'min' in json_data
    assert 'max' in json_data
    
    min_data = json_data['min']
    max_data = json_data['max']
    
    # Verifique se os dados mínimos e máximos têm a estrutura esperada
    assert isinstance(min_data, list)
    assert isinstance(max_data, list)
    
    for item in min_data + max_data:
        assert isinstance(item, dict)
        assert all(key in item for key in ['producer', 'interval', 'followingWin', 'previousWin'])

def test_bad_request(client):
    # Teste para verificar se a API retorna erro 400 em caso de erro
    response = client.get('/award_interval?invalid_param=1')
    assert response.status_code == 400
    json_data = json.loads(response.data)
    assert 'error' in json_data
