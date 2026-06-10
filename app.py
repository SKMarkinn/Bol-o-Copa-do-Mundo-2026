if not firebase_admin._apps:
    # Obtém o dicionário dos secrets
    config = dict(st.secrets["FIREBASE_CREDS"])
    
    # IMPORTANTE: Corrige manualmente a quebra de linha na chave privada
    # Se o TOML removeu os \n, nós reinserimos aqui para garantir o formato correto
    config["private_key"] = config["private_key"].replace("\\n", "\n")
    
    cred = credentials.Certificate(config)
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://bolao-copa-do-mundo-2026-c4d2c-default-rtdb.firebaseio.com/'
    })
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

# ==========================================
# 2. AGENDA DE JOGOS (APENAS DATA E HORA)
# ==========================================
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

# ==========================================
# 3. LÓGICA E INICIALIZAÇÃO DA MEMÓRIA
# ==========================================
if 'tabelas_copa' not in st.session_state:
    st.session_state.tabelas_copa = {}
    for nome_grupo, times in grupos_oficiais.items():
        st.session_state.tabelas_copa[nome_grupo] = {
            time: {"pontos": 0, "vitorias": 0, "empates": 0, "derrotas": 0, "gols_pro": 0, "gols_sofridos": 0, "saldo": 0}
            for time in times
        }

if 'jogos_registrados' not in st.session_state:
    st.session_state.jogos_registrados = set()
    
if 'mata_mata_32' not in st.session_state:
    st.session_state.mata_mata_32 = []

def registrar_jogo(grupo, time1, gols1, time2, gols2):
    ref = db.reference(f'palpites/{grupo}')
    ref.push({
        'time1': time1,
        'gols1': gols1,
        'time2': time2,
        'gols2': gols2,
        'data': datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    })
    # Opcional: manter a lógica local também para a tabela atualizar na tela
    # ... (seu código atual de atualizar tabela)

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

# ==========================================
# 4. INTERFACE: FASE DE GRUPOS E PALPITES
# ==========================================
st.header("⚽ Fase de Grupos")
grupo_selecionado = st.selectbox("Selecione o Grupo para palpitar e ver a tabela:", list(grupos_oficiais.keys()))

col_tabela, col_placar = st.columns([1.5, 1])

with col_tabela:
    st.subheader(f"Tabela - {grupo_selecionado}")
    df = pd.DataFrame.from_dict(st.session_state.tabelas_copa[grupo_selecionado], orient='index')
    df = df.sort_values(by=['pontos', 'vitorias', 'saldo', 'gols_pro'], ascending=[False, False, False, False])
    df = df.rename(columns={"pontos": "Pontos", "vitorias": "Vitórias", "empates": "Empates", "derrotas": "Derrotas", "gols_pro": "GP", "gols_sofridos": "GS", "saldo": "SG"})
    st.dataframe(df, use_container_width=True)

