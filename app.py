import streamlit as st
import os
import json
import pandas as pd
import firebase_admin
from firebase_admin import credentials, db
import pytz
from datetime import datetime, timedelta

if not firebase_admin._apps:
    # Monta o dicionário de credenciais a partir das variáveis do Render
    cred_dict = {
        "type": "service_account",
        "project_id": os.environ.get("FIREBASE_PROJECT_ID"),
        "private_key_id": os.environ.get("FIREBASE_PRIVATE_KEY_ID"),
        "private_key": os.environ.get("FIREBASE_PRIVATE_KEY").replace('\\n', '\n'),
        "client_email": os.environ.get("FIREBASE_CLIENT_EMAIL"),
        "client_id": os.environ.get("FIREBASE_CLIENT_ID"),
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": os.environ.get("FIREBASE_CLIENT_CERT_URL")
    }
    
    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred, {
        'databaseURL': os.environ.get("FIREBASE_DATABASE_URL")
    })
def registrar_palpite(usuario, grupo, jogo_id, t1, g1, t2, g2):
    ref = db.reference(f'palpites/{grupo}/{usuario}')
    ref.child(jogo_id).set({'time1': t1, 'gols1': g1, 'time2': t2, 'gols2': g2})

def registrar_resultado_oficial(grupo, jogo_id, g1, g2):
    ref = db.reference(f'resultados_oficiais/{grupo}/{jogo_id}')
    ref.set({'g1': g1, 'g2': g2})

def calcular_pontos(gols1_palpite, gols2_palpite, gols1_oficial, gols2_oficial):
    if gols1_palpite == gols1_oficial and gols2_palpite == gols2_oficial:
        return 10  # Pontos por placar exato
    
    vencedor_palpite = (gols1_palpite > gols2_palpite) if gols1_palpite != gols2_palpite else "empate"
    vencedor_oficial = (gols1_oficial > gols2_oficial) if gols1_oficial != gols2_oficial else "empate"
    
    if vencedor_palpite == vencedor_oficial:
        return 5
        
    return 0  
    
def gerar_ranking():
    palpites_db = db.reference('palpites').get()
    resultados_db = db.reference('resultados_oficiais').get()
    
    if not palpites_db: return pd.DataFrame(columns=['Usuário', 'Pontos'])
    
    ranking = {}
    
    # 1. Grupo
    for grupo, jogos_no_grupo in palpites_db.items():
        # 2. jogo_id (ex: A1)
        for jogo_id, usuarios_no_jogo in jogos_no_grupo.items():
            # 3. Usuario (ex: Josue)
            for usuario, palpite in usuarios_no_jogo.items():
                
                # Verifica se existe resultado para este jogo
                if resultados_db and grupo in resultados_db and jogo_id in resultados_db[grupo]:
                    res = resultados_db[grupo][jogo_id]
                    
                    if usuario not in ranking: ranking[usuario] = 0
                    pts = calcular_pontos(palpite['gols1'], palpite['gols2'], res['g1'], res['g2'])
                    ranking[usuario] += pts
                        
    df = pd.DataFrame(list(ranking.items()), columns=['Usuário', 'Pontos'])
    
    if not df.empty:
        return df.groupby('Usuário', as_index=False)['Pontos'].sum().sort_values(by='Pontos', ascending=False)
    return df
