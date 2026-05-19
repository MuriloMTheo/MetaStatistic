# Análise — Inteligência do Sistema

---

## Requisitos de Uso

- O usuário deve **obrigatoriamente** escolher uma das cinco rotas disponíveis do time **Aliado**.
- O usuário deve **obrigatoriamente** escolher um outro campeão em alguma rota diferente da selecionada por ele. O único requisito é ter apenas um campeão selecionado, seja inimigo ou aliado.

---

## Regras por Campeão

Cada campeão possui três informações:

- **Tipo de dano:** Poder de Habilidade (AP), Dano de Ataque (AD) ou Dano Misto.
- **Alcance de ataque básico:** Ranged (ataque a distância) ou Melee (ataque corporal).
- **Classe:** Lutador, Assassino, Mago, Atirador, Tanque, etc.

---

## Funcionalidade

1. Quando o usuário escolhe e confirma a rota que deseja usar o sistema, uma requisição é enviada ao banco para retornar apenas os campeões daquela rota durante o patch.
   - **Exemplo:** Ao selecionar *Selva*, o sistema recomendará algum dos campeões relacionados àquela rota.

2. Após a seleção da rota do usuário, ele deve preencher qualquer uma das outras nove posições restantes (4 do time aliado e 5 do time inimigo), sem restrições.

3. Após o preenchimento das outras rotas, o usuário deve clicar em um botão de **Confirmar** na interface, e o sistema trará a recomendação de **até 3 campeões** da rota selecionada, especificando o porquê de cada escolha.

---

## Forma de Validação

### Estrutura de Variáveis

Cada posição/rota representa um token/variável. Exemplos: `Top_Ally`, `Top_Enemy`, etc.

Cada uma dessas variáveis armazena o nome do campeão selecionado e, quando confirmado, recebe suas informações determinadas por personagem.

**Exemplo de agrupamento:**
```json
Ally_Team {
  "qntAp": 0,
  "qntAd": 2,
  "classes": ["assassino", "lutador"],
  "RivalRange": "Melee"
}
```

---

### Verificações

**Primeira verificação:** Se existe informação de time aliado, inimigo ou ambos.

- **Ambos:** a comparação é feita a partir da ausência no time aliado e presença no time inimigo.
- **Apenas time aliado:** é definido em razão dos pontos focais ausentes na equipe.
  - *Exemplo: Um time com dois magos fáceis de serem abatidos → recomendação de um lutador/tanque.*
- **Apenas time inimigo:** é definido a partir de relações de mais forte/mais fraco.
  - *Exemplo: Um time adversário com um assassino AD e um tanque → recomendação de um lutador/tanque.*

**Segunda verificação:** Tipo de dano — recomendação para suprir o que falta. Em caso de equilíbrio, avança para a próxima etapa.

**Terceira verificação:** Classe — recomendação feita com base em regras estabelecidas.
- *Exemplo: Time inimigo possui lutador e assassino, enquanto o time aliado possui somente mago → recomendação com base em uma ordem de prioridades para esse caso.*
- Em caso de equilíbrio, avança para a próxima etapa.

**Quarta verificação:** Range de ataque.

---

### Seleção Final

Os três campeões recomendados são escolhidos de acordo com a **estatística de maior WinRate do meta**, de acordo com o resultado obtido a partir da seleção.

**Exemplo de retorno:**
```
Return_Champ_As { "AD", "Lutador", "Tanque", "Melee" }
```

**Exemplo de descrição justificando a escolha:**
> **Urgot:** Time aliado sem front-line de lutador/tanque e ausência de dano AD. Time inimigo com dano AD e front-line tanque.

---

## Resumo do Fluxo de Recomendação

1. Pega os campeões da rota escolhida.
2. Filtra por tipo de dano (AD / AP / Misto).
3. Filtra por classe (em cima do resultado anterior).
4. Filtra por range (em cima do resultado anterior).
5. Se em algum passo o resultado ficar vazio, volta ao passo anterior e prossegue para a próxima iteração.
6. Ordena pelo WinRate e retorna os **top 3**.
7. **Default:** Caso nenhuma condição seja atendida, retorna o **top 3 mais forte do patch** para aquela rota.