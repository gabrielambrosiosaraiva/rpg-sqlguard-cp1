#SQLgard – O Despertar do Kernel Ancestral E Os Anéis do Poder

##👥 Integrantes
- João Victor Vendrameto – RM 563665
- Gabriel Ambrósio Saraiva – RM 566552

##📌 Descrição
Mini-RPG acadêmico feito em **Python + Streamlit**, conectado a um banco de dados **Oracle**.  
A cada turno, os heróis sofrem dano da névoa ancestral. O jogador pode restaurar os heróis caídos, trazendo-os de volta ao estado ativo com vida máxima.

##📌 Diagrama de Fluxo
o

 Usuário
   │
   ▼
 Interface Streamlit
   │   ├── Botão "Próximo Turno" → chama função processar_turno()
   │   └── Botão "Bênção de Galadriel" → chama função restaurar_herois()
   │
   ▼
 Banco Oracle (TB_HEROIS)
   │   ├── SELECT → listar_herois()
   │   ├── UPDATE → aplicar dano da névoa
   │   └── UPDATE → restaurar heróis caídos
   │
   ▼
 Streamlit exibe tabela atualizada dos heróis

##📌 Fluxo de Funcionamento
- Usuário interage com a interface web (Streamlit).
- Cada ação dispara funções Python que executam blocos PL/SQL no Oracle.
- O banco atualiza os dados dos heróis (HP, status).
- O Streamlit renderiza novamente a tabela com os estados atualizados.

##📌 Tecnologias Usadas
- Python 3.12+ (compatível com `python-oracledb`)
- Streamlit → interface web interativa
- Oracle Database → armazenamento dos heróis
- python-oracledb ou cx_Oracle → driver de conexão
- pandas → manipulação e estilização da tabela

##📌 Estrutura do Projeto
- `app.py` → código principal
- `requirements.txt` → dependências
- `README.md` → documentação

##📌 Banco de Dados
Tabela usada: **TB_HEROIS**

```sql
CREATE TABLE TB_HEROIS (
    id_heroi NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome VARCHAR2(50),
    classe VARCHAR2(20),
    hp_atual NUMBER,
    hp_max NUMBER,
    status VARCHAR2(20) DEFAULT 'ATIVO'
);

-- Inserções iniciais
INSERT INTO TB_HEROIS (nome, classe, hp_atual, hp_max) VALUES ('Artorias', 'GUERREIRO', 100, 100);
INSERT INTO TB_HEROIS (nome, classe, hp_atual, hp_max) VALUES ('Sif', 'LADRÃO', 80, 80);
INSERT INTO TB_HEROIS (nome, classe, hp_atual, hp_max) VALUES ('Gwyn', 'MAGO', 60, 60);

COMMIT;



##📌 Funcionalidades
- Listar Heróis → mostra nome, classe, HP e status.
- Próximo Turno → aplica dano da névoa (10 pontos por turno).
- Restaurar Heróis → revive todos os heróis caídos e restaura HP ao máximo.

##📌 requirements.txt

##📌Para Python 3.12

streamlit
python-oracledb
pandas


##📌Para Python 3.13
streamlit
cx_Oracle
pandas

##📌 Como Rodar Localmente

pip install -r requirements.txt
setx DB_USER meu_usuario
setx DB_PASSWORD minha_senha
setx DB_DSN "host:porta/servico"
streamlit run app.py


##📌 Deploy no Vercel
- Adicione requirements.txt ao projeto.
- Configure variáveis de ambiente (DB_USER, DB_PASSWORD, DB_DSN) no painel do Vercel.
- Comando de inicialização:

streamlit run app.py --server.port=$PORT --server.headless=true

##📌 Observações
- Cada clique em Próximo Turno aplica um turno de dano.
- O botão Restaurar Heróis revive todos os heróis caídos de uma vez.
