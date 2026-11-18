# Explorer — investigação dinâmica na Fase 1

O Explorer gera hipóteses a partir de *market_tags* observadas e não de uma
lista fixa de setores. O motor usa uma interface `Finder.search()` e
`Sampler.sample()`, exige URL, termos e autorização antes de amostrar e
produz um dossier com fontes, contagens verificáveis e lacunas explícitas.
`platform_client.save_hypothesis` publica novas hipóteses e revisões na Platform.

OpenAlexResearch consulta documentação científica real quando configurado,
mas **não** fornece oportunidades de compra nem comprova rentabilidade.
A efetiva pesquisa automática de fontes comerciais depende de um Finder
licenciado e de acesso a APIs adequadas. Os testes locais usam um Finder
e um Sampler explícitos e não afirmam que houve recolha comercial real.

Sem fornecedor de IA na Fase 1 e sem jobs CircleCI.
