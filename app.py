import streamlit as st
import pandas as pd
import os
import json
import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime, timedelta 
import pytz                             

# Inicialização do Firebase via Variável de Ambiente (Render)
if not firebase_admin._apps:
    try:
        # Carrega a string JSON da variável de ambiente e converte para dicionário Python
        config_string = os.environ.get('FIREBASE_CONFIG_JSON')
        firebase_config = json.loads(config_string)
        
        cred = credentials.Certificate(firebase_config)
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://bolao-copa-do-mundo-2026-c4d2c-default-rtdb.firebaseio.com/'
        })
    except Exception as e:
        st.error(f"Erro ao inicializar Firebase: {e}")
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
if 'tabelas_copa' not in st.session_state:
    st.session_state.tabelas_copa = {
        g: {t: {"pontos": 0, "vitorias": 0, "empates": 0, "derrotas": 0, "gols_pro": 0, "gols_sofridos": 0, "saldo": 0} 
        for t in times} for g, times in grupos_oficiais.items()
    }
if 'jogos_registrados' not in st.session_state:
    st.session_state.jogos_registrados = set()
if 'mata_mata_32' not in st.session_state:
    st.session_state.mata_mata_32 = []

# 4. Funções de Lógica
def registrar_palpite(grupo, jogo_id, time1, gols1, time2, gols2):
    ref = db.reference(f'palpites/{grupo}/{jogo_id}')
    ref.set({'t1': time1, 'g1': gols1, 't2': time2, 'g2': gols2, 'data': datetime.now().strftime("%d/%m/%Y %H:%M")})

def registrar_jogo(grupo, time1, gols1, time2, gols2):
    tabela = st.session_state.tabelas_copa[grupo]
    # Lógica de pontos (se gols1 > gols2, etc...)
    if gols1 > gols2:
        tabela[time1]["pontos"] += 3
        tabela[time1]["vitorias"] += 1
        tabela[time2]["derrotas"] += 1
    elif gols2 > gols1:
        tabela[time2]["pontos"] += 3
        tabela[time2]["vitorias"] += 1
        tabela[time1]["derrotas"] += 1
    else:
        tabela[time1]["pontos"] += 1
        tabela[time2]["pontos"] += 1
        tabela[time1]["empates"] += 1
        tabela[time2]["empates"] += 1
    
    tabela[time1]["gols_pro"] += gols1
    tabela[time1]["gols_sofridos"] += gols2
    tabela[time1]["saldo"] = tabela[time1]["gols_pro"] - tabela[time1]["gols_sofridos"]
    tabela[time2]["gols_pro"] += gols2
    tabela[time2]["gols_sofridos"] += gols1
    tabela[time2]["saldo"] = tabela[time2]["gols_pro"] - tabela[time2]["gols_sofridos"]
def registrar_resultado_oficial(grupo, jogo_id, gols1, gols2):
    # Admin: insere resultado real
    db.reference(f'resultados_oficiais/{grupo}/{jogo_id}').set({'g1': gols1, 'g2': gols2})
    st.success("Resultado oficial registrado!")

# 5. Interface
st.header("⚽ Fase de Grupos")
grupo_selecionado = st.selectbox("Selecione o Grupo:", list(grupos_oficiais.keys()))

with st.expander("⚙️ Área do Administrador (Registrar Resultado Real)"):
    # A área administrativa fica SOLTA, fora do if/else de trava
    jogo_id_admin = st.text_input("ID do Jogo (ex: A1)")
    c_adm1, c_adm2 = st.columns(2)
    g_adm1 = c_adm1.number_input("Gols Time 1", min_value=0)
    g_adm2 = c_adm2.number_input("Gols Time 2", min_value=0)
    if st.button("Salvar Placar Oficial"):
        registrar_resultado_oficial(grupo_selecionado, jogo_id_admin, g_adm1, g_adm2)
        st.success("Resultado oficial registrado!")
    jogo_id_admin = st.text_input("ID do Jogo (ex: A1)", key="admin_jogo_id")
    c_adm1, c_adm2 = st.columns(2)
    g_adm1 = c_adm1.number_input("Gols Time 1", min_value=0)
    g_adm2 = c_adm2.number_input("Gols Time 2", min_value=0)
    if st.button("Salvar Placar Oficial"):
        registrar_resultado_oficial(grupo_selecionado, jogo_id_admin, g_adm1, g_adm2)
jogos_do_grupo = agenda_oficial.get(grupo_selecionado, [])
for jogo in jogos_do_grupo:
    # 1. Montar a string de data/hora no formato que o código espera
    data_hora_str = f"{jogo['data']} {jogo['hora']}:00" # Ex: "11/06/2026 16:00:00"
    
    # 2. Configurar o fuso e calcular a trava
    brasilia_tz = pytz.timezone('America/Sao_Paulo')
    horario_jogo = datetime.strptime(data_hora_str, "%d/%m/%Y %H:%M:%S")
    agora = datetime.now(brasilia_tz).replace(tzinfo=None)
    limite_palpite = horario_jogo - timedelta(minutes=1)

    with st.expander(f"{jogo['t1']} vs {jogo['t2']} - 🕒 {jogo['data']} {jogo['hora']}"):
        if agora < limite_palpite:
            # Formulário de Palpite
            g1_palpite = st.number_input(f"Gols {jogo['t1']}", min_value=0, key=f"g1_{jogo['id']}")
            g2_palpite = st.number_input(f"Gols {jogo['t2']}", min_value=0, key=f"g2_{jogo['id']}")
            
            if st.button("Confirmar Palpite", key=f"btn_{jogo['id']}"):
                registrar_palpite(grupo_selecionado, jogo['id'], jogo['t1'], g1_palpite, jogo['t2'], g2_palpite)
                st.success("Palpite salvo!")
        else:
            st.error("🔒 Palpites encerrados!")

        # Exibir resultado real (se existir)
        res = db.reference(f'resultados_oficiais/{grupo_selecionado}/{jogo["id"]}').get()
        if res:
            st.info(f"Resultado Real: {res['g1']} x {res['g2']}")