# --- 1. CARREGAMENTO DOS DADOS ---
# Certifique-se de que a estrutura 'agenda_oficial' esteja carregada aqui
grupos_oficiais = {
    "Grupo A": ["México 🇲🇽", "África do Sul 🇿🇦", "Coreia do Sul 🇰🇷", "Rep. Tcheca 🇨🇿"],
    "Grupo B": ["Canadá 🇨🇦", "Bósnia e Herz. 🇧🇦", "Catar 🇶🇦", "Suíça 🇨🇭"],
    "Grupo C": ["Brasil 🇧🇷", "Marrocos 🇲🇦", "Haiti 🇭🇹", "Escócia 🏴󠁧󠁢󠁳󠁣󠁴󠁿"],
    "Grupo D": ["Estados Unidos 🇺🇸", "Paraguai 🇵🇾", "Austrália 🇦🇺", "Turquia 🇹🇷"],
    "Grupo E": ["Alemanha 🇩🇪", "Curaçao 🇨🇼", "Costa do Marfim 🇨🇮", "Equador 🇪🇨"],
    "Grupo F": ["Holanda 🇳🇱", "Japão 🇯🇵", "Suécia 🇸🇪", "Tunísia 🇹🇳"],
    "Grupo G": ["Bélgica 🇧🇪", "Egito 🇪🇬", "Irã 🇮🇷", "Nova Zelândia 🇳🇿"],
    "Grupo H": ["Espanha 🇪🇸", "Cabo Verde 🇨🇻", "Arábia Saudita 🇸🇦", "Uruguai 🇺🇾"],
    "Grupo I": ["França 🇫🇷", "Senegal 🇸🇳", "Iraque 🇮🇶", "Noruega 🇳🇴"],
    "Grupo J": ["Argentina 🇦🇷", "Argélia 🇩🇿", "Áustria 🇦🇹", "Jordânia 🇯🇴"],
    "Grupo K": ["Portugal 🇵🇹", "RD Congo 🇨🇩", "Uzbequistão 🇺🇿", "Colômbia 🇨🇴"],
    "Grupo L": ["Inglaterra 🏴󠁧󠁢󠁥󠁮󠁧󠁿", "Croácia 🇭🇷", "Gana 🇬🇭", "Panamá 🇵🇦"]
}
# (Substitua por como você carrega seus dados)
if 'agenda_oficial' not in locals():
    # Exemplo de carregamento, ajuste conforme seu código original
   agenda_oficial = {
    "Grupo A": [
        {"id": "A1", "t1": "México 🇲🇽", "t2": "África do Sul 🇿🇦", "data": "11/06/2026", "hora": "16:00"},
        {"id": "A2", "t1": "Coreia do Sul 🇰🇷", "t2": "Rep. Tcheca 🇨🇿", "data": "11/06/2026", "hora": "23:00"},
        {"id": "A3", "t1": "México 🇲🇽", "t2": "Coreia do Sul 🇰🇷", "data": "18/06/2026", "hora": "22:00"},
        {"id": "A4", "t1": "Rep. Tcheca 🇨🇿", "t2": "África do Sul 🇿🇦", "data": "18/06/2026", "hora": "13:00"},
        {"id": "A5", "t1": "Rep. Tcheca 🇨🇿", "t2": "México 🇲🇽", "data": "24/06/2026", "hora": "22:00"},
        {"id": "A6", "t1": "África do Sul 🇿🇦", "t2": "Coreia do Sul 🇰🇷", "data": "24/06/2026", "hora": "22:00"}
    ],
    "Grupo B": [
        {"id": "B1", "t1": "Canadá 🇨🇦", "t2": "Bósnia e Herz. 🇧🇦", "data": "12/06/2026", "hora": "16:00"},
        {"id": "B2", "t1": "Catar 🇶🇦", "t2": "Suíça 🇨🇭", "data": "13/06/2026", "hora": "16:00"},
        {"id": "B3", "t1": "Canadá 🇨🇦", "t2": "Catar 🇶🇦", "data": "18/06/2026", "hora": "19:00"},
        {"id": "B4", "t1": "Suíça 🇨🇭", "t2": "Bósnia e Herz. 🇧🇦", "data": "18/06/2026", "hora": "18:00"},
        {"id": "B5", "t1": "Suíça 🇨🇭", "t2": "Canadá 🇨🇦", "data": "24/06/2026", "hora": "16:00"},
        {"id": "B6", "t1": "Bósnia e Herz. 🇧🇦", "t2": "Catar 🇶🇦", "data": "24/06/2026", "hora": "16:00"}
    ],
    "Grupo C": [
        {"id": "C1", "t1": "Brasil 🇧🇷", "t2": "Marrocos 🇲🇦", "data": "13/06/2026", "hora": "19:00"},
        {"id": "C2", "t1": "Haiti 🇭🇹", "t2": "Escócia 🏴󠁧󠁢󠁳󠁣󠁴󠁿", "data": "13/06/2026", "hora": "22:00"},
        {"id": "C3", "t1": "Brasil 🇧🇷", "t2": "Escócia 🏴󠁧󠁢󠁳󠁣󠁴󠁿", "data": "24/06/2026", "hora": "19:00"},
        {"id": "C4", "t1": "Marrocos 🇲🇦", "t2": "Haiti 🇭🇹", "data": "24/06/2026", "hora": "19:00"},
        {"id": "C5", "t1": "Haiti 🇭🇹", "t2": "Brasil 🇧🇷", "data": "19/06/2026", "hora": "21:30"},
        {"id": "C6", "t1": "Escócia 🏴󠁧󠁢󠁳󠁣󠁴󠁿", "t2": "Marrocos 🇲🇦", "data": "19/06/2026", "hora": "19:00"}
    ],
    "Grupo D": [
        {"id": "D1", "t1": "Estados Unidos 🇺🇸", "t2": "Paraguai 🇵🇾", "data": "12/06/2026", "hora": "22:00"},
        {"id": "D2", "t1": "Austrália 🇦🇺", "t2": "Turquia 🇹🇷", "data": "14/06/2026", "hora": "01:00"},
        {"id": "D3", "t1": "Estados Unidos 🇺🇸", "t2": "Austrália 🇦🇺", "data": "19/06/2026", "hora": "16:00"},
        {"id": "D4", "t1": "Turquia 🇹🇷", "t2": "Paraguai 🇵🇾", "data": "20/06/2026", "hora": "00:00"},
        {"id": "D5", "t1": "Turquia 🇹🇷", "t2": "Estados Unidos 🇺🇸", "data": "25/06/2026", "hora": "23:00"},
        {"id": "D6", "t1": "Paraguai 🇵🇾", "t2": "Austrália 🇦🇺", "data": "25/06/2026", "hora": "23:00"}
    ],
    "Grupo E": [
        {"id": "E1", "t1": "Alemanha 🇩🇪", "t2": "Curaçao 🇨🇼", "data": "14/06/2026", "hora": "14:00"},
        {"id": "E2", "t1": "Costa do Marfim 🇨🇮", "t2": "Equador 🇪🇨", "data": "14/06/2026", "hora": "20:00"},
        {"id": "E3", "t1": "Alemanha 🇩🇪", "t2": "Costa do Marfim 🇨🇮", "data": "20/06/2026", "hora": "17:00"},
        {"id": "E4", "t1": "Equador 🇪🇨", "t2": "Curaçao 🇨🇼", "data": "20/06/2026", "hora": "21:00"},
        {"id": "E5", "t1": "Equador 🇪🇨", "t2": "Alemanha 🇩🇪", "data": "25/06/2026", "hora": "17:00"},
        {"id": "E6", "t1": "Curaçao 🇨🇼", "t2": "Costa do Marfim 🇨🇮", "data": "25/06/2026", "hora": "17:00"}
    ],
    "Grupo F": [
        {"id": "F1", "t1": "Holanda 🇳🇱", "t2": "Japão 🇯🇵", "data": "14/06/2026", "hora": "17:00"},
        {"id": "F2", "t1": "Suécia 🇸🇪", "t2": "Tunísia 🇹🇳", "data": "14/06/2026", "hora": "23:00"},
        {"id": "F3", "t1": "Holanda 🇳🇱", "t2": "Suécia 🇸🇪", "data": "20/06/2026", "hora": "14:00"},
        {"id": "F4", "t1": "Tunísia 🇹🇳", "t2": "Japão 🇯🇵", "data": "21/06/2026", "hora": "01:00"},
        {"id": "F5", "t1": "Tunísia 🇹🇳", "t2": "Holanda 🇳🇱", "data": "25/06/2026", "hora": "20:00"},
        {"id": "F6", "t1": "Japão 🇯🇵", "t2": "Suécia 🇸🇪", "data": "25/06/2026", "hora": "20:00"}
    ],
    "Grupo G": [
        {"id": "G1", "t1": "Bélgica 🇧🇪", "t2": "Egito 🇪🇬", "data": "15/06/2026", "hora": "16:00"},
        {"id": "G2", "t1": "Irã 🇮🇷", "t2": "Nova Zelândia 🇳🇿", "data": "15/06/2026", "hora": "22:00"},
        {"id": "G3", "t1": "Bélgica 🇧🇪", "t2": "Irã 🇮🇷", "data": "21/06/2026", "hora": "16:00"},
        {"id": "G4", "t1": "Nova Zelândia 🇳🇿", "t2": "Egito 🇪🇬", "data": "21/06/2026", "hora": "22:00"},
        {"id": "G5", "t1": "Nova Zelândia 🇳🇿", "t2": "Bélgica 🇧🇪", "data": "27/06/2026", "hora": "00:00"},
        {"id": "G6", "t1": "Egito 🇪🇬", "t2": "Irã 🇮🇷", "data": "27/06/2026", "hora": "00:00"}
    ],
    "Grupo H": [
        {"id": "H1", "t1": "Espanha 🇪🇸", "t2": "Cabo Verde 🇨🇻", "data": "15/06/2026", "hora": "13:00"},
        {"id": "H2", "t1": "Arábia Saudita 🇸🇦", "t2": "Uruguai 🇺🇾", "data": "15/06/2026", "hora": "19:00"},
        {"id": "H3", "t1": "Espanha 🇪🇸", "t2": "Arábia Saudita 🇸🇦", "data": "21/06/2026", "hora": "13:00"},
        {"id": "H4", "t1": "Uruguai 🇺🇾", "t2": "Cabo Verde 🇨🇻", "data": "21/06/2026", "hora": "19:00"},
        {"id": "H5", "t1": "Uruguai 🇺🇾", "t2": "Espanha 🇪🇸", "data": "26/06/2026", "hora": "21:00"},
        {"id": "H6", "t1": "Cabo Verde 🇨🇻", "t2": "Arábia Saudita 🇸🇦", "data": "26/06/2026", "hora": "21:00"}
    ],
    "Grupo I": [
        {"id": "I1", "t1": "França 🇫🇷", "t2": "Senegal 🇸🇳", "data": "16/06/2026", "hora": "16:00"},
        {"id": "I2", "t1": "Iraque 🇮🇶", "t2": "Noruega 🇳🇴", "data": "16/06/2026", "hora": "19:00"},
        {"id": "I3", "t1": "França 🇫🇷", "t2": "Iraque 🇮🇶", "data": "22/06/2026", "hora": "18:00"},
        {"id": "I4", "t1": "Noruega 🇳🇴", "t2": "Senegal 🇸🇳", "data": "22/06/2026", "hora": "21:00"},
        {"id": "I5", "t1": "Noruega 🇳🇴", "t2": "França 🇫🇷", "data": "26/06/2026", "hora": "16:00"},
        {"id": "I6", "t1": "Senegal 🇸🇳", "t2": "Iraque 🇮🇶", "data": "26/06/2026", "hora": "16:00"}
    ],
    "Grupo J": [
        {"id": "J1", "t1": "Argentina 🇦🇷", "t2": "Argélia 🇩🇿", "data": "16/06/2026", "hora": "22:00"},
        {"id": "J2", "t1": "Áustria 🇦🇹", "t2": "Jordânia 🇯🇴", "data": "17/06/2026", "hora": "01:00"},
        {"id": "J3", "t1": "Argentina 🇦🇷", "t2": "Áustria 🇦🇹", "data": "22/06/2026", "hora": "14:00"},
        {"id": "J4", "t1": "Jordânia 🇯🇴", "t2": "Argélia 🇩🇿", "data": "23/06/2026", "hora": "00:00"},
        {"id": "J5", "t1": "Jordânia 🇯🇴", "t2": "Argentina 🇦🇷", "data": "27/06/2026", "hora": "23:00"},
        {"id": "J6", "t1": "Argélia 🇩🇿", "t2": "Áustria 🇦🇹", "data": "27/06/2026", "hora": "23:00"}
    ],
    "Grupo K": [
        {"id": "K1", "t1": "Portugal 🇵🇹", "t2": "RD Congo 🇨🇩", "data": "17/06/2026", "hora": "14:00"},
        {"id": "K2", "t1": "Uzbequistão 🇺🇿", "t2": "Colômbia 🇨🇴", "data": "17/06/2026", "hora": "23:00"},
        {"id": "K3", "t1": "Portugal 🇵🇹", "t2": "Uzbequistão 🇺🇿", "data": "23/06/2026", "hora": "14:00"},
        {"id": "K4", "t1": "Colômbia 🇨🇴", "t2": "RD Congo 🇨🇩", "data": "23/06/2026", "hora": "23:00"},
        {"id": "K5", "t1": "Colômbia 🇨🇴", "t2": "Portugal 🇵🇹", "data": "27/06/2026", "hora": "20:30"},
        {"id": "K6", "t1": "RD Congo 🇨🇩", "t2": "Uzbequistão 🇺🇿", "data": "27/06/2026", "hora": "20:30"}
    ],
    "Grupo L": [
        {"id": "L1", "t1": "Inglaterra 🏴󠁧󠁢󠁥󠁮󠁧󠁿", "t2": "Croácia 🇭🇷", "data": "17/06/2026", "hora": "17:00"},
        {"id": "L2", "t1": "Gana 🇬🇭", "t2": "Panamá 🇵🇦", "data": "17/06/2026", "hora": "20:00"},
        {"id": "L3", "t1": "Inglaterra 🏴󠁧󠁢󠁥󠁮󠁧󠁿", "t2": "Gana 🇬🇭", "data": "23/06/2026", "hora": "17:00"},
        {"id": "L4", "t1": "Panamá 🇵🇦", "t2": "Croácia 🇭🇷", "data": "23/06/2026", "hora": "20:00"},
        {"id": "L5", "t1": "Panamá 🇵🇦", "t2": "Inglaterra 🏴󠁧󠁢󠁥󠁮󠁧󠁿", "data": "27/06/2026", "hora": "18:00"},
        {"id": "L6", "t1": "Croácia 🇭🇷", "t2": "Gana 🇬🇭", "data": "27/06/2026", "hora": "18:00"}
     ]
   }
