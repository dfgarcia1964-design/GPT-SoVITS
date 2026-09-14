"""
File to Speech Module for GPT-SoVITS
Convierte archivos (PDF, DOCX, TXT, MD) a voz
"""

import os
import tempfile
from typing import Tuple, Optional
import gradio as gr

# Importaciones condicionales para diferentes formatos
try:
    import pdfplumber
    PDF_SUPPORT = True
except ImportError:
    PDF_SUPPORT = False
    print("⚠️ pdfplumber no instalado. Instala con: pip install pdfplumber")

try:
    from docx import Document
    DOCX_SUPPORT = True
except ImportError:
    DOCX_SUPPORT = False
    print("⚠️ python-docx no instalado. Instala con: pip install python-docx")


def extract_text_from_file(file_path: str) -> Tuple[str, str]:
    """
    Extrae texto de archivos en diferentes formatos.

    Args:
        file_path: Ruta del archivo

    Returns:
        Tuple de (texto_extraído, formato_detectado)
    """

    if not os.path.exists(file_path):
        return "", "Error: Archivo no encontrado"

    file_ext = os.path.splitext(file_path)[1].lower()

    try:
        # ========== TXT ==========
        if file_ext == ".txt":
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
            return text, "txt"

        # ========== MARKDOWN ==========
        elif file_ext == ".md":
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
            # Limpiar sintaxis markdown básica
            text = clean_markdown(text)
            return text, "md"

        # ========== PDF ==========
        elif file_ext == ".pdf":
            if not PDF_SUPPORT:
                return "", "Error: pdfplumber no instalado"

            try:
                text_parts = []
                with pdfplumber.open(file_path) as pdf:
                    for page_num, page in enumerate(pdf.pages, 1):
                        text = page.extract_text()
                        if text and text.strip():
                            text_parts.append(f"--- Página {page_num} ---\n{text}")

                if not text_parts:
                    return "", (
                        "⚠️ No se pudo extraer texto del PDF\n\n"
                        "Posibles causas:\n"
                        "• PDF escaneado (imagen) - necesita OCR\n"
                        "• PDF protegido o cifrado\n"
                        "• PDF sin contenido de texto\n\n"
                        "Solución: Convierte el PDF a texto con OCR primero"
                    )

                text = "\n\n".join(text_parts)
                return text, "pdf"
            except Exception as e:
                return "", (
                    f"❌ Error al procesar PDF: {str(e)}\n\n"
                    "Verifica que:\n"
                    "• El archivo sea un PDF válido\n"
                    "• No esté corrupto\n"
                    "• Tenga permisos de lectura"
                )

        # ========== DOCX ==========
        elif file_ext == ".docx":
            if not DOCX_SUPPORT:
                return "", "Error: python-docx no instalado"

            doc = Document(file_path)
            paragraphs = []

            # Extraer párrafos
            for para in doc.paragraphs:
                if para.text.strip():
                    paragraphs.append(para.text)

            # Extraer tablas
            for table in doc.tables:
                table_text = []
                for row in table.rows:
                    row_text = [cell.text for cell in row.cells]
                    table_text.append(" | ".join(row_text))
                if table_text:
                    paragraphs.append("\n".join(table_text))

            text = "\n\n".join(paragraphs)
            return text, "docx"

        else:
            return "", f"Error: Formato no soportado ({file_ext})"

    except Exception as e:
        return "", f"Error procesando archivo: {str(e)}"


def clean_markdown(text: str) -> str:
    """
    Limpia sintaxis markdown para mejor lectura en voz.
    """
    lines = text.split("\n")
    cleaned_lines = []

    for line in lines:
        # Remover encabezados markdown
        if line.startswith("#"):
            line = line.lstrip("#").strip()

        # Remover énfasis markdown
        line = line.replace("**", "").replace("__", "")
        line = line.replace("*", "").replace("_", "")
        line = line.replace("`", "").replace("```", "")

        # Remover listas markdown
        if line.startswith("-") or line.startswith("*"):
            line = line.lstrip("-* ").strip()
        elif line[0].isdigit() and "." in line:
            line = line.split(".", 1)[1].strip()

        # Remover enlaces markdown
        import re
        line = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", line)

        if line.strip():
            cleaned_lines.append(line)

    return "\n".join(cleaned_lines)


