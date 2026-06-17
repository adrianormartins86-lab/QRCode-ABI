import streamlit as st
import qrcode
from io import BytesIO
from PIL import Image

# Configuração da página
st.set_page_config(page_title="Gerador de QR Code", page_icon="📱")

st.title("📱 Gerador de QR Code com Logo")
st.write("Insira um link e faça o upload de uma logo para gerar um QR Code personalizado.")

# Campo para o usuário passar o link
link = st.text_input("Cole o link aqui:")

# Campo para upload da logo
logo_file = st.file_uploader("Faça upload da logo (Opcional - PNG ou JPG)", type=["png", "jpg", "jpeg"])

# Criação do botão "Gerar QR Code"
if st.button("Gerar QR Code"):
    if link:
        # Lógica de criação do QR Code
        qr = qrcode.QRCode(
            version=1,
            # CRÍTICO: Mudar para ERROR_CORRECT_H para permitir que a logo cubra o centro sem quebrar a leitura
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(link)
        qr.make(fit=True)

        # Cria a imagem do QR Code e converte para RGB (necessário para colar imagens coloridas)
        img_qr = qr.make_image(fill_color="black", back_color="white").convert('RGB')

        # Se o usuário fez upload de uma logo, processa a imagem
        if logo_file is not None:
            logo = Image.open(logo_file)
            
            # Calcula o tamanho ideal da logo (aqui estamos usando cerca de 25% da largura do QR Code)
            basewidth = int(img_qr.size[0] / 4)
            wpercent = (basewidth / float(logo.size[0]))
            hsize = int((float(logo.size[1]) * float(wpercent)))
            
            # Redimensiona a logo com alta qualidade
            logo = logo.resize((basewidth, hsize), Image.Resampling.LANCZOS)
            
            # Converte a logo para RGBA para garantir que fundos transparentes funcionem (como no seu passarinho)
            logo = logo.convert("RGBA")
            
            # Calcula as coordenadas X e Y para colar a logo exatamente no centro
            pos_x = (img_qr.size[0] - logo.size[0]) // 2
            pos_y = (img_qr.size[1] - logo.size[1]) // 2
            
            # Cola a logo no centro do QR Code (usando a própria logo como máscara para preservar a transparência)
            img_qr.paste(logo, (pos_x, pos_y), logo)

        # Salva a imagem final na memória para exibir no site
        buf = BytesIO()
        img_qr.save(buf, format="PNG")
        byte_im = buf.getvalue()

        st.success("QR Code gerado com sucesso!")
        
        # Exibe a imagem centralizada
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(byte_im, use_container_width=True)
            
            # Botão para o usuário baixar a imagem
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
