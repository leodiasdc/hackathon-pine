import yfinance as yf

def obter_cotacao_moeda(par_moedas):
    try:
        # Baixa os dados do par de moedas
        dados = yf.Ticker(par_moedas)
        historico = dados.history(period="1d")
        
        if not historico.empty:
            preco_atual = round(historico['Close'][-1], 2)
            preco_abertura = round(historico['Open'][-1], 2)
            preco_maximo = round(historico['High'][-1], 2)
            preco_minimo = round(historico['Low'][-1], 2)
            preco_atual = f"{preco_atual :.2f}".replace('.', ',')
            preco_abertura = f"{preco_abertura :.2f}".replace('.', ',')
            preco_maximo = f"{preco_maximo :.2f}".replace('.', ',')
            preco_minimo = f"{preco_minimo :.2f}".replace('.', ',')

            return f"O par de moedas informado {par_moedas} tem preço atual de {preco_atual}. O preço máximo do dia foi {preco_maximo}. O preço mínimo foi {preco_minimo}. O preço de abertura foi de {preco_abertura}"
        else:
            return {"erro": "Dados não encontrados para o par informado."}
    except Exception as e:
        return {"erro": str(e)}