st.header("⚽ Fase de Grupos")
grupo_selecionado = st.selectbox("Selecione o Grupo:", list(agenda_oficial.keys()))

# --- 2. ÁREA DO ADMINISTRADOR (FORA DO LOOP) ---
with st.expander("⚙️ Área do Administrador (Registrar Resultado Real)"):
    jogo_id_admin = st.text_input("ID do Jogo (ex: A1)", key="admin_id")
    c_adm1, c_adm2 = st.columns(2)
    g_adm1 = c_adm1.number_input("Gols Time 1", min_value=0, key="admin_g1")
    g_adm2 = c_adm2.number_input("Gols Time 2", min_value=0, key="admin_g2")
    if st.button("Salvar Resultado Oficial", key="btn_admin"):
        registrar_resultado_oficial(grupo_selecionado, jogo_id_admin, g_adm1, g_adm2)
        st.success("Resultado registrado!")
    st.divider()
    st.subheader("⚠️ Zona de Perigo")
if st.text_input("Senha de Adimin", type="password") == "Skcopa26@":
    if st.button("🚨 Resetar Tudo (Palpites e Resultados)"):
        db.reference('palpites').set({})
        db.reference('resultados_oficiais').set({})
        st.warning("Sistema limpo! Todos os dados de palpites e resultados foram removidos.")

