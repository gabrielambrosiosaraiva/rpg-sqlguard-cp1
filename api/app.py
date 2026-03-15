from fastapi import FastAPI
import oracledb, os
oracledb.init_oracle_client(lib_dir=os.path.join(os.getcwd(), "instantclient", "instantclient_19_22"))


app = FastAPI()

DB_USER = os.environ["DB_USER"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_DSN = os.environ["DB_DSN"]

def get_connection():
    return oracledb.connect(user=DB_USER, password=DB_PASSWORD, dsn=DB_DSN)

@app.get("/listar-herois")
def listar_herois():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT nome, classe, hp_atual, hp_max, status FROM TB_HEROIS")
    dados = cur.fetchall()
    cur.close()
    conn.close()
    return {"herois": dados}

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
