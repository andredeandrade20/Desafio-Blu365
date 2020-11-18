import pandas as pd

## Leitura e otimização do arquivo
chunks = []
for chunk in pd.read_csv('C:/Users/Ygoor/Desktop/Blu365/teste.csv', encoding = 'UTF-8', sep = '|', low_memory=False,chunksize=1000): ### Importante mudar o caminho para a pasta em que o arquivo foi salvo
    chunks.append(chunk)
df = pd.concat(chunks)
df.dropna()

## Quantidade e Soma de todos os acordos, contando com inválidos.
todos = df.loc[df['ValorContrato'] > 0]
s_todos = todos['ValorContrato'].sum()
q_todos = todos['documento'].count()

## Quantidade de cnpjs e cpfs que geraram acordo
cnpjs = df.loc[(df['documento'] > 99999999999) & (df['ValorContrato'] > 0)].documento.count()
cpfs = df.loc[(df['documento'] < 99999999999) & (df['ValorContrato'] > 0)].documento.count()

## Quantidade de valores inválidos por estarem incorretos
incorretos = df.loc[(df['ValorContrato'] != df['ValorParcela']*df['ContratoPlano']) & (df['ValorContrato']>0)].documento.count()

## Quantidade de valores incorretos por não estarem em dia útil
df['n_datas'] = pd.to_datetime(df['DataVencimento,'])
df['uteis'] = df['n_datas'].dt.dayofweek
uteis = df.loc[(df['uteis'] > 4) & (df['ValorContrato'] > 0)].documento.count()

## Quantidade de acordos inválidos total
invalidos = df.loc[(df['ValorContrato'] != df['ValorParcela']*df['ContratoPlano']) | (df['uteis'] > 4) & (df['ValorContrato'] > 0)].documento.count()

##Quantidade e Soma total de acordos que não estão inválidos
total = df.loc[(df['ValorContrato'] != df['ValorParcela']*df['ContratoPlano']) | (df['uteis'] < 5) & (df['ValorContrato'] > 0)]
q_total = total.documento.count()
s_total = total.ValorContrato.sum()

print(' Relatório''\n Quantidade de acordos gerados =',q_todos,'\n Quantidade de acordos inválidos =',invalidos, '\n Inválidos por valores incorretos =', incorretos,'\n Invalidos por dias não úteis =',uteis,'\n Quantidade de acordos válidos =',q_total,'\n Acordos por CPF =',cpfs,'\n Acordos por CNPJ =',cnpjs,'\n Valor de todos os acordos =',s_todos,'R$','\n Valor de todos os acordos válidos =',s_total,'R$')
