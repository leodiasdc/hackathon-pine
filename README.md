# PineBot

## Rodar localmente

Você deve primeiro preencher as variáveis de ambiente no arquivo `.env.example` e, após isso, trocar o nome desse arquivo para `.env` para rodar a aplicação em NextJS. 
Para isso, você vai precisar acessar um servidor de banco de dados em `PostgreSQL`, setar uma API Key para o `Cohere` e para o `LangChain`. 

Após isso, você pode baixar o `pnpm` ou `yarn` para rodar a aplicação. 

```bash
pnpm install
pnpm dev
```
Para acessar o Back-End, instale todos os `requirements.txt` localizados na pasta `/backend` e inicialize a aplicação. 

```bash
python3 app.py
```
O aplicativo deve estar rodando localmente na porta [localhost:3000](http://localhost:3000/).

