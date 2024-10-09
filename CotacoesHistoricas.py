import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import mplcyberpunk

# Selecionando ativos:
lista_tickers = ['BBDC4.SA', 'BBAS3.SA', 'ITUB4.SA', 'SANB4.SA', '^BVSP']

# Coletando dados e gerando tabela:
dados_bancarios = yf.download(lista_tickers, start='2010-01-01', end='2022-04-30')
dados_bancarios = dados_bancarios['Adj Close']

# Lendo arquivo EXCEL com os dados dos meus ativos
lucros_bancos = pd.read_excel(r'lucro_bancos_2010_2022.xlsx')

# Filtrando dados atráves do "index" (data) para período selecionado (2015+):
dados_2015 = dados_bancarios[dados_bancarios.index > '2015-01-01']

# Filtrando dados atráves dos dados_bancarios do ativo selecionado (ITUB4) onde apenas valores menores do que 15 serão mantidos:
# LEMBRANDO: com base no ATIVO SELECIONADO
cotacao_menor_que_15_ITUB4 = dados_bancarios[dados_bancarios['ITUB4.SA'] < 15]

# Separando váriaveis por ativo:
itau = dados_bancarios['ITUB4.SA']
banco_do_brasil = dados_bancarios['BBAS3.SA']
bradesco = dados_bancarios['BBDC4.SA']
santander = dados_bancarios['SANB4.SA']
ibovespa = dados_bancarios['^BVSP']

# CALCULANDO RETORNO (functions):

# Retorno Total:
def retorno_total(lista_cotacoes):
    
    retorno = lista_cotacoes.iloc[-1]/lista_cotacoes.iloc[0] - 1

    return retorno

# Retorno: PERIODOS --> ( Anual == "YE" ), ( Semestral == "6ME" ), ( Trimestral == "QE" ), ( Mensal == "ME" )
def resample_periodo(lista_cotacoes, periodo):

    cotacoes_mensais = lista_cotacoes.resample(f'{periodo}').last()
    retorno_ativo = cotacoes_mensais.pct_change().dropna()

    return retorno_ativo

# Retorno Diário:
def retorno_diario(lista_cotacoes):

    retorno_diario = lista_cotacoes.pct_change().dropna()

    return retorno_diario

# Retorno TOTAL por ativo:
retorno_itau = retorno_total(itau)
retorno_banco_do_brasil = retorno_total(banco_do_brasil)
retorno_bradesco = retorno_total(bradesco)
retorno_santander = retorno_total(santander)
retorno_ibovespa = retorno_total(ibovespa)

# Gerando DataFrame "Retornos", com o retorno total de cada ativo:
retornos_df = pd.DataFrame(
    data = {'retornos': [retorno_bradesco, retorno_banco_do_brasil, retorno_itau, retorno_santander, retorno_ibovespa]},
    index = ['BBDC4.SA', 'BBAS3.SA', 'ITUB4.SA', 'SANB4.SA', '^BVSP']
)
 # Percentual
retornos_df['retornos'] = retornos_df['retornos'] * 100  # transformando em porcentagem
 # Ordenando
retornos_df = retornos_df.sort_values(by='retornos', ascending=False)

# Gráfico - RETORNO:
# Style
plt.style.use('cyberpunk')
# Gráfico Base:
fig, ax = plt.subplots()
ax.bar(retornos_df.index, retornos_df['retornos'])
# Formatando eixo "Y" para PORCENTAGEM
ax.yaxis.set_major_formatter(mtick.PercentFormatter())
plt.xticks(fontsize=11)

# CALCULANDO LUCRATIVIDADE:

# Setando Index ('data')
lucros_bancos = lucros_bancos.set_index('data')
# Calculando percentual de todo o período:
var_lucro_bancos = lucros_bancos.iloc[-1] / lucros_bancos.iloc[0] - 1
# Transformando em Porcentagem
var_lucro_bancos = var_lucro_bancos * 100
# Ordenando
var_lucro_bancos = var_lucro_bancos.sort_values(ascending=False)

# Gráfico LUCRATIVIDADE:
# Style
plt.style.use('cyberpunk')
# Gráfico Base:
fig, ax = plt.subplots()
ax.bar(var_lucro_bancos.index, var_lucro_bancos.values)
# Formatando eixo "Y" para PORCENTAGEM
ax.yaxis.set_major_formatter(mtick.PercentFormatter())
plt.xticks(fontsize=12)

# Comparando Rentabilidade entre Ativos:
# Function de Gráfico de comparação ANUAL
def grafico_long_short_anual(var_long, var_short):
    # Importando Estilo "cyberpunk"
    import mplcyberpunk
    
    # Gráfico Base:
    fig, ax = plt.subplots()
    ax.plot(var_long.index.year, var_long.values, label=var_long.name)
    ax.plot(var_short.index.year, var_short.values, label=var_short.name)
    
    # Forçando a exibir todos os anos:
    ax.set_xticks(var_long.index.year)
    
    # Legenda ( O que cada linha representa )
    ax.legend()
    
    # Titúlos
    ax.set_title(f'{var_long.name} em relação ao {var_short.name}')
    ax.set_ylabel('Percentual Anual')
     
    # Transformando eixo "y" em porcentagem
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1.0)) # xmax=1.0 = indicar que os valores devem ser multiplicados por "100"
        
    return plt.show()

# Function para pegar retorno anual de duas ações, e compara-las ao final retornando uma série e um gráfico.
def long_short_anual(long, short, periodo):
   
    var_long = resample_periodo(long, periodo)
    var_short = resample_periodo(short, periodo)
    outperform = (var_long - var_short) * 100
    
    print(outperform)
    grafico_long_short_anual(var_long, var_short)

# Exemplo:
long_short_anual(itau, santander, 'YE')