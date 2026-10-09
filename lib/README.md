# Dependência de busca

`search.jar` é uma dependência do tutorial oficial, preservada localmente e ignorada no Git. Antes de compilar, o lançador a recupera do ZIP oficial caso esteja ausente e confere os hashes do pacote e do arquivo. Não extrai outros arquivos do ZIP nem substitui silenciosamente uma versão diferente.

Origem: https://raw.githubusercontent.com/jacamo-lang/jacamo/main/doc/tutorials/gold-miners/initial-gold-miners.zip

SHA-256 do JAR: `290e21c7300c74e16f1eb620f92bbed5c3a87adf2f9e6a5d8f595c0b9ae2b34e`.

O manifesto interno não informa uma licença específica; o binário não é redistribuído por este repositório. Os metadados de origem estão em `docs/origem-do-tutorial.json`. Usar o lançador Python antes de executar tarefas Gradle diretamente em um clone novo.
