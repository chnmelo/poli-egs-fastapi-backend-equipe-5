# **Back_2025.1 - Observatório de Projetos**

Bem-vindo ao repositório de **Back-End** do **Observatório de Projetos** versão 2.0 da **POLI-UPE**! Este projeto faz parte da disciplina de Engenharia de Software do curso de Engenharia da Computação e foi projetado para oferecer uma plataforma colaborativa, onde projetos acadêmicos e artigos podem ser explorados, submetidos e gerenciados.

**Link deploy produção**: https://poli-egs-frontend-equipe-2.onrender.com/

#### ATENÇÃO: Cuidado para não expor o 'key-admin.json'!!, pois contem informações sensíveis

## 🧰 **Tecnologias Utilizadas**

- 🐍 **Python**: Linguagem principal utilizada no desenvolvimento do back-end.
- ⚡ **FastAPI**: Framework moderno e performático para construção de APIs RESTful.
- 🔥 **Firestore Database**: Banco de dados NoSQL da Google, usado para armazenar dados em tempo real e de forma escalável.
- ☁️ **Render Web Service**: Plataforma utilizada para o deploy automatizado do back-end na nuvem.
- 🐳 **Docker**: Utilizado para criar contêineres, garantindo ambiente consistente de desenvolvimento e produção.

## 🌐 Endpoints:

