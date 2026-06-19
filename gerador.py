import streamlit as st
import qrcode
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import os

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
    logo_file = st.file_uploader("Faça upload da logo (Opcional - PNG ou JPG)", type=["png", "jpg", "jpeg"])

with col_dir:
    st.write("")
    st.write("")
    gerar_btn = st.button("Gerar QR Code", use_container_width=True)

if gerar_btn:
    if link:
        # Cria o QR Code base
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(link)
        qr.make(fit=True)

        img_qr = qr.make_image(fill_color="black", back_color="white").convert('RGB')

        # Cola a logo se existir
        if logo_file is not None:
            logo = Image.open(logo_file)
            basewidth = int(img_qr.size[0] / 4)
            wpercent = (basewidth / float(logo.size[0]))
            hsize = int((float(logo.size[1]) * float(wpercent)))
            logo = logo.resize((basewidth, hsize), Image.Resampling.LANCZOS)
            logo = logo.convert("RGBA")
            pos_x = (img_qr.size[0] - logo.size[0]) // 2
            pos_y = (img_qr.size[1] - logo.size[1]) // 2
            img_qr.paste(logo, (pos_x, pos_y), logo)

        # --- SISTEMA DE TÍTULO COM FONTE LOCAL ---
        if titulo:
            draw_temp = ImageDraw.Draw(img_qr)
            
            # O nome do arquivo que você subiu no GitHub
            font_path = "fonte.ttf" 
            
            if not os.path.exists(font_path):
                st.error("⚠️ O arquivo 'fonte.ttf' não foi encontrado! Por favor, suba ele no seu GitHub na mesma pasta do código.")
                st.stop() # Para a execução aqui para você corrigir
            
            # Definimos a meta: o texto deve ocupar 80% da largura do QR Code
            largura_alvo = img_qr.width * 0.8
            tamanho_fonte = 20 # Tamanho inicial
            
            # Inicia a fonte local
            font = ImageFont.truetype(font_path, tamanho_fonte)
            
            # LOOP MÁGICO: Aumenta a fonte até bater 80% da largura
            while True:
                try:
                    bbox = draw_temp.textbbox((0, 0), titulo, font=font)
                    text_width = bbox[2] - bbox[0]
                    text_height = bbox[3] - bbox[1]
                except AttributeError:
                    text_width, text_height = draw_temp.textsize(titulo, font=font)
                    
                if text_width >= largura_alvo or tamanho_fonte >= 300:
                    break
                
                tamanho_fonte += 2
                font = ImageFont.truetype(font_path, tamanho_fonte)

            # Altura do cabeçalho = altura do texto + 80 pixels de margem para "respirar"
            header_height = text_height + 80 
            
            # Cria uma nova imagem com espaço extra no topo
            new_img = Image.new('RGB', (img_qr.width, img_qr.height + header_height), color='white')
            
            # Desenha o texto
            draw = ImageDraw.Draw(new_img)
            text_x = (new_img.width - text_width) // 2
            text_y = (header_height - text_height) // 2
            
            draw.text((text_x, text_y), titulo, font=font, fill="black")
            new_img.paste(img_qr, (0, header_height))
            img_qr = new_img

        # Salva e exibe
        buf = BytesIO()
        img_qr.save(buf, format="PNG")
        byte_im = buf.getvalue()

        st.success("QR Code gerado com sucesso!")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(byte_im, use_container_width=True)
            st.download_button(
                label="Baixar Imagem (PNG)",
                data=byte_im,
                file_name="qrcode_personalizado.png",
                mime="image/png",
                use_container_width=True
            )
    else:
        st.warning("Por favor, cole um link no campo acima antes de gerar.")