with col_placar:
    st.subheader("Registrar Palpite")
    jogos_do_grupo = agenda_oficial.get(grupo_selecionado, [])
    
    if not jogos_do_grupo:
        st.warning("⚠️ Agenda oficial não cadastrada.")
    else:
        opcoes = [f"{j['t1']} x {j['t2']}" for j in jogos_do_grupo]
        escolha = st.selectbox("Selecione a Partida", opcoes)
        idx = opcoes.index(escolha)
        jogo_atual = jogos_do_grupo[idx]
        
        with st.container(border=True):
            st.markdown(f"<h4 style='text-align: center;'>{jogo_atual['t1']} vs {jogo_atual['t2']}</h4>", unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            c1.caption(f"📅 **Data:** {jogo_atual['data']}")
            c2.caption(f"⏰ **Hora:** {jogo_atual['hora']}")
            
        formato = "%d/%m/%Y %H:%M"
        hora_do_jogo = datetime.strptime(f"{jogo_atual['data']} {jogo_atual['hora']}", formato)
        
        # Sincronização automática com o fuso de Brasília
        agora_brasil = datetime.utcnow() - timedelta(hours=3)
        prazo_limite = hora_do_jogo - timedelta(minutes=1)
        
        if agora_brasil > prazo_limite:
            st.error(f"🚨 Tempo esgotado! Prazo encerrou às {prazo_limite.strftime('%H:%M')}.")
        else:
            st.success(f"✅ Palpite liberado até as {prazo_limite.strftime('%H:%M')}.")
            col_g1, col_x, col_g2 = st.columns([2,1,2])
            with col_g1:
                gols_t1 = st.number_input(f"{jogo_atual['t1']}", min_value=0, step=1, key="g1")
            with col_x:
                st.markdown("<h4 style='text-align: center; margin-top: 30px;'>X</h4>", unsafe_allow_html=True)
            with col_g2:
                gols_t2 = st.number_input(f"{jogo_atual['t2']}", min_value=0, step=1, key="g2")

                if st.button("Salvar Resultado"):
                   registrar_palpite_firebase(grupo_selecionado, jogo_atual['id'], jogo_atual['t1'], gols_t1, jogo_atual['t2'], gols_t2)
                   st.success("Palpite enviado para o Banco de Dados!")
                else:
                   registrar_jogo(grupo_selecionado, jogo_atual['t1'], gols_t1, jogo_atual['t2'], gols_t2)
                   st.session_state.jogos_registrados.add(jogo_atual['id'])
                   st.rerun()

st.divider()

# ==========================================
# 5. APURAÇÃO E CHAVEAMENTO AUTOMÁTICO
# ==========================================
st.header("🏆 Chaveamento Oficial (Mata-Mata)")

if st.button("🔐 Encerrar Fase de Grupos e Gerar Chaveamento", type="primary", use_container_width=True):
    primeiros = {}
    segundos = {}
    terceiros = []

    for grupo in grupos_oficiais.keys():
        df_grupo = pd.DataFrame.from_dict(st.session_state.tabelas_copa[grupo], orient='index')
        df_grupo = df_grupo.sort_values(by=['pontos', 'vitorias', 'saldo', 'gols_pro'], ascending=[False, False, False, False])
        times_ordenados = df_grupo.index.tolist()
        
        primeiros[grupo] = times_ordenados[0]
        segundos[grupo] = times_ordenados[1]
        
        status_terceiro = df_grupo.iloc[2].to_dict()
        status_terceiro["time"] = times_ordenados[2]
        terceiros.append(status_terceiro)
    
    df_terceiros = pd.DataFrame(terceiros)
    df_terceiros['gols_sofridos_neg'] = -df_terceiros['gols_sofridos'] 
    df_terceiros = df_terceiros.sort_values(by=['pontos', 'vitorias', 'saldo', 'gols_pro', 'gols_sofridos_neg'], ascending=[False, False, False, False, False])
    melhores_terceiros = df_terceiros.head(8)['time'].tolist()

    st.session_state.mata_mata_32 = [
        {"id": "M1", "t1": primeiros["Grupo A"], "t2": melhores_terceiros[0]},
        {"id": "M2", "t1": segundos["Grupo B"], "t2": segundos["Grupo F"]},
        {"id": "M3", "t1": primeiros["Grupo C"], "t2": melhores_terceiros[1]},
        {"id": "M4", "t1": segundos["Grupo D"], "t2": segundos["Grupo H"]},
        {"id": "M5", "t1": primeiros["Grupo E"], "t2": melhores_terceiros[2]},
        {"id": "M6", "t1": segundos["Grupo A"], "t2": segundos["Grupo E"]},
        {"id": "M7", "t1": primeiros["Grupo G"], "t2": melhores_terceiros[3]},
        {"id": "M8", "t1": segundos["Grupo C"], "t2": segundos["Grupo G"]},
        {"id": "M9", "t1": primeiros["Grupo I"], "t2": melhores_terceiros[4]},
        {"id": "M10", "t1": primeiros["Grupo B"], "t2": segundos["Grupo I"]},
        {"id": "M11", "t1": primeiros["Grupo K"], "t2": melhores_terceiros[5]},
        {"id": "M12", "t1": primeiros["Grupo D"], "t2": segundos["Grupo J"]},
        {"id": "M13", "t1": primeiros["Grupo L"], "t2": melhores_terceiros[6]},
        {"id": "M14", "t1": primeiros["Grupo F"], "t2": segundos["Grupo K"]},
        {"id": "M15", "t1": primeiros["Grupo J"], "t2": melhores_terceiros[7]},
        {"id": "M16", "t1": primeiros["Grupo H"], "t2": segundos["Grupo L"]},
    ]
    st.rerun()

if len(st.session_state.mata_mata_32) > 0:
    st.success("✅ Chaveamento gerado com sucesso!")
    st.info("⚠️ Em caso de empate no mata-mata, registre o placar somando os pênaltis.")
    
    for i in range(0, 16, 2):
        col1, col2 = st.columns(2)
        m1 = st.session_state.mata_mata_32[i]
        with col1:
            with st.container(border=True):
                st.markdown(f"<p style='text-align:center;'><b>Jogo {i+1}</b></p>", unsafe_allow_html=True)
                ca, cb, cc = st.columns([2,1,2])
                ca.number_input(m1['t1'], min_value=0, step=1, key=f"g1_{m1['id']}")
                cb.markdown("<h4 style='text-align: center; margin-top: 30px;'>X</h4>", unsafe_allow_html=True)
                cc.number_input(m1['t2'], min_value=0, step=1, key=f"g2_{m1['id']}")
                
        m2 = st.session_state.mata_mata_32[i+1]
        with col2:
            with st.container(border=True):
                st.markdown(f"<p style='text-align:center;'><b>Jogo {i+2}</b></p>", unsafe_allow_html=True)
                ca, cb, cc = st.columns([2,1,2])
                ca.number_input(m2['t1'], min_value=0, step=1, key=f"g1_{m2['id']}")
                cb.markdown("<h4 style='text-align: center; margin-top: 30px;'>X</h4>", unsafe_allow_html=True)
                cc.number_input(m2['t2'], min_value=0, step=1, key=f"g2_{m2['id']}")
