👨‍💻 Integrantes


Nome	RM


João Victor Vendrameto  563665

Gabriel Ambrósio Saraiva  566552






🧙 SQLgard – O Despertar do Kernel Ancestral e Os Anéis do Poder
RPG Engine com Python + Oracle PL/SQL



📖 A História

Um antigo servidor de RPG foi encontrado nos escombros de uma universidade esquecida.

No mundo de SQLgard, uma névoa venenosa ancestral começou a se espalhar pelo campo de batalha, drenando lentamente a vida de todos os heróis ativos.

A cada turno, essa névoa consome parte da energia vital dos guerreiros, aproximando-os lentamente da queda.

Mas uma antiga magia ainda resiste.

Inspirado nas lendas de The Lord of the Rings, o sistema inclui uma mecânica especial chamada Bênção de Galadriel.

Quando todos os heróis parecem estar perdidos, essa magia pode restaurar completamente os heróis que foram derrotados, permitindo que a batalha continue e evitando que o jogo termine prematuramente.

Assim, o sistema simula um pequeno motor de RPG, onde a interface visual mostra o estado dos heróis enquanto a lógica do combate é processada diretamente dentro do banco de dados.

🧠 Arquitetura do Projeto

O sistema foi dividido em duas camadas principais.

🎮 Interface (Python)

Responsável por:

Exibir o estado atual dos heróis

Permitir avançar o turno da batalha

Aplicar a Bênção de Galadriel

Exibir mensagens narrativas do combate

A aplicação foi construída com Flask.

⚙️ Motor do Jogo (PL/SQL)

Toda a lógica da batalha ocorre dentro do Oracle Database.

A cada turno:

A Névoa Ancestral causa dano em todos os heróis ativos

O HP é reduzido

Se o HP chegar a 0, o status muda para CAÍDO

A Bênção de Galadriel pode restaurar todos os heróis caídos, devolvendo-os ao combate com HP máximo.

🛠 Tecnologias Utilizadas
Backend

🐍 Python

🌐 Flask

🔌 oracledb



Banco de Dados

🗄 Oracle Database

⚙️ PL/SQL




Hospedagem

☁ Vercel

🧪 SQL de Inicialização



CREATE TABLE TB_HEROIS (
    id_heroi NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome VARCHAR2(50),
    classe VARCHAR2(20),
    hp_atual NUMBER,
    hp_max NUMBER,
    status VARCHAR2(20) DEFAULT 'ATIVO'
);

INSERT INTO TB_HEROIS (nome, classe, hp_atual, hp_max)
VALUES ('Artorias', 'GUERREIRO', 100, 100);

INSERT INTO TB_HEROIS (nome, classe, hp_atual, hp_max)
VALUES ('Sif', 'LADRÃO', 80, 80);

INSERT INTO TB_HEROIS (nome, classe, hp_atual, hp_max)
VALUES ('Gwyn', 'MAGO', 60, 60);

COMMIT;



⚔️ Mecânica da Batalha

A cada turno:

A Névoa Ancestral causa 10 pontos de dano aos heróis ativos

Se o HP chegar a 0, o status muda para CAÍDO

A Bênção de Galadriel pode restaurar os heróis derrotados.




🧩 Bloco PL/SQL do Turno





DECLARE
    v_dano NUMBER := 10;
    v_hp NUMBER;
BEGIN
    FOR r IN (
        SELECT id_heroi, hp_atual
        FROM TB_HEROIS
        WHERE status = 'ATIVO'
    ) LOOP

        v_hp := r.hp_atual - v_dano;

        IF v_hp <= 0 THEN
            UPDATE TB_HEROIS
            SET hp_atual = 0,
                status = 'CAÍDO'
            WHERE id_heroi = r.id_heroi;
        ELSE
            UPDATE TB_HEROIS
            SET hp_atual = v_hp
            WHERE id_heroi = r.id_heroi;
        END IF;

    END LOOP;

    COMMIT;
END;



🌐 Deploy

A aplicação foi hospedada utilizando Vercel.

Variáveis de ambiente
DB_USER
DB_PASSWORD
DB_DSN

Exemplo de DSN:

host:1521/service_name
📦 Estrutura do Projeto
api/
   app.py

requirements.txt
README.md
⚡ Conceitos Demonstrados

Este projeto demonstra:

Integração Python + Oracle

Uso de PL/SQL para lógica de negócio

Processamento transacional dentro do banco

Deploy de aplicações Python serverless

Interface web integrada ao banco de dados

