import qrcode
from io import BytesIO
from PIL import Image, ImageDraw

def generate_qr_code(text: str) -> bytes:
    img = qrcode.make(text)
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return buffer.getvalue()


def generate_custom_qr_code(
        text: str,
        logo_path: str = None,
        qr_color: str = 'black',
        bg_color: str = 'white',
        logo_size: int = 50,
        version: int = 1,
        error_correction: str = 'L'
) -> bytes:
    # Mapeia o nível de correção de erro
    error_correction_map = {
        'L': qrcode.constants.ERROR_CORRECT_L,  # 7% de erro corrigido
        'M': qrcode.constants.ERROR_CORRECT_M,  # 15% de erro corrigido
        'Q': qrcode.constants.ERROR_CORRECT_Q,  # 25% de erro corrigido
        'H': qrcode.constants.ERROR_CORRECT_H,  # 30% de erro corrigido
    }

    # Verifica se o nível de correção de erro é válido
    error_correction_level = error_correction_map.get(error_correction.upper(), qrcode.constants.ERROR_CORRECT_L)

    # Cria o QR Code com os parâmetros fornecidos
    qr = qrcode.QRCode(
        version=version,  # Tamanho do QR Code
        error_correction=error_correction_level,  # Nível de correção de erro
        box_size=10,  # Tamanho de cada caixa
        border=4,  # Tamanho da borda
    )
    qr.add_data(text)
    qr.make(fit=True)

    # Gera a imagem do QR Code com cores personalizadas
    img = qr.make_image(fill=qr_color, back_color=bg_color)

    # Adiciona o logo, se fornecido
    if logo_path:
        logo = Image.open(logo_path)
        logo = logo.resize((logo_size, logo_size))  # Ajusta o tamanho do logo

        # Posição do logo no centro do QR Code
        img.paste(logo, ((img.size[0] - logo.size[0]) // 2, (img.size[1] - logo.size[1]) // 2), logo)

    # Salva o QR Code em um buffer de memória
    img_bytes = BytesIO()
    img.save(img_bytes, format="PNG")
    img_bytes.seek(0)

    return img_bytes.getvalue()
