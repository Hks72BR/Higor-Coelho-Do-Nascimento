# Conta Digital Dock 

# Introdução 
A aplicação desenvolvida é uma API para gerenciamento de contas digitais, onde é possível criar e remover portadores (clientes), criar contas digitais, consultar saldos, realizar depósitos, saques, e gerar extratos. Também inclui funcionalidades para bloquear e desbloquear contas, garantindo que operações como saques e depósitos só sejam realizadas em contas ativas e desbloqueadas.

# Tecnologias Utilizadas

Linguagem de Programação: Python

Por que Python? Python foi escolhido pela sua simplicidade e eficiência na escrita de código. Sua sintaxe clara e concisa facilita o desenvolvimento rápido e a manutenção do código. Além disso, Python possui uma vasta quantidade de bibliotecas e frameworks que suportam o desenvolvimento web, como Flask e SQLAlchemy.

# Frameworks:

Flask: Um microframework para desenvolvimento web em Python. Foi escolhido devido à sua leveza e flexibilidade, permitindo uma estrutura de aplicação simples e eficiente.
SQLAlchemy: Uma biblioteca ORM (Object Relational Mapper) que facilita a interação com bancos de dados SQL. Foi escolhida pela sua capacidade de mapear modelos de dados de forma declarativa e por oferecer uma interface de alto nível para operações de banco de dados.
Funcionalidades da Aplicação

# Gerenciamento de Portadores:

Criação de Portadores: Permite a criação de novos portadores fornecendo nome completo e CPF. O CPF deve ser único e válido.
Remoção de Portadores: Permite a remoção de portadores existentes. Todas as contas associadas ao portador são excluídas automaticamente.
Gerenciamento de Contas:

# Criação de Contas: 

Permite a criação de contas digitais associadas a um portador existente, utilizando o CPF do portador.
Consulta de Contas: Permite a consulta de saldo, número da conta e agência.
Fechamento de Contas: Permite que um portador feche sua conta a qualquer momento.
Operações Financeiras:

# Depósitos: 

Permite a realização de depósitos em contas ativas e desbloqueadas.

# Saques: 
Permite a realização de saques em contas ativas e desbloqueadas, desde que haja saldo disponível e que não ultrapasse o limite diário de 2 mil reais.

# Consulta de Extrato: 
Permite a consulta do extrato da conta por um período especificado.

# Segurança e Regulação:

Bloqueio e Desbloqueio de Contas: Permite o bloqueio e desbloqueio de contas a qualquer momento. Operações financeiras só podem ser realizadas em contas desbloqueadas.

# Proibição de Saldo Negativo: 
A aplicação garante que uma conta nunca possa ter saldo negativo.
Estrutura do Código
O código está organizado em módulos, separando claramente as responsabilidades:

models.py: Define os modelos de dados Portador e Conta utilizando SQLAlchemy.
routes.py: Define as rotas da API utilizando Flask. Inclui endpoints para todas as operações mencionadas acima.
validations.py: Contém funções de validação, como a validação de CPF.
Configuração e Execução
Para configurar e executar a aplicação localmente, siga os passos abaixo:

# Clone o repositório:

sh
Copiar código
git clone <URL do Repositório>
cd <Nome do Repositório>

# Crie um ambiente virtual:

sh
Copiar código
python -m venv venv
source venv/bin/activate  # No Windows use `venv\Scripts\activate`

# Instale as dependências:

sh
Copiar código
pip install -r requirements.txt

# Configure o banco de dados:

sh
Copiar código
flask db init
flask db migrate
flask db upgrade

# Execute a aplicação:

sh
Copiar código
flask run
Testando com Postman:

# Criação de Portadores:

Método: POST
URL: http://127.0.0.1:5000/portadores
Body (JSON): { "nome_completo": "John Doe", "cpf": "12345678901" }

# Remoção de Portadores:

Método: DELETE
URL: http://127.0.0.1:5000/portadores/1 (Substitua 1 pelo ID do portador)
**Demais funcionalidades podem ser testadas seguindo a documentação dos endpoints definidos em routes.py.

# Conclusão

Esta aplicação demonstra a capacidade de gerenciar contas digitais de forma eficiente e segura. A escolha de Python, Flask e SQLAlchemy permitiu desenvolver uma API robusta e de fácil manutenção, atendendo às necessidades de expansão e inovação da Dock no mercado financeiro.