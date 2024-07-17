import pandas as pd
from flask import Flask, jsonify, request, abort
import sqlite3
import json

app = Flask(__name__)

def award_interval():
    conn = sqlite3.connect(':memory:')

    file_path = './archive/the_oscar_award.csv'
    try:
        # Lendo o arquivo CSV
        data = pd.read_csv(file_path)
        # Conectando no SQLite em memória
        # conn = sqlite3.connect(':memory:')
        # Criando a tabela com base no conteúdo do arquivo
        data.to_sql('tb_award', conn, if_exists='replace', index=False)

        # conn.close()
        
    except FileNotFoundError:
        raise Exception(f"Erro: O arquivo '{file_path}' não foi encontrado.")
    except pd.errors.EmptyDataError:
        raise Exception("Erro: O arquivo está vazio.")
    except pd.errors.ParserError:
        raise Exception("Erro: Erro ao analisar o arquivo.")
    except Exception as e:
        raise Exception(f"Ocorreu um erro: {e}")
    
    try:
        # Conectando ao banco de dados SQLite em memória
        # conn = sqlite3.connect(':memory:')
        cursor = conn.cursor()
        
        # Executando o script SQL para obter o valor máximo e mínimo da coluna especificada
        cursor.execute("""
            WITH IntervalData AS (
                SELECT name AS producer, 
                       MAX(year_ceremony) - MIN(year_ceremony) AS interval, 
                       MAX(year_ceremony) AS followingWin, 
                       MIN(year_ceremony) AS previousWin 
                FROM tb_award 
                GROUP BY name 
                HAVING COUNT(DISTINCT film) > 1 
            ),
            MinMax AS (
                SELECT MIN(interval) AS min_interval, MAX(interval) AS max_interval 
                FROM IntervalData
            )
            SELECT producer, interval, followingWin, previousWin 
            FROM IntervalData 
            WHERE interval = (SELECT min_interval FROM MinMax) 
               OR interval = (SELECT max_interval FROM MinMax)
            ORDER BY interval
        """)
        results = cursor.fetchall()
        
        conn.close()
        
        if results and len(results) > 0:
            min_interval = []
            max_interval = []
            
            for row in results:
                item = {
                    "producer": row[0],
                    "interval": row[1],
                    "followingWin": row[2],
                    "previousWin": row[3]
                }
                
                if row[1] == results[0][1]:  # Se for o intervalo mínimo
                    min_interval.append(item)
                elif row[1] == results[-1][1]:  # Se for o intervalo máximo
                    max_interval.append(item)
            
            return json.dumps({"min": min_interval, "max": max_interval}, indent=4)
        
    except sqlite3.Error as e:
        raise Exception(f"Ocorreu um erro ao acessar o banco de dados: {e}")

@app.route('/award_interval', methods=['GET'])
def get_award_interval():
    if 'invalid_param' in request.args:
        return jsonify({'error': 'Parâmetro inválido'}), 400
    
    try:
        interval = award_interval()
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
    # Não encontrou nenhum item no banco de dados
    if not interval:
        abort(404)

    return interval, 200

# Tratamento de erro personalizado para 404
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

# Tratamento de erro personalizado para 400
@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad request'}), 400

if __name__ == '__main__':
    app.run(debug=True)
