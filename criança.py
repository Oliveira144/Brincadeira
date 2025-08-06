import streamlit as st
import collections

# --- Configuração da página ---
st.set_page_config(
    page_title="Analisador de Padrões de Apostas",
    page_icon="🔮",
    layout="wide"
)

# --- Funções de Análise de Padrões ---
def analisar_padrao(historico):
    """
    Analisa o histórico e retorna o padrão detectado e a sugestão de aposta.
    """
    if len(historico) < 2:
        return "Nenhum Padrão Detectado", "Insira mais resultados para iniciar a análise."

    # Invertemos o histórico para analisar do mais recente para o mais antigo
    hist_recente = historico[::-1]

    # --- Padrão de Alternância Simples (Ping-Pong) ---
    if len(hist_recente) >= 4 and hist_recente[0] != hist_recente[1] and hist_recente[1] != hist_recente[2] and hist_recente[2] != hist_recente[3]:
        count_ping_pong = 0
        for i in range(len(hist_recente) - 1):
            if hist_recente[i] != hist_recente[i+1]:
                count_ping_pong += 1
            else:
                break
        if count_ping_pong >= 4:
            sugestao = f"Padrão de Ping-Pong detectado com {count_ping_pong+1} alternâncias. A IA pode quebrar este padrão agora. Sugestão: Aposte contra a alternância (ex: se o último foi {hist_recente[0]}, aposte em {hist_recente[0]} novamente)."
            return "Padrão 1. Alternância Simples (Ping-Pong)", sugestao
    
    # --- Padrão de Sequência Estendida ---
    if len(hist_recente) >= 3 and hist_recente[0] == hist_recente[1] == hist_recente[2]:
        repeticao = hist_recente[0]
        count_seq = 0
        for resultado in hist_recente:
            if resultado == repeticao:
                count_seq += 1
            else:
                break
        sugestao = f"Sequência estendida de {count_seq} resultados de {mapear_cores[repeticao]}. A IA força você a acreditar que 'vai virar'. Sugestão: Mantenha a aposta na continuação até a quebra, ou aguarde a quebra e inverta."
        return "Padrão 2. Sequência Estendida", sugestao
    
    # --- Padrão de Âncora com Empate ---
    if len(hist_recente) >= 3 and 'E' in hist_recente[:3] and hist_recente[0] != 'E' and hist_recente[2] != 'E' and hist_recente[1] == 'E':
        sugestao = f"Empate (🟡) inserido no meio da sequência. A IA usa o empate para resetar a leitura e quebrar ciclos mentais. Sugestão: Reavalie o padrão. A tendência pode mudar agora."
        return "Padrão 3. Âncora com Empate", sugestao
    
    # --- Padrão Camuflado de Ciclo 3-1 ---
    if len(hist_recente) >= 4:
        if (hist_recente[0:3] == [hist_recente[0], hist_recente[0], hist_recente[0]] and hist_recente[3] != hist_recente[0]):
            sugestao = f"Ciclo 3-1 detectado ({mapear_cores[hist_recente[0]]}, {mapear_cores[hist_recente[0]]}, {mapear_cores[hist_recente[0]]}, {mapear_cores[hist_recente[3]]}). A IA tende a inverter o ciclo quando as apostas aumentam. Sugestão: Esteja preparado para a inversão."
            return "Padrão 4. Ciclo 3-1", sugestao
    
    # --- Padrão de Armadilha Pós-Ganho ---
    if len(hist_recente) >= 3 and hist_recente[0] == hist_recente[1] and hist_recente[2] != hist_recente[0]:
        sugestao = f"Armadilha Pós-Ganho detectada (ex: {mapear_cores[hist_recente[2]]} -> {mapear_cores[hist_recente[0]]}, {mapear_cores[hist_recente[0]]}). A IA força dois resultados opostos após uma vitória para derrubar quem dobra a aposta. Sugestão: Não dobre sua aposta após uma vitória neste momento."
        return "Padrão 6. Armadilha Pós-Ganho", sugestao
    
    # --- Padrão Espelho ---
    if len(hist_recente) >= 6 and hist_recente[0:3] == hist_recente[3:6][::-1]:
        sugestao = f"Padrão Espelho detectado (ex: {hist_recente[0]}{hist_recente[1]}{hist_recente[2]} -> {hist_recente[3]}{hist_recente[4]}{hist_recente[5]}). A IA inverte a sequência para confundir sua leitura. Sugestão: Não confie na repetição exata do padrão."
        return "Padrão 7. Espelho", sugestao

    # --- Padrão de Ruído Controlado (se nenhum outro for detectado) ---
    sugestao = "A sequência parece aleatória, mas a IA pode estar gerando pseudo-aleatoriedade com âncoras ocultas. Sugestão: Cautela, não há padrão claro. Evite apostas pesadas."
    return "Padrão 5. Ruído Controlado", sugestao

# --- Variáveis de Mapeamento ---
mapear_cores = {'A': 'Azul', 'E': 'Amarelo', 'V': 'Vermelho'}
mapear_emojis = {'A': '🔵', 'E': '🟡', 'V': '🔴'}

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
    if st.button("🔵 Vitória da Casa", use_container_width=True):
        st.session_state.historico.append('A')
with col2:
    if st.button("🟡 Empate", use_container_width=True):
        st.session_state.historico.append('E')
with col3:
    if st.button("🔴 Vitória de Fora", use_container_width=True):
        st.session_state.historico.append('V')
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
# Exibe o histórico de forma horizontal
historico_str = " ".join([mapear_emojis[r] for r in st.session_state.historico])
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
