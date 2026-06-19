import streamlit as st
import qrcode
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

# Configuração da página
st.set_page_config(page_title="Gerador de QR Code", page_icon="📱")

# --- Injeção de CSS para botões verdes elegantes ---
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

# Campos para o usuário
link = st.text_input("Cole o link aqui:")
titulo = st.text_input("Título do QR Code (Opcional - Ex: Básico, Corredor 3):")

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

        # --- NOVIDADE: Adicionando o Título no topo da imagem ---
        if titulo:
            # Tamanho da fonte fixado em 100 conforme solicitado
            tamanho_fonte = 1100 
            
            # Tenta carregar a fonte em NEGRITO (Bold)
            try:
                # 'arialbd.ttf' é o Arial Bold no Windows
                font = ImageFont.truetype("arialbd.ttf", tamanho_fonte)
            except IOError:
                try:
                    # 'DejaVuSans-Bold.ttf' é a versão negrito no servidor do Streamlit
                    font = ImageFont.truetype("DejaVuSans-Bold.ttf", tamanho_fonte)
                except IOError:
                    font = ImageFont.load_default()

            draw_temp = ImageDraw.Draw(img_qr)
            
            # Calcula o tamanho do texto para centralizar
            try:
                bbox = draw_temp.textbbox((0, 0), titulo, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
            except AttributeError:
                text_width, text_height = draw_temp.textsize(titulo, font=font)

            # Espaço em branco (+ 80) para dar um respiro maior já que a fonte cresceu
            header_height = text_height + 80 
            
            # Cria uma nova imagem com espaço extra no topo
            new_img = Image.new('RGB', (img_qr.width, img_qr.height + header_height), color='white')
            
            # Desenha o texto centralizado na nova imagem
            draw = ImageDraw.Draw(new_img)
            text_x = (new_img.width - text_width) // 2
            
            # Desce o texto um pouquinho (margem superior de 40)
            text_y = 40 
            
            draw.text((text_x, text_y), titulo, font=font, fill="black")
            
            # Cola o QR Code gerado abaixo do texto
            new_img.paste(img_qr, (0, header_height))
            
            # Substitui a variável para salvar a imagem completa
            img_qr = new_img

        # Salva a imagem final na memória
        buf = BytesIO()
        img_qr.save(buf, format="PNG")
        byte_im = buf.getvalue()

        st.success("QR Code gerado com sucesso!")
        
        # Exibe a imagem centralizada
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(byte_im, use_container_width=True)
            
            # Botão para baixar a imagem
            st.download_button(
                label="Baixar Imagem (PNG)",
                data=byte_im,
                file_name="qrcode_personalizado.png",
                mime="image/png",
                use_container_width=True
            )
    else:
        # Aviso caso o usuário clique em gerar com o campo vazio
        st.warning("Por favor, cole um link no campo acima antes de gerar.")
