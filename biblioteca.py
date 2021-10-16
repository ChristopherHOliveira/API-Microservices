# importando funções do SQLalchemy
from sqlalchemy import create_engine
from sqlalchemy.sql import text


# usando o banco de dados contido no arquivo 'bib.db', no formato SQLite
engine = create_engine('sqlite:///bib.db')


# definindo uma classe que herda todas as funcionalidades, métodos e atributos de Exception
class AlunoNaoExisteException(Exception):
    # não há diferenças de execução em relação à Exception
    pass


# função que recebe o parâmetro 'id_aluno' e devolve um dicionário com os dados desse aluno
def consulta_aluno(id_aluno):
    # conectando ao BD
    with engine.connect() as con:
        # selecionando tudo da tabela 'aluno' onde 'id' (coluna na tabela) == 'id_do_aluno'(espaço definido na query SQL)
        sql_consulta = text ("SELECT * FROM aluno WHERE id = :id_do_aluno")
        # executando a query definida em sql_consulta, preenchendo o "espaço" 'id_do_aluno' com o argumento passado em 'id_aluno'
        rs = con.execute(sql_consulta, id_do_aluno = id_aluno)
        # fetchone() para pegar apenas uma linha do resultado
        result = rs.fetchone() # caso hajam mais linhas, executar outro fetchone()
        # se a query retornou 0 linhas
        if result == None:
            # levantar exceção
            raise AlunoNaoExisteException
        # retornando o resultado do SQLalchemy convertido em um dicionário
        return dict(result)


# Função que retorna um lista com um dicionario para cada aluno
def todos_alunos():
    with engine.connect() as con:
        # selecionando tudo da tabela 'aluno'
        sql_consulta = text ("SELECT * FROM aluno")
        # executando a query
        rs = con.execute(sql_consulta)
        # criando uma lista vazia
        resultados = []
        # sempre executar
        while True:
            # pega uma linha do resultado e guarda na var 'result'
            result = rs.fetchone()
            # se o resultado for None
            if result == None:
                # parar
                break
            # guardando o resultado convertido em dicionário na var 'd_result'
            d_result = dict(result)
            # adicionando o resultado na lista 'resultados'
            resultados.append(d_result)
        # retornando o resutado
        return resultados


# função que retorna um lista com um dicionario para cada livro
def todos_livros():
    with engine.connect() as con:
        sql_consulta = text ("SELECT * FROM livro")
        rs = con.execute(sql_consulta)
        resultados = []
        while True:
            result = rs.fetchone()
            if result == None:
                break
            d_result = dict(result)
            resultados.append(d_result)
        return resultados

# função que recebe os dados de um livro e adiciona o livro no banco de dados
def cria_livro(id_livro, descricao):
    with engine.connect() as con:    
        sql_create = text ("INSERT INTO livro (id_livro, descricao) VALUES (:id_livro, :descricao)")
        con.execute(sql_create, id_livro = id_livro, descricao = descricao)


# função que recebe a id de um livro, a id de um aluno e marca o livro como emprestado pelo aluno
def empresta_livro(id_livro, id_aluno):
    with engine.connect() as con:    
        sql_create = text ("UPDATE livro SET id_aluno = :id_aluno WHERE id_livro = :id_livro")
        con.execute(sql_create, id_livro=id_livro, id_aluno=id_aluno)


# função que recebe a id de um livro, e marca o livro como disponível
def devolve_livro(id_livro):
    with engine.connect() as con:    
        sql_create = text ("UPDATE livro SET id_aluno = NULL WHERE id_livro = :id_livro")
        con.execute(sql_create, id_livro = id_livro)


# função que devolve uma lista (de dicionários) dos livros que não estão emprestados
def livros_parados():
    with engine.connect() as con:
        sql_consulta = text ("SELECT * FROM livro WHERE id_aluno ISNULL")
        rs = con.execute(sql_consulta)
        resultados = []
        while True:
            result = rs.fetchone()
            if result == None:
                break
            d_result = dict(result)
            resultados.append(d_result)
        return resultados


# função que recebe o nome do aluno e devolve uma lista (de dicionários) dos livros que estão com o aluno no momento
def livros_do_aluno(nome):
    with engine.connect() as con:    
        sql_consulta = text ('''SELECT id_livro, id_aluno, descricao
                                FROM livro
                                JOIN aluno ON livro.id_aluno = aluno.id
                                WHERE nome = :nome''')
        rs = con.execute(sql_consulta, nome = nome)
        resultados = []
        while True:
            result = rs.fetchone()
            if result == None:
                break
            d_result = dict(result)
            resultados.append(d_result)
        return resultados
