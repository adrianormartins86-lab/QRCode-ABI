import streamlit as st
import qrcode
from io import BytesIO
from PIL import Image

# Configuração da página
st.set_page_config(page_title="Gerador de QR Code", page_icon="📱")

# --- NOVIDADE: Injeção de CSS para botões verdes elegantes ---
st.markdown("""
    <style>
    /* Estilização dos botões do Streamlit */
    div.stButton > button, div.stDownloadButton > button {
        background-color: #2E8B57 !important; /* Verde elegante (SeaGreen) */
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
        transition: all 0.3s ease !important;
    }
    
    /* Efeito ao passar o mouse (Hover) */
    div.stButton > button:hover, div.stDownloadButton > button:hover {
        background-color: #1f6b3f !important; /* Verde mais escuro */
        box-shadow: 0 6px 8px rgba(0,0,0,0.2) !important;
        transform: translateY(-2px) !important;
    }
    
    /* Cor do texto ao clicar (Active) */
    div.stButton > button:active, div.stDownloadButton > button:active {
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📱 Gerador de QR Code")
st.write("Insira um link e faça o upload de uma logo para gerar um QR Code personalizado.")

# Campo para o usuário passar o link
link = st.text_input("Cole o link aqui:")

# Coluna 1 (esquerda) com peso 2, Coluna 2 (direita) com peso 1
col_esq, col_dir = st.columns([2, 1])

with col_esq:
    # Campo para upload da logo fica na esquerda
    logo_file = st.file_uploader("Faça upload da logo (Opcional - PNG ou JPG)", type=["png", "jpg", "jpeg"])

with col_dir:
    # Pequeno truque para alinhar o botão mais para baixo, acompanhando o centro do uploader
    st.write("")
    st.write("")
    # O botão de gerar agora fica na direita
    gerar_btn = st.button("Gerar QR Code", use_container_width=True)

# A verificação agora é se a variável gerar_btn foi ativada
if gerar_btn:
    if link:
        # Lógica de criação do QR Code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(link)
        qr.make(fit=True)

        # Cria a imagem do QR Code e converte para RGB
        img_qr = qr.make_image(fill_color="black", back_color="white").convert('RGB')

        # Se o usuário fez upload de uma logo, processa a imagem
        if logo_file is not None:
            logo = Image.open(logo_file)
            
            # Calcula o tamanho ideal da logo
            basewidth = int(img_qr.size[0] / 4)
            wpercent = (basewidth / float(logo.size[0]))
            hsize = int((float(logo.size[1]) * float(wpercent)))
            
            # Redimensiona a logo com alta qualidade
            logo = logo.resize((basewidth, hsize), Image.Resampling.LANCZOS)
            
            # Converte a logo para RGBA
            logo = logo.convert("RGBA")
            
            # Calcula as coordenadas
            pos_x = (img_qr.size[0] - logo.size[0]) // 2
            pos_y = (img_qr.size[1] - logo.size[1]) // 2
            
            # Cola a logo no centro
            img_qr.paste(logo, (pos_x, pos_y), logo)

        # Salva a imagem final na memória
        buf = BytesIO()
        img_qr.save(buf, format="PNG")
        byte_im = buf.getvalue()

        st.success("QR Code gerado com sucesso!")
        
        # Exibe a imagem centralizada
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(byte_im, use_container_width=True)
            
            # Botão para baixar a imagem (também ficará verde por causa do CSS)
            st.download_button(
                label="Baixar Imagem (PNG)",
                data=byte_im,
                file_name="meu_qrcode_com_logo.png",
                mime="image/png",
                use_container_width=True
            )
    else:
        # Aviso caso o usuário clique em gerar com o campo vazio
        st.warning("Por favor, cole um link no campo acima antes de gerar.")
