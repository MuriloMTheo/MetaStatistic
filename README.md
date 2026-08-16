## Projeto em andamento. Parte 1 Finalizada:

### Funcionalidade de Tier List:

<img width="1808" height="831" alt="image" src="https://github.com/user-attachments/assets/c0715096-4c24-4c51-8a22-ccd03866abbc" />

### Funcionalidade da inteligência para Seleção de Campeões:

<img width="1802" height="798" alt="image" src="https://github.com/user-attachments/assets/9e95a086-740d-4d5f-ada0-2d07ec37d3ac" />

<img width="1796" height="789" alt="image" src="https://github.com/user-attachments/assets/6b2aff97-1d14-42c5-83ee-a891eb85f1fa" />

## Parte 2:

**FastAPI (Python)** — expor a inteligência como serviço

- Lógica pronta, apenas configurar endpoints
- Permite que qualquer sistema consuma a inteligência (C#, React direto, mobile futuramente)

**ASP.NET (C#)** — back-end robusto

- Responsável por orquestrar chamadas (Python + Data Dragon), cache e histórico
- Escalável — se o projeto crescer, o C# aguenta bem

**React** — interface visual de qualidade

- Componentes reutilizáveis (card de campeão, tierlist, champion select)
- Muito mais controle visual do que o Streamlit permite

---

#### Ordem dos passos

1. **FastAPI** — expor os endpoints Python (`/tierlist`, `/recommend`). Base de tudo.
2. **ASP.NET C#** — criar a API que consome o FastAPI e a Data Dragon.
3. **React** — construir a interface consumindo o C#.
4. **PostgreSQL** — adicionar histórico de recomendações quando quiser evoluir.
