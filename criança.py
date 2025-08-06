import streamlit as st
import collections

# --- Configuração da página ---
st.set_page_config(
    page_title="Analisador de Padrões de Apostas",
    page_icon="🔮",
    layout="wide"
)

# --- Variáveis de Mapeamento ---
mapear_emojis = {'V': '🔴', 'A': '🔵', 'E': '🟡'}

# --- Funções de Análise de Padrões ---
def analisar_padrao(historico):
    """
    Analisa o histórico e retorna o padrão detectado e a sugestão de aposta.
    A lógica agora prioriza a análise de padrões de Empate.
    """
    if len(historico) < 2:
        return "Nenhum Padrão Detectado", "Insira mais resultados para iniciar a análise."

    # Invertemos o histórico para analisar do mais recente para o mais antigo
    hist_recente = list(historico)[::-1]

    # --- ANÁLISE PRIORITÁRIA DE PADRÕES DE EMPATE (🟡) ---
    # Verifica se o resultado mais recente é um empate
    if hist_recente[0] == 'E':
        # 3. Empate Duplo Estratégico (Ex.: 🔴🟡🔵🟡) - Raro, mas crítico
        if len(hist_recente) >= 4 and hist_recente[2] == 'E':
            lado_vencedor = mapear_emojis[hist_recente[1]]
            sugestao = f"Empate Duplo Estratégico ({mapear_emojis['E']}) detectado. A IA pode forçar uma sequência forte agora. Sugestão: Aposte na repetição do último lado a vencer ({lado_vencedor})."
            return "Empate 3. Duplo Estratégico", sugestao

        # 5. Empate no Início do Ciclo (Ex.: 🟡🔴🔵)
        if len(hist_recente) >= 3:
            sugestao = f"Empate ({mapear_emojis['E']}) no início do ciclo. A IA pode usar isto para embaralhar a leitura. Sugestão: Observe as próximas duas jogadas ({mapear_emojis[hist_recente[1]]}{mapear_emojis[hist_recente[0]]}) e, se forem diferentes, aposte na repetição do segundo lado ({mapear_emojis[hist_recente[0]]})."
            return "Empate 5. Início do Ciclo", sugestao

    # Verifica se há empates nos últimos 3 resultados para padrões de reset
    if 'E' in hist_recente[1:3]:
        # 1. Empate como Reset de Padrão (Ex.: 🔵🔵🔵🟡)
        if len(hist_recente) >= 4 and hist_recente[1] == 'E' and hist_recente[2] == hist_recente[3]:
            lado_dominante = mapear_emojis[hist_recente[2]]
            lado_oposto = mapear_emojis['A' if hist_recente[2] == 'V' else 'V']
            sugestao = f"Padrão de Reset de Padrão (🟡) detectado após sequência de {lado_dominante}. A IA tende a inverter a tendência. Sugestão: Aposte no lado oposto ({lado_oposto})."
            return "Empate 1. Reset de Padrão", sugestao

        # 2. Empate como Âncora no Meio (Ex.: 🔵🔴🟡🔴🔵)
        if len(hist_recente) >= 3 and hist_recente[1] == 'E' and hist_recente[0] != hist_recente[2]:
            sugestao = f"Empate ({mapear_emojis['E']}) como âncora no meio de uma alternância. A IA continua a alternância. Sugestão: Siga a alternância, aposte em ({mapear_emojis[hist_recente[2]]})."
            return "Empate 2. Âncora no Meio", sugestao

        # 4. Empate como Isca de Virada (Ex.: 🔵🔵🟡🔴🔴)
        if len(hist_recente) >= 4 and hist_recente[1] == 'E' and hist_recente[0] == hist_recente[1] and hist_recente[0] != hist_recente[2]:
            lado_novo = mapear_emojis[hist_recente[0]]
            sugestao = f"Empate ({mapear_emojis['E']}) como isca de virada. A IA mudou radicalmente o padrão. Sugestão: Acompanhe a nova tendência ({lado_novo})."
            return "Empate 4. Isca de Virada", sugestao

    # --- ANÁLISE DOS PADRÕES SEM EMPATE RECENTE ---
    # Garante que não há empates recentes para evitar conflito com a lógica acima
    if 'E' not in hist_recente[:6]:
        # 7. Padrão Espelho
        if len(hist_recente) >= 6 and hist_recente[0:3] == hist_recente[3:6][::-1]:
            sugestao = "Padrão Espelho detectado. A IA inverte a sequência para confundir sua leitura. Sugestão: Não confie na repetição exata do padrão."
            return "7. Espelho", sugestao

        # 4. Padrão Camuflado de Ciclo 3-1
        if len(hist_recente) >= 4 and hist_recente[0] == hist_recente[1] == hist_recente[2] and hist_recente[3] != hist_recente[0]:
            sugestao = f"Ciclo 3-1 detectado ({mapear_emojis[hist_recente[0]]}x3 -> {mapear_emojis[hist_recente[3]]}). A IA tende a inverter o ciclo quando as apostas aumentam. Sugestão: Esteja preparado para a inversão."
            return "4. Ciclo 3-1", sugestao

        # 6. Armadilha Pós-Ganho
        if len(hist_recente) >= 3 and hist_recente[0] == hist_recente[1] and hist_recente[2] != hist_recente[0]:
            sugestao = f"Armadilha Pós-Ganho detectada. A IA força dois resultados opostos após uma vitória. Sugestão: Não dobre sua aposta após uma vitória neste momento."
            return "6. Armadilha Pós-Ganho", sugestao

        # 1. Padrão de Alternância Simples (Ping-Pong)
        count_ping_pong = 0
        if len(hist_recente) >= 2:
            for i in range(len(hist_recente) - 1):
                if hist_recente[i] != hist_recente[i+1]:
                    count_ping_pong += 1
                else:
                    break
        if count_ping_pong >= 4:
            sugestao = f"Padrão de Ping-Pong detectado com {count_ping_pong + 1} alternâncias. A IA pode quebrar este padrão agora. Sugestão: Aposte contra a alternância (ex: se o último foi {mapear_emojis[hist_recente[0]]}, aposte em {mapear_emojis[hist_recente[0]]} novamente)."
            return "1. Alternância Simples (Ping-Pong)", sugestao
        
        # 2. Padrão de Sequência Estendida
        count_seq = 0
        if len(hist_recente) >= 2:
            for i in range(len(hist_recente)):
                if hist_recente[i] == hist_recente[0]:
                    count_seq += 1
                else:
                    break
        if count_seq >= 3:
            sugestao = f"Sequência estendida de {count_seq} resultados de {mapear_emojis[hist_recente[0]]}. A IA força você a acreditar que 'vai virar'. Sugestão: Mantenha a aposta na continuação até a quebra, ou aguarde a quebra e inverta."
            return "2. Sequência Estendida", sugestao
    
    # --- Padrão de Ruído Controlado / Quântico (Caso nenhum outro se encaixe) ---
    sugestao = "A sequência parece aleatória. Sugestão: Cautela, não há padrão claro. Evite apostas pesadas."
    return "8. Ruído Controlado / Quântico", sugestao