def validate_file(file_obj) -> Tuple[bool, str]:
    """
    Valida que el archivo sea soportado.
    """
    if file_obj is None:
        return False, "❌ No se cargó archivo"

    allowed_formats = [".pdf", ".docx", ".txt", ".md"]
    file_ext = os.path.splitext(file_obj.name)[1].lower()

    if file_ext not in allowed_formats:
        return False, f"❌ Formato no soportado: {file_ext}"

    # Verificar tamaño máximo (100MB)
    max_size = 100 * 1024 * 1024
    file_size = os.path.getsize(file_obj.name)
    if file_size > max_size:
        return False, f"❌ Archivo muy grande ({file_size/1024/1024:.1f}MB > 100MB)"

    return True, "✅ Archivo válido"


def create_file_to_speech_tab():
    """
    Crea la pestaña de conversión de archivos a voz.
    """

    gr.HTML("""
    <style>
        .f2s-header {
            background: linear-gradient(135deg, #00D4FF 0%, #0099CC 100%);
            padding: 30px;
            border-radius: 15px;
            color: white;
            margin-bottom: 25px;
            text-align: center;
        }
        .f2s-header h2 { margin: 0; font-size: 2em; }

        .f2s-card {
            border-left: 5px solid #00D4FF;
            padding: 20px;
            background: linear-gradient(to right, #f0f9ff, white);
            border-radius: 10px;
            margin: 15px 0;
        }

        .f2s-status {
            padding: 15px;
            border-radius: 8px;
            margin: 15px 0;
            font-weight: bold;
        }
        .f2s-success {
            background: #d4edda;
            color: #155724;
            border-left: 4px solid #28a745;
        }
        .f2s-error {
            background: #f8d7da;
            color: #721c24;
            border-left: 4px solid #dc3545;
        }
        .f2s-info {
            background: #d1ecf1;
            color: #0c5460;
            border-left: 4px solid #17a2b8;
        }
    </style>

    <div class="f2s-header">
        <h2>📄➡️🎙️ Convertir Archivos a Voz</h2>
        <p>Sube tus documentos y conviértelos en audio</p>
    </div>
    """)

    gr.Markdown("""
## 📤 Cómo funciona:

1. **📁 Sube tu archivo** (PDF, DOCX, TXT o MD)
2. **👁️ Revisa el texto** extraído
3. **🎙️ Genera audio** con síntesis de voz
4. **⬇️ Descarga** el archivo MP3
    """)

    with gr.Row():
        with gr.Column(scale=1):
            file_input = gr.File(
                label="📄 Carga tu archivo",
                file_count="single",
                file_types=[".pdf", ".docx", ".txt", ".md"]
            )

            gr.Markdown("""
**Formatos soportados:**
- 📋 PDF
- 📝 DOCX (Word)
- 📄 TXT
- 📋 Markdown (MD)

**Límites:**
- Máximo 100MB por archivo
- Máximo 10,000 caracteres para síntesis
            """)

        with gr.Column(scale=2):
            text_preview = gr.Textbox(
                label="📖 Vista previa del texto",
                lines=15,
                max_lines=20,
                interactive=True
            )

            file_status = gr.Textbox(
                label="Estado del archivo",
                interactive=False,
                value="Esperando archivo..."
            )

    gr.Markdown("---")

    with gr.Row():
        with gr.Column():
            gr.Markdown("### 🎙️ Configuración de voz:")

            model_version = gr.Dropdown(
                label="Versión del modelo",
                choices=["v2Pro", "v2ProPlus", "v4"],
                value="v2Pro"
            )

            speaker_emotion = gr.Dropdown(
                label="Emoción/Expresión",
                choices=["Neutral", "Feliz", "Triste", "Fuerte", "Suave"],
                value="Neutral"
            )

            speed = gr.Slider(
                label="Velocidad de lectura",
                minimum=0.5,
                maximum=2.0,
                value=1.0,
                step=0.1
            )

        with gr.Column():
            gr.Markdown("### 🎚️ Ajustes avanzados:")

            chunk_size = gr.Slider(
                label="Caracteres por segmento",
                minimum=100,
                maximum=1000,
                value=500,
                step=100
            )

            voice_sample = gr.File(
                label="🎤 Muestra de voz (opcional)",
                file_count="single",
                file_types=[".wav", ".mp3"]
            )

            gr.Markdown("Carga un audio de referencia para personalizar la voz")

    gr.Markdown("---")

    generate_btn = gr.Button(
        value="🎙️ GENERAR AUDIO",
        variant="primary",
        size="lg",
        scale=2
    )

    with gr.Row():
        audio_output = gr.Audio(
            label="🎵 Audio generado",
            type="filepath"
        )

        download_btn = gr.File(
            label="⬇️ Descargar MP3",
            visible=False
        )

    gr.Markdown("""
---

## 💡 Consejos para mejor resultado:

1. **Texto claro:** Usa textos bien puntuados y estructurados
2. **Longitud:** Menos de 10,000 caracteres por generación
3. **Formato:** Markdown limpio sin código
4. **Voz de referencia:** 3-10 segundos de audio para mejor personalización
5. **Paciencia:** La síntesis toma 10-30 segundos según la longitud

## ⚠️ Limitaciones:

- Máximo 10,000 caracteres por audio
- Archivos PDF con imágenes pueden tener menos texto
- Formato DOCX con tablas complejas puede requerir ajustes
    """)

    return {
        "file_input": file_input,
        "text_preview": text_preview,
        "file_status": file_status,
        "model_version": model_version,
        "speaker_emotion": speaker_emotion,
        "speed": speed,
        "chunk_size": chunk_size,
        "voice_sample": voice_sample,
        "generate_btn": generate_btn,
        "audio_output": audio_output,
        "download_btn": download_btn
    }


