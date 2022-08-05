from secrets import token_hex
from fastapi import FastAPI
from model import Pessoa, Tokens, conect_banco
from hashlib import sha256
import re

app = FastAPI()
session = conect_banco()

#FastAPI
#Validação de email
#Coloquei a senha com o sha256 no BD
#Quando o usuário for logar ele gera um token que é salvo na tabela TOKENS
#Utilização do SqlAlchemy para se conectar ao MySQL






@app.post('/cadastrar')
def cadastrar_bd(nome:str, email:str, senha:str):
    try:
        #Puxando os dados do usuário de acordo com o email inserido e retorna uma lista
        x = session.query(Pessoa).filter_by(email=email).all()

        #Caso o email inserido não exista no BD ele irá registrar.
        if len(x) == 0:
            if re.search('\w*@\w*\.w*',email):
                x = Pessoa(nome=nome, email=email, senha= sha256(senha.encode()).hexdigest())
                session.add(x)
                session.commit()
                return 'Cadastrado com Sucesso.'
            else:
                return 'Insira um email valido.'

        #Caso o email inserido já exista ele irá retornar:
        else:
            return 'Usuario já cadastrado.' 

    except:
        return 'ERRO ao cadastrar.'

@app.post('/logar')
def login_user(email: str, senha: str):
    #Transformando a senha inserida em hash para comparar com a senha que está no BD.
    senha_code = sha256(senha.encode()).hexdigest()
    
    try:
        #Caso insira email não cadastrado.
        x = session.query(Pessoa).filter_by(email=email, senha=senha_code).all()
        if len(x) == 0:
            return 'Usuário não cadastrado.'
        

        #Gera um novo token a cada vez que o usuário logar

        while True:
            #Gerando um token 
            token = token_hex(50)
            token_existe = session.query(Tokens).filter_by(token=token).all()
           

            if len(token_existe) == 0:
                pessoa_existe = session.query(Tokens).filter_by(id_pessoa=x[0].id).all()
                
                #Caso o usuário nunca tenha logado consequentemente ele não terá nenhum token registrado ao seu id_pessoa, portanto nesse if irá  adicionar um token (já gerado) ao seu id_pessoa.
                if len(pessoa_existe) == 0:
                    novo_token = Tokens(id_pessoa=x[0].id, token=token)
                    session.add(novo_token)
                
                #Caso o usuário ja tenha logado o elif irá apenas dar um update no token antigo para o novo token.
                elif len(pessoa_existe) > 0:
                    pessoa_existe[0].token = token
                    
                session.commit()

                break
        return 'LOGADO COM SUCESSO'

    except:
        'ERRO AO LOGAR'
         




    