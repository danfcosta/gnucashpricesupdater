# GnuCash Prices Updater

## Objetivo e Motivação

Este script foi criado para auxiliar na obtenção de cotação de ações (ou qualquer ativo negociado na [B3](https://www.b3.com.br) e de cotas de fundos de investimentos (via arquivos da CVM) para importação automática no [GnuCash](https://www.gnucash.org).

Premissa: arquivo do GnuCash deve estar salvo no formato SQLite (o padrão é XML).

*OBS: Tem muito tempo que não programo (pelo menos a lógica ainda está fresca). Meu conhecimento em Python tende a ZERO. Portanto, ignore eventuais atrocidades no código.*

## Instruções

### Configuração de uso

No GnuCash, informar os seguintes dados:
-  Fundos de Investimento:
  - Agrupamentos pré-configurados: FUNDO RF, FUNDO MULTI ou PREVIDENCIA (ver aquivo *settings.py*)
  - Informar o CNPJ (formatado 00.000.000/0000-00)
 - Ações, FIIs de mais ativos negociado na B3:
   - Agrupamento pré-configurados: ACAO, OPCAO, FII (ver aquivo *settings.py*)
   - Informar o ticker do ativo. Ex: PETR4
   
### Configuração da aplicação

Configurações devem ser definidas no arquivo *settings.py*:

### Forma de Uso

```
python main.py
```

Será solicitada data da cotação. Deve ser informado no formato YYYY-MM-DD.

### Importante

No momento, a sequencia é de download do arquivo da CVM e depois da B3. Não coloquei opção de ativar/desativar um ou outro.

### Saída

Tabela *price*  do GnuCash atualizada com os valores encontrados na data informada.