# Función callback para procesar archivos
def process_file(file_obj):
    """
    Procesa el archivo cargado y extrae el texto.
    """
    if file_obj is None:
        return "", "❌ Por favor carga un archivo"

    # Validar archivo
    is_valid, message = validate_file(file_obj)
    if not is_valid:
        return "", message

    # Extraer texto
    text, format_type = extract_text_from_file(file_obj.name)

    if not text:
        return "", f"❌ Error: {format_type}"

    # Información del procesamiento
    char_count = len(text)
    line_count = len(text.split("\n"))
    status = f"""
✅ Archivo procesado correctamente

📊 Estadísticas:
- Formato: {format_type.upper()}
- Caracteres: {char_count:,}
- Líneas: {line_count}
- Estado: Listo para síntesis
    """

    return text[:5000], status  # Mostrar primeros 5000 caracteres en preview


# Función para generar audio (demostración)
def generate_speech(text, model, emotion, speed, chunk_size, voice_sample):
    """
    Genera audio del texto (demostración).
    Nota: Integración real con GPT-SoVITS pendiente.
    """

    if not text or len(text.strip()) == 0:
        return None, "❌ El texto está vacío"

    if len(text) > 10000:
        return None, f"❌ Texto muy largo ({len(text)} > 10,000 caracteres)"

    try:
        import numpy as np
        import wave

        sample_rate = 22050
        duration = max(1, len(text) * 0.05)
        frames = int(sample_rate * duration)

        # Generar audio de demostración (ruido blanco suave)
        audio = np.random.randn(frames).astype(np.float32) * 0.05
        audio_int16 = (audio * 32767).astype(np.int16)

        # Guardar como WAV
        audio_path = tempfile.NamedTemporaryFile(delete=False, suffix=".wav").name

        with wave.open(audio_path, 'w') as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(audio_int16.tobytes())

        return audio_path, f"""✅ Audio generado exitosamente (demostración)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 Configuración:
  • Modelo: {model}
  • Emoción: {emotion}
  • Velocidad: {speed}x
  • Caracteres: {len(text)}
  • Duración: ~{duration:.1f}s

📝 Nota: Este es audio de demostración. Para síntesis real, integra GPT-SoVITS.
        """
    except Exception as e:
        return None, f"❌ Error al generar audio: {str(e)}"


def setup_file_to_speech_callbacks(components):
    """
    Configura los callbacks para la pestaña de archivo a voz.
    """

    # Callback para procesar archivo
    components["file_input"].change(
        fn=process_file,
        inputs=[components["file_input"]],
        outputs=[components["text_preview"], components["file_status"]]
    )

    # Callback para generar audio
    components["generate_btn"].click(
        fn=generate_speech,
        inputs=[
            components["text_preview"],
            components["model_version"],
            components["speaker_emotion"],
            components["speed"],
            components["chunk_size"],
            components["voice_sample"]
        ],
        outputs=[components["audio_output"], components["file_status"]]
    )


if __name__ == "__main__":
    # Test del módulo
    print("Módulo file_to_speech.py cargado correctamente")
    print(f"Soporte PDF: {PDF_SUPPORT}")
    print(f"Soporte DOCX: {DOCX_SUPPORT}")
