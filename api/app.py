from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse
import oracledb, os

app = FastAPI()

DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_DSN = os.environ.get("DB_DSN")


def get_connection():
    return oracledb.connect(user=DB_USER, password=DB_PASSWORD, dsn=DB_DSN)


def listar_herois():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT nome, classe, hp_atual, hp_max, status FROM TB_HEROIS")
    dados = cur.fetchall()

    cur.close()
    conn.close()

    return dados


def processar_turno():
    conn = get_connection()
    cur = conn.cursor()

    plsql = """
    DECLARE
        v_dano NUMBER := 10;
        v_hp NUMBER;
    BEGIN
        FOR r IN (SELECT id_heroi, hp_atual FROM TB_HEROIS WHERE status = 'ATIVO') LOOP
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
    """

    cur.execute(plsql)
    cur.close()
    conn.close()


def restaurar_herois():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM TB_HEROIS WHERE status = 'CAÍDO'")
    qtd = cur.fetchone()[0]

    if qtd == 0:
        msg = "Somente heróis caídos podem receber a Bênção de Galadriel."
    else:

        plsql = """
        BEGIN
            UPDATE TB_HEROIS
            SET hp_atual = hp_max,
                status = 'ATIVO'
            WHERE status = 'CAÍDO';
            COMMIT;
        END;
        """

        cur.execute(plsql)
        msg = "Vida dos heróis caídos restaurada ao máximo!"

    cur.close()
    conn.close()

    return msg


@app.get("/", response_class=HTMLResponse)
def dashboard():

    dados = listar_herois()

    rows = ""

    for nome, classe, hp_atual, hp_max, status in dados:

        cor = "#33cc33" if status == "ATIVO" else "#ff4d4d"

        rows += f"""
        <tr>
            <td>{nome}</td>
            <td>{classe}</td>
            <td>{hp_atual}</td>
            <td>{hp_max}</td>
            <td style="background:{cor}; font-weight:bold;">{status}</td>
        </tr>
        """

    return f"""
    <html>
    <head>

    <title>SQLgard</title>

    <style>

    body {{
        background:#0b1220;
        font-family:Arial;
        color:white;
        margin:40px;
    }}

    h1 {{
        color:#60a5fa;
    }}

    button {{
        padding:12px 20px;
        margin:10px;
        border:none;
        border-radius:6px;
        font-weight:bold;
        cursor:pointer;
    }}

    .turno {{
        background:#2563eb;
        color:white;
    }}

    .bencao {{
        background:#16a34a;
        color:white;
    }}

    table {{
        width:100%;
        border-collapse:collapse;
        margin-top:20px;
    }}

    th {{
        background:#1f2937;
        padding:10px;
    }}

    td {{
        padding:10px;
        text-align:center;
        border-bottom:1px solid #374151;
    }}

    .alert {{
        background:#222;
        padding:15px;
        border-radius:10px;
        margin-top:20px;
        text-align:center;
    }}

    </style>

    </head>

    <body>

    <h1>SQLgard — O Despertar do Kernel Ancestral</h1>

    <form action="/turno" method="post">
        <button class="turno">Próximo Turno</button>
    </form>

    <form action="/bencao" method="post">
        <button class="bencao">Aplicar Bênção de Galadriel</button>
    </form>

    <h2>Estado dos Heróis</h2>

    <table>

    <tr>
    <th>Nome</th>
    <th>Classe</th>
    <th>HP Atual</th>
    <th>HP Máx</th>
    <th>Status</th>
    </tr>

    {rows}

    </table>

    <div class="alert">
        <b>A Névoa Ancestral</b> envolve o campo de batalha.<br>
        Cada turno ela drena <span style="color:red;font-weight:bold;">10 HP</span> dos heróis ativos.
    </div>

    </body>
    </html>
    """


@app.post("/turno")
def turno():
    processar_turno()
    return RedirectResponse("/", status_code=303)


@app.post("/bencao")
def bencao():
    restaurar_herois()
    return RedirectResponse("/", status_code=303)
