from fastapi import FastAPI
import oracledb, os

app = FastAPI()

# Variáveis de ambiente (usando get para não quebrar se estiverem faltando)
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_DSN = os.environ.get("DB_DSN")

def get_connection():
    # Conexão em modo thin (sem Instant Client)
    return oracledb.connect(user=DB_USER, password=DB_PASSWORD, dsn=DB_DSN)

@app.get("/")
def home():
    return {"msg": "Deploy funcionando em modo thin!"}

@app.get("/listar-herois")
def listar_herois():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT nome, classe, hp_atual, hp_max, status FROM TB_HEROIS")
        dados = cur.fetchall()
        cur.close()
        conn.close()
        return {"herois": dados}
    except Exception as e:
        return {"erro": str(e)}

@app.post("/processar-turno")
def processar_turno():
    try:
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
    except Exception as e:
        return {"erro": str(e)}

@app.post("/restaurar-herois")
def restaurar_herois():
    try:
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
    except Exception as e:
        return {"erro": str(e)}
