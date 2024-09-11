# unb-solidarity

## Para rodar o projeto siga os seguintes passos:
1. Verifica a instalação de todos os documentos necessários 
2. Inicia o banco de dados mongoDB
3. Se for necessário, coloque a senha no terminal, verifique como em config.py
4. Coloque no terminal `python run.py ` para iniciar a aplicação

## Relatório de cobertura

O relatório de cobertura está na pasta htmlcov. Para gerar o relatório atualizado:
1. `coverage run -m pytest`
2. `coverage html`
Para gerar a cobertura de testes no terminal:
1. `pytest --cov=app --cov-report=term-missing`

Documentação do projeto:
1. Basta acessar a páginas docs
2. Documentação Doxygen -> docs/html
3. Diagrama do projeto -> docs/
4. Tabela de horas trabalhadas do grupo -> docs/
5. Backlog e sprints -> docs/

Repositório do projeto:
https://github.com/biancands/unb-solidarity

Kanban utilizado:
https://github.com/users/biancands/projects/2

Foi utilizado no código yapf para formatação e pylint para verificação.