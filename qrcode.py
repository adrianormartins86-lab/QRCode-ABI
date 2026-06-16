import streamlit as st
import qrcode
from io import BytesIO

# Configuração da página
st.set_page_config(page_title="Gerador de QR Code", page_icon="📱")

st.title("📱 Gerador de QR Code")
st.write("Insira um link ou texto abaixo para gerar o seu QR Code instantaneamente.")

# Campo para o usuário passar o link
link = st.text_input("Cole o link aqui:")

if link:
    # Lógica de criação do QR Code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(link)
    qr.make(fit=True)

    # Cria a imagem do QR Code
    img = qr.make_image(fill_color="black", back_color="white")

    # Salva a imagem na memória para exibir no site
    buf = BytesIO()
    img.save(buf, format="PNG")
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
            file_name="meu_qrcode.png",
            mime="image/png",
            use_container_width=True
        )
