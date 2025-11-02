# 🔗 **Relacionamentos entre Entidades -- MIDDLEWARE_OAB**

### 🧾 **Cadastro**

-   **0 : N** → `Usuario_advogado`\
-   **0 : N** → `Analista_de_ti`\
-   **0 : N** → `Administrador_sala_coworking`

Cada cadastro pode estar associado a um único tipo de usuário (advogado, analista ou administrador).

------------------------------------------------------------------------

### ⚖️ **Usuario_advogado**

-   **1 : 1** → `Cadastro`\
-   **1 : 1** → `Sessao`

Um usuário advogado possui um cadastro único e pode ter uma sessão ativa em um computador de sala de coworking.

------------------------------------------------------------------------

### 🧑‍💻 **Analista_de_ti**

-   **1 : 1** → `Cadastro`\
-   **N : N** → `Sessao` *(via tabela associativa `Sessoes_analistas`)*

Um analista de TI possui um cadastro único e pode estar associado a múltiplas sessões para suporte técnico.

------------------------------------------------------------------------

### 🧑‍🏫 **Administrador_sala_coworking**

-   **1 : 1** → `Cadastro`\
-   **1 : 1** → `Sala_coworking`\
-   **1 : N** → `Sessao`

Um administrador de sala de coworking possui um cadastro único, gerencia uma sala específica e pode supervisionar várias sessões.

------------------------------------------------------------------------

### 🏢 **Subsecional**

-   **1 : N** → `Unidade`\
-   **1 : N** → `Sala_coworking`

Cada subsecional pode conter várias unidades e salas de coworking.

------------------------------------------------------------------------

### 🏬 **Unidade**

-   **1 : 1** → `Subsecional`\
-   **1 : N** → `Sala_coworking`

Cada unidade pertence a uma subsecional e pode abrigar várias salas de coworking.

------------------------------------------------------------------------

### 💼 **Sala_coworking**

-   **1 : 1** → `Subsecional`\
-   **1 : 1** → `Unidade`\
-   **0 : 1** → `Administrador_sala_coworking`\
-   **1 : N** → `Computador`\

Cada sala de coworking está vinculada a uma subsecional e unidade específicas, pode ter um administrador e contém múltiplos computadores.

------------------------------------------------------------------------

### 💻 **Computador**

-   **1 : 1** → `Sala_coworking`\
-   **0 : 1** → `Sessao`

Cada computador está localizado em uma sala de coworking e pode estar associado a uma sessão ativa.

------------------------------------------------------------------------

### ⏱️ **Sessao**

-   **1 : 1** → `Computador`\
-   **1 : 1** → `Usuario_advogado`\
-   **1 : 1** → `Administrador_sala_coworking`\
-   **N : N** → `Analista_de_ti` *(via `Sessoes_analistas`)*

Cada sessão está vinculada a um computador, um usuário advogado, um administrador de sala de coworking e pode envolver múltiplos analistas de TI para suporte.

------------------------------------------------------------------------

### 🔄 **Sessoes_analistas**

-   **N : N** entre `Sessao` e `Analista_de_ti`\

Tabela associativa para gerenciar a relação muitos-para-muitos entre sessões e analistas de TI.
