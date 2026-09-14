#!/usr/bin/env python3
"""
GPT-SoVITS Complete WebUI with File-to-Speech Module
"""

import os
os.environ["version"] = "v2Pro"

import gradio as gr
import tempfile
from pathlib import Path

# Importar el módulo de archivo a voz
from file_to_speech import (
    create_file_to_speech_tab,
    setup_file_to_speech_callbacks,
    extract_text_from_file,
    validate_file,
    process_file,
    PDF_SUPPORT,
    DOCX_SUPPORT
)

def i18n(text):
    """Simple translation stub"""
    translations = {
        "Inicio Rápido": "Inicio Rápido",
        "Archivo a Voz": "Archivo a Voz",
        "Documentación": "Documentación",
    }
    return translations.get(text, text)

# ============ CREAR INTERFAZ ============

with gr.Blocks(
    title="GPT-SoVITS - Sistema Completo",
    theme=gr.themes.Soft()
) as app:

    gr.HTML("<h1 style='text-align: center;'>🎤 GPT-SoVITS - Sistema Completo</h1>")

    with gr.Tabs() as tabs_main:

        # ============ QUICK START TAB ============
        with gr.TabItem("⚡ " + i18n("Inicio Rápido")):

            gr.HTML("""
            <style>
                .qs-header {
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    padding: 40px;
                    border-radius: 15px;
                    color: white;
                    margin-bottom: 30px;
                    text-align: center;
                }
                .qs-header h1 {
                    margin: 0;
                    font-size: 2.5em;
                    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
                }
                .qs-card {
                    border-left: 6px solid #667eea;
                    padding: 25px;
                    background: linear-gradient(to right, #f8f9fa, white);
                    border-radius: 10px;
                    margin: 20px 0;
                    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.1);
                }
                .qs-btn {
                    font-weight: bold;
                    padding: 15px 30px !important;
                    border-radius: 10px;
                    font-size: 1.1em;
                }
                .qs-tip {
                    background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
                    border-left: 5px solid #2196F3;
                    padding: 20px;
                    border-radius: 8px;
                    margin: 20px 0;
                    font-size: 1.05em;
                }
            </style>

            <div class="qs-header">
                <h1>🚀 ¡Bienvenido a GPT-SoVITS!</h1>
                <p>Una herramienta poderosa para síntesis de voz basada en IA</p>
            </div>
            """)

            with gr.Row():
                with gr.Column(scale=3):
                    gr.Markdown("## 🎯 Elige tu camino")
                with gr.Column(scale=1):
                    theme_selector = gr.Radio(
                        label="Tema",
                        choices=["Claro", "Oscuro"],
                        value="Claro"
                    )

            gr.Markdown("---")

            # OPCIÓN 1: TTS
            with gr.Accordion(label="📚 Opción 1: TTS Rápido (5-30 seg)", open=True):
                with gr.Row():
                    with gr.Column(scale=2):
                        gr.HTML('<div class="qs-card">')
                        gr.Markdown("""
### ⏱️ **Lo más rápido**

Sintetiza voz inmediatamente.

**Ventajas:**
✅ 4 pasos simples
✅ Modelos entrenados
✅ Segundos
✅ Sin GPU
                        """)
                        gr.HTML('</div>')
                    with gr.Column(scale=1):
                        gr.Button("▶️ Ir a TTS", variant="primary", size="lg")

            # OPCIÓN 2: ENTRENAR
            with gr.Accordion(label="🎓 Opción 2: Entrenar (3-72 horas)", open=False):
                with gr.Row():
                    with gr.Column(scale=2):
                        gr.HTML('<div class="qs-card">')
                        gr.Markdown("""
### 🎤 **Tu voz personalizada**

Crea un modelo único.

**Ventajas:**
✅ Personalizado
✅ Automático
✅ Control total
✅ Profesional
                        """)
                        gr.HTML('</div>')
                    with gr.Column(scale=1):
                        gr.Button("▶️ Ir a Datos", variant="primary", size="lg")

            # OPCIÓN 3: CAMBIO DE VOZ
            with gr.Accordion(label="🔄 Opción 3: Cambio Voz (5-20 seg)", open=False):
                with gr.Row():
                    with gr.Column(scale=2):
                        gr.HTML('<div class="qs-card">')
                        gr.Markdown("""
### 🎭 **Transforma voces**

Convierte una voz en otra.

**Ventajas:**
✅ Sin entrenar
✅ Inmediato
✅ Control fino
✅ Creativo
                        """)
                        gr.HTML('</div>')
                    with gr.Column(scale=1):
                        gr.Button("▶️ Ir a Cambio", variant="primary", size="lg")

            gr.HTML("""
            <div class="qs-tip">
                <h3>💡 Inicia aquí</h3>
                <ol style="margin: 15px 0; padding-left: 25px;">
                    <li>Prueba TTS (5 min)</li>
                    <li>Explora cambio de voz</li>
                    <li>Entrena tu modelo</li>
                    <li>Convierte archivos</li>
                </ol>
            </div>
            """)

        # ============ FILE TO SPEECH TAB ============
        with gr.TabItem("📄➡️🎙️ " + i18n("Archivo a Voz")):

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
                .f2s-card {
                    border-left: 5px solid #00D4FF;
                    padding: 20px;
                    background: linear-gradient(to right, #f0f9ff, white);
                    border-radius: 10px;
                    margin: 15px 0;
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
3. **🎙️ Genera audio** con síntesis
4. **⬇️ Descarga** el MP3
            """)

            with gr.Row():
                with gr.Column(scale=1):
                    file_input = gr.File(
                        label="📄 Carga tu archivo",
                        file_count="single",
                        file_types=[".pdf", ".docx", ".txt", ".md"]
                    )

                    gr.Markdown(f"""
**Formatos soportados:**
- 📋 PDF {("✅" if PDF_SUPPORT else "❌")}
- 📝 DOCX {("✅" if DOCX_SUPPORT else "❌")}
- 📄 TXT ✅
- 📋 MD ✅

**Límites:**
- Máximo 100MB
- Máximo 10,000 caracteres
                    """)

                with gr.Column(scale=2):
                    text_preview = gr.Textbox(
                        label="📖 Vista previa del texto",
                        lines=12,
                        max_lines=15,
                        interactive=True
                    )

                    file_status = gr.Textbox(
                        label="Estado",
                        interactive=False,
                        value="Esperando archivo..."
                    )

            gr.Markdown("---")

            with gr.Row():
                with gr.Column():
                    gr.Markdown("### 🎙️ Configuración:")

                    model_v = gr.Dropdown(
                        label="Modelo",
                        choices=["v2Pro", "v2ProPlus", "v4"],
                        value="v2Pro"
                    )

                    emotion = gr.Dropdown(
                        label="Emoción",
                        choices=["Neutral", "Feliz", "Triste"],
                        value="Neutral"
                    )

                    speed = gr.Slider(
                        label="Velocidad",
                        minimum=0.5,
                        maximum=2.0,
                        value=1.0,
                        step=0.1
                    )

                with gr.Column():
                    gr.Markdown("### 🎚️ Avanzado:")

                    chunk_size = gr.Slider(
                        label="Caracteres/segmento",
                        minimum=100,
                        maximum=1000,
                        value=500,
                        step=100
                    )

                    voice_sample = gr.File(
                        label="🎤 Muestra de voz",
                        file_count="single",
                        file_types=[".wav", ".mp3"]
                    )

            gr.Markdown("---")

            generate_btn = gr.Button(
                value="🎙️ GENERAR AUDIO",
                variant="primary",
                size="lg"
            )

            with gr.Row():
                audio_output = gr.Audio(
                    label="🎵 Audio generado"
                )
                download_btn = gr.File(
                    label="⬇️ Descargar MP3"
                )

            gr.Markdown("""
---

## 💡 Consejos:

1. **Texto claro** y bien puntuado
2. **Menos de 10,000** caracteres
3. **Markdown limpio** sin código
4. **Voz de referencia** 3-10 segundos
5. **Paciencia** - 10-30 segundos
            """)

            # Setup callbacks
            file_input.change(
                fn=process_file,
                inputs=[file_input],
                outputs=[text_preview, file_status]
            )

            generate_btn.click(
                fn=lambda text, model, emotion, speed, chunk, voice: (
                    None,
                    f"✅ Generación iniciada\n- Modelo: {model}\n- Emoción: {emotion}\n- Velocidad: {speed}x\n- Caracteres: {len(text) if text else 0}\n\n⏳ Procesando... (Esta es una demostración)"
                ),
                inputs=[text_preview, model_v, emotion, speed, chunk_size, voice_sample],
                outputs=[audio_output, file_status]
            )

        # ============ DOCUMENTATION TAB ============
        with gr.TabItem("📚 Documentación"):

            gr.HTML("""
            <style>
                .doc-header {
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    padding: 30px;
                    border-radius: 15px;
                    color: white;
                    margin-bottom: 25px;
                    text-align: center;
                }
            </style>

            <div class="doc-header">
                <h2>📚 Documentación de GPT-SoVITS</h2>
            </div>
            """)

            gr.Markdown("""
### 🎯 Sistema Completo GPT-SoVITS

**Funcionalidades:**
- ✅ Síntesis de voz con modelos preentrenados
- ✅ Entrenamiento personalizado
- ✅ Cambio de voz
- ✅ **Conversión de archivos a voz**

### 🔗 Enlaces

- **GitHub:** https://github.com/RVC-Boss/GPT-SoVITS
- **Comunidad:** Discord oficial

### 📄 Convertir Archivos

Convierte fácilmente tus documentos en audio:
- Soporta PDF, DOCX, TXT, Markdown
- Extrae texto automáticamente
- Sintetiza con tu voz preferida
- Descarga el audio generado

### ⚖️ Licencia MIT

Responsabilidades:
- Respeta derechos de voz
- Usa eticamente
- Cumple leyes locales
            """)

if __name__ == "__main__":
    app.launch(server_name="127.0.0.1", server_port=7860, share=False)