# --- 3. LOOP DOS JOGOS ---
jogos_do_grupo = agenda_oficial.get(grupo_selecionado, [])
st.write(f"DEBUG: Jogos carregados para {grupo_selecionado}: {len(jogos_do_grupo)}")

for jogo in jogos_do_grupo:
    try:
        # Lógica de Tempo
        data_hora_str = f"{jogo['data']} {jogo['hora']}:00"
        brasilia_tz = pytz.timezone('America/Sao_Paulo')
        horario_jogo = datetime.strptime(data_hora_str, "%d/%m/%Y %H:%M:%S")
        agora = datetime.now(brasilia_tz).replace(tzinfo=None)
        limite_palpite = horario_jogo - timedelta(minutes=1)

        # O EXPANDE DEVE ESTAR AQUI DENTRO
        with st.expander(f"{jogo['t1']} vs {jogo['t2']} - 🕒 {jogo['data']} {jogo['hora']}"):
            res = db.reference(f'resultados_oficiais/{grupo_selecionado}/{jogo["id"]}').get()
            if res:
                st.info(f"Resultado Real: {res['g1']} x {res['g2']}")
            
            # Bloqueio ou liberação
            if agora < limite_palpite:
                g1_palpite = st.number_input(f"Gols {jogo['t1']}", min_value=0, key=f"g1_{jogo['id']}")
                g2_palpite = st.number_input(f"Gols {jogo['t2']}", min_value=0, key=f"g2_{jogo['id']}")
                nome_usuario = st.text_input(f"Seu Nome/Nick:", key=f"user_{jogo['id']}")
                if st.button("Confirmar Palpite", key=f"btn_{jogo['id']}"):
                    if nome_usuario:
                        registrar_palpite(nome_usuario, grupo_selecionado, jogo['id'], jogo['t1'], g1_palpite, jogo['t2'], g2_palpite)
                        st.success("Palpite salvo!")
                    else:
                        st.warning("Por favor, digite seu nome antes de salvar.")
            else:
                st.error("🔒 Palpites encerrados!")

    except Exception as e:
        st.error(f"Erro no jogo {jogo.get('id')}: {e}")
# --- DEBUG DO RANKING ---
# --- EXIBIÇÃO DO RANKING NO FINAL DA PÁGINA ---
st.divider()
st.header("🏆 Classificação Copástica")

# Chamamos a função diretamente
df_ranking = gerar_ranking()

# Exibição personalizada
if not df_ranking.empty:
    # use_container_width=True faz a tabela ocupar a largura da tela (fica mais bonito)
    st.dataframe(df_ranking, use_container_width=True, hide_index=True)
else:
    st.info("Ainda não há palpites computados.")