### 🔧 **Back-end**  
- **URL**: [https://poli-egs-fastapi-backend-equipe-2.onrender.com/docs](https://poli-egs-fastapi-backend-equipe-2.onrender.com/docs)  
- **Descrição**: Este é o endpoint da API desenvolvida com FastAPI. Através dele, é possível visualizar e testar os endpoints disponíveis utilizando a interface interativa gerada automaticamente pela documentação Swagger. Ideal para desenvolvedores entenderem os serviços oferecidos e testarem requisições de forma prática.

## 🧑‍💻 Instruções para Desenvolvedores

### 🔁 Clonar o Repositório

```bash```
```git clone https://github.com/PriscillaIA/poli-egs-fastapi-backend-equipe-2.git```
```cd poli-egs-fastapi-backend-equipe-2```

### 🛠️ Criar e Ativar Ambiente Virtual (Recomendado)

#### Criar o ambiente virtual:
- python -m venv nome_do_seu_ambiente

#### Entrar no venv:
- **🪟 Windows:**
```.\nome_do_seu_ambiente\Scripts\activate```

- **🐧 Linux/Mac:**
```source nome_do_seu_ambiente/bin/activate```

### 📦 Instalar Dependências:

#### Acesse a pasta FastApi e instale os pacotes do projeto:
-  ```pip install -r requirements.txt```

#### Caso esteja usando o VS Code, selecione o interpretador do ambiente virtual:
- C:\Users\NomeUsuario\nome_do_seu_ambiente\Scripts\python.exe

### ▶️ Rodar o Servidor Local:

#### Execute o servidor FastAPI a partir da raiz do projeto:

- Opção 1:
```fastapi dev app.py```

- Opção 2:
```fastapi dev app.py```

- Opção 3 (para expor publicamente):
```uvicorn app:app --host 0.0.0.0 --port 8000```
  - Observação: no comando uvicorn app:app, o primeiro app é o nome do arquivo (app.py) e o segundo é a variável FastAPI definida dentro dele (app = FastAPI()).

### ☁️ Deploy no Servidor Render
- Após um commit na branch configurada, o Render faz o deploy automaticamente. Então, é necessário cadastrar no servidor Render os links do front e back-end
- ⚠️ Atenção: verifique se todas as alterações foram testadas e validadas antes de fazer push, pois o deploy ocorrerá automaticamente.

### 🔐 Variáveis de Ambiente
- É necessário criar um arquivo .env na raiz do projeto com as chaves corretas.
- 📩 Solicite esse arquivo .env a outro desenvolvedor do projeto ou ao dono do sistema se ainda não tiver.

### 🗄️ Banco de Dados:
- Este projeto utiliza Firestore do Firebase como banco de dados NoSQL.
- Peça a outro desenvolvedor do projeto acesso ao banco de dados.

### 🐳 Executando com Docker
Isso executará o backend na porta 8000 do seu host local. Entao voce pode acessar via navegador: http://localhost:8000/docs
- Build da imagem: ```docker build -t your-image-name .```
- Executar o container: ```docker run -p 8000:8000 your-image-name```

#### 🖼️ Exemplo de execução bem-sucedida
![image](https://github.com/user-attachments/assets/3c8c93fb-9a3e-4221-9663-eefa464ccec1)

### 📑 Documentação:

### Tabela de Rastreamento de Funcionalidades
  
  ![image](https://github.com/user-attachments/assets/6062ab5d-879d-45de-9f4f-62ca36cf4b73)

### Especificacao dos Novos Modulos Desenvolvidos:

#### - **Especificações Funcionais - Módulo Produtos** 
[📘 Acessar Documento](https://github.com/PriscillaIA/poli-egs-fastapi-backend-equipe-2/blob/master/documenta%C3%A7%C3%A3o/Especifica%C3%A7%C3%A3o%20Funcional%20-%20M%C3%B3dulo_%20Produtos.pdf)
#### - **Especificações Funcionais - Módulo Gestão de Dúvidas e Sugestões** 
[📘 Acessar Documento](https://github.com/PriscillaIA/poli-egs-fastapi-backend-equipe-2/blob/master/documenta%C3%A7%C3%A3o/Especifica%C3%A7%C3%A3o%20Funcional%20-%20M%C3%B3dulo%20Gest%C3%A3o%20de%20D%C3%BAvidas%20e%20Sugest%C3%B5es.pdf)
#### - **Especificações Funcionais - Módulo Cadastrar Integrantes da Equipe**
[📘 Acessar Documento](https://github.com/PriscillaIA/poli-egs-fastapi-backend-equipe-2/blob/master/documenta%C3%A7%C3%A3o/Especifica%C3%A7%C3%A3o%20Funcional%20-%20Modulo%20Cadastrar%20Integrantes%20Equipe.pdf)

### Gerenciamento do Projeto:

#### - **Matriz de Commits**
[📘 Acessar Documento](https://github.com/PriscillaIA/poli-egs-fastapi-backend-equipe-2/blob/master/documenta%C3%A7%C3%A3o/Matriz%20de%20Controle%20de%20Commites.pdf)
#### - **Regras relacionada ao formato dos commites**
[📘 Acessar Documento](https://github.com/PriscillaIA/poli-egs-fastapi-backend-equipe-2/blob/master/documenta%C3%A7%C3%A3o/Regras%20relacionada%20ao%20formato%20dos%20commites.pdf)
#### - **Exemplo de Sprint Plan**
[📘 Acessar Documento](https://github.com/PriscillaIA/poli-egs-fastapi-backend-equipe-2/blob/master/documenta%C3%A7%C3%A3o/Sprint%20Plan%20Model.pdf)
#### - **Exemplo de documento utilizado nas reunioes com o cliente**
[📘 Acessar Documento](https://github.com/PriscillaIA/poli-egs-fastapi-backend-equipe-2/blob/master/documenta%C3%A7%C3%A3o/Exemplo%20de%20documento%20utilizado%20nas%20reunioes%20com%20cliente.pdf)
#### - **Exemplo de documento utilizado para o gerenciamento das reunioes diarias**
[📘 Acessar Documento](https://github.com/PriscillaIA/poli-egs-fastapi-backend-equipe-2/blob/master/documenta%C3%A7%C3%A3o/Exemplo%20de%20documento%20de%20gerenciamento%20das%20reunioes%20diarias.pdf)
#### - **Exemplo de documento utilizado na retrospectiva da sprint**
[📘 Acessar Documento](https://github.com/PriscillaIA/poli-egs-fastapi-backend-equipe-2/blob/master/documenta%C3%A7%C3%A3o/Exemplo%20de%20documento%20com%20retrospectiva%20da%20sprint.pdf)
#### - **Exemplo de documento How To Do (onde os integrantes compartilharam conhecimentos)**
[📘 Acessar Documento](https://github.com/PriscillaIA/poli-egs-fastapi-backend-equipe-2/blob/master/documenta%C3%A7%C3%A3o/Exemplo%20de%20documento%20explicando%20Como%20Fazer%20as%20coisas.pdf)

#### Caso de Testes Criados:

#### - **Casos de Testes para o Modulo Produtos**
[📘 Acessar Documento](https://github.com/PriscillaIA/poli-egs-fastapi-backend-equipe-2/blob/master/documenta%C3%A7%C3%A3o/Casos%20de%20Teste%20para%20Modulo%20Projetos.pdf)
#### - **Casos de Testes para o Modulo Gestão de Dúvidas e Sugestões**
[📘 Acessar Documento](https://github.com/PriscillaIA/poli-egs-fastapi-backend-equipe-2/blob/master/documenta%C3%A7%C3%A3o/Casos%20de%20Testes%20para%20Modulo%20Gest%C3%A3o%20de%20D%C3%BAvidas%20e%20Sugest%C3%B5es.pdf)
#### - **Casos de Testes para o Modulo Informacoes sobre Integrantes da Equipe**
[📘 Acessar Documento](https://github.com/PriscillaIA/poli-egs-fastapi-backend-equipe-2/blob/master/documenta%C3%A7%C3%A3o/Casos%20de%20Teste%20Exibir%20Informa%C3%A7%C3%B5es%20da%20Equipe.pdf)
#### - **Casos de Testes para o Modulo Projetos**
[📘 Acessar Documento](https://github.com/PriscillaIA/poli-egs-fastapi-backend-equipe-2/blob/master/documenta%C3%A7%C3%A3o/Casos%20de%20Testes%20para%20Modulo%20Produtos.pdf)
#### - **Casos de Testes para o Modulo Artigos**
[📘 Acessar Documento](https://github.com/PriscillaIA/poli-egs-fastapi-backend-equipe-2/blob/master/documenta%C3%A7%C3%A3o/Casos%20de%20Testes%20para%20Modulo%20Artigos.pdf)

### Bugs e Task Levantadas para Futura Implementacao
[📘 Acessar Documento](https://github.com/PriscillaIA/poli-egs-fastapi-backend-equipe-2/blob/master/documenta%C3%A7%C3%A3o/Back-end%20-%20Error%20de%20token%20quando%20usu%C3%A1rio%20adm%20tenta%20aprovar%20ou%20reprovar%20artigo%20quando%20o%20usu%C3%A1rio%20esta%20logando%20a%20muito%20tempo.pdf)

[📘 Acessar Documento](https://github.com/PriscillaIA/poli-egs-fastapi-backend-equipe-2/blob/master/documenta%C3%A7%C3%A3o/Refatoramento%20do%20c%C3%B3digo%20de%20back%20-%20melhoria%20do%20codigo.pdf)

[📘 Acessar Documento](https://github.com/PriscillaIA/poli-egs-fastapi-backend-equipe-2/blob/master/documenta%C3%A7%C3%A3o/%5BDatabase%5D%20os%20pdf%20ou%20imagens%20dos%20projetos%2C%20artigos%20ou%20produtos%20exclu%C3%ADdos%20pela%20interface%20do%20usu%C3%A1rio%20n%C3%A3o%20est%C3%A3o%20sendo%20exclu%C3%ADdos%20do%20banco%20de%20dados.pdf)

[📘 Acessar Documento](https://github.com/PriscillaIA/poli-egs-fastapi-backend-equipe-2/blob/master/documenta%C3%A7%C3%A3o/%5BFront%20e%20Back%5D%5BLogin%5D%20Credenciais%20de%20login%20est%C3%A3o%20sendo%20enviadas%20via%20query%20string%20(risco%20de%20seguran%C3%A7a).pdf)

[📘 Acessar Documento](https://github.com/PriscillaIA/poli-egs-fastapi-backend-equipe-2/blob/master/documenta%C3%A7%C3%A3o/%5BFront-end%5D%5BModal%20Cadastrar%20novo%20Artigo%5D%20Sistema%20n%C3%A3o%20faz%20verifica%C3%A7%C3%A3o%20de%20campos%20obrigat%C3%B3rios.pdf)

## Storys Trabalhas no Observatorio 2.0 no (Jira app)
![one](https://github.com/user-attachments/assets/c3756aa9-f72a-4fbb-8b50-ea0312f40e17)
![two](https://github.com/user-attachments/assets/75063b13-992d-4b04-909c-57494d849471)
![three](https://github.com/user-attachments/assets/29e5b8c3-5d4e-4b2f-a362-75eed44529e2)
![four](https://github.com/user-attachments/assets/1415f5ac-ead3-4cf1-854b-cd57e7a573d3)
![five](https://github.com/user-attachments/assets/146a8adc-60c9-4144-b971-56b84059abbd)

### Equipe 2 do semestre 2025.1:
- **IAN TEIXEIRA PIMENTEL (DEV FRONT-END E BACK-END)**
- **JULIANA DANZI D'AMORIM FERREIRA (DEV FRONT-END E BACK-END)**
- **ALICE GALVÃO VASCONCELOS (DEV FRONT-END E BACK-END)**
- **PRISCILLA DE SOUZA SILVA (SCRUM, PO, TESTER E DEV FRONT-END)**
- **SILVIO ANDRÉ VITAL JUNIOR (GERENTE DE PROJETO)**
- **ARTHUR SOBRAL DE MACÊDO (DEV FRONT-END E BACK-END)**