# --- Inicialização do estado da sessão ---
if 'historico' not in st.session_state:
    st.session_state.historico = collections.deque(maxlen=20) # Limita a 20 resultados

# --- Layout do aplicativo ---
st.title("🔮 Analisador de Padrões de Apostas")
st.markdown("---")

st.markdown("### 1. Inserir Resultados")
st.write("Clique nos botões correspondentes ao resultado do jogo.")

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    if st.button("🔴 Vitória da Casa", use_container_width=True):
        st.session_state.historico.append('V')
with col2:
    if st.button("🔵 Vitória do Visitante", use_container_width=True):
        st.session_state.historico.append('A')
with col3:
    if st.button("🟡 Empate", use_container_width=True):
        st.session_state.historico.append('E')
with col4:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Desfazer", help="Remove o último resultado inserido", use_container_width=True):
        if st.session_state.historico:
            st.session_state.historico.pop()
with col5:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Limpar Histórico", help="Apaga todos os resultados", type="primary", use_container_width=True):
        st.session_state.historico.clear()

st.markdown("---")

st.markdown("### 2. Histórico de Resultados")
historico_str = " ".join([mapear_emojis[r] for r in reversed(st.session_state.historico)])
st.markdown(f"**Mais Recente → Mais Antigo:** {historico_str}")

st.markdown("---")

st.markdown("### 3. Análise e Sugestão")
if st.session_state.historico:
    padrao, sugestao = analisar_padrao(list(st.session_state.historico))
    st.markdown(f"**Padrão Detectado:** `{padrao}`")
    st.info(f"**Sugestão:** {sugestao}")
else:
    st.info("O histórico está vazio. Insira resultados para começar a análise.")

# Agradecimento
st.markdown("<br><br><br>", unsafe_allow_html=True)
st.markdown("---")
st.write("Desenvolvido para análise de padrões de cassino com Streamlit. **Lembre-se:** jogue com responsabilidade.")
