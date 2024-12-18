import yfinance as yf

def obter_cotacao_moeda(par_moedas):
    try:
        # Baixa os dados do par de moedas
        dados = yf.Ticker(par_moedas)
        historico = dados.history(period="1d")
        
        if not historico.empty:
            preco_atual = historico['Close'][-1]
            preco_abertura = historico['Open'][-1]
            preco_maximo = historico['High'][-1]
            preco_minimo = historico['Low'][-1]

            return {
                "par": par_moedas,
                "preco_atual": preco_atual,
                "preco_abertura": preco_abertura,
                "preco_maximo": preco_maximo,
                "preco_minimo": preco_minimo
            }
        else:
            return {"erro": "Dados não encontrados para o par informado."}
    except Exception as e:
        return {"erro": str(e)}
