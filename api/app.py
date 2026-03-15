from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import oracledb, os

app = FastAPI()

DB_USER = os.environ["DB_USER"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_DSN = os.environ["DB_DSN"]

pool = oracledb.create_pool(
    user=DB_USER,
    password=DB_PASSWORD,
    dsn=DB_DSN,
    min=1,
    max=5,
    increment=1
)

def get_connection():
    return pool.acquire()


@app.get("/listar-herois", response_class=HTMLResponse)
def listar_herois():
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT nome, classe, hp_atual, hp_max, status FROM TB_HEROIS")
        dados = cur.fetchall()

        cur.close()
        conn.close()

        html = """
        <html>
        <head>
            <style>
                table {border-collapse: collapse; width: 80%; margin: 20px auto;}
                th, td {border: 1px solid #ccc; padding: 8px; text-align: center;}
                th {background-color: #f2f2f2;}
            </style>
        </head>
        <body>
            <h2 style="text-align:center;">Tabela de Heróis</h2>
            <table>
                <tr>
                    <th>Nome</th>
                    <th>Classe</th>
                    <th>HP Atual</th>
                    <th>HP Máx</th>
                    <th>Status</th>
                </tr>
        """

        for nome, classe, hp_atual, hp_max, status in dados:
            html += f"""
                <tr>
                    <td>{nome}</td>
                    <td>{classe}</td>
                    <td>{hp_atual}</td>
                    <td>{hp_max}</td>
                    <td>{status}</td>
                </tr>
            """

        html += """
            </table>
        </body>
        </html>
        """

        return html

    except Exception as e:
        return f"<p>Erro: {str(e)}</p>"


@app.post("/processar-turno")
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

    return {"msg": "Turno processado!"}


@app.post("/restaurar-herois")
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

    return {"msg": msg}
