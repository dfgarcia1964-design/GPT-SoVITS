# Enhanced Quick Start Module for GPT-SoVITS
# Insert this into webui.py after the import statements and before the app creation

import gradio as gr

def create_quickstart_tab(i18n):
    """
    Create an enhanced Quick Start tab with all features:
    - Multiple workflow options
    - Interactive buttons with navigation
    - Comprehensive FAQ
    - Theme selector
    - Advanced options
    - Tutorial links
    """

    # Create tabs container
    with gr.Tabs() as tabs_main:

        # ============ QUICK START TAB ============
        with gr.TabItem("⚡ " + i18n("Inicio Rápido")):

            # Header with styling
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
                .qs-header h1 { margin: 0; font-size: 2.5em; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); }
                .qs-header p { margin: 15px 0 0 0; font-size: 1.1em; opacity: 0.95; }

                .qs-card {
                    border-left: 6px solid #667eea;
                    padding: 25px;
                    background: linear-gradient(to right, #f8f9fa, white);
                    border-radius: 10px;
                    margin: 20px 0;
                    box-shadow: 0 2px 8px rgba(102, 126, 234, 0.1);
                }

                .qs-btn {
                    font-weight: bold;
                    padding: 15px 30px;
                    border-radius: 10px;
                    font-size: 1.1em;
                }

                .feature-list {
                    list-style: none;
                    padding: 0;
                    margin: 15px 0;
                }
                .feature-list li {
                    padding: 10px 0;
                    margin-left: 30px;
                    font-size: 1.05em;
                }
                .feature-list li:before {
                    content: "✅ ";
                    margin-left: -30px;
                    margin-right: 15px;
                    color: #667eea;
                    font-weight: bold;
                    font-size: 1.2em;
                }

                .qs-steps {
                    background: #f0f4ff;
                    padding: 20px;
                    border-radius: 8px;
                    margin: 15px 0;
                }

                .qs-tip {
                    background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
                    border-left: 5px solid #2196F3;
                    padding: 20px;
                    border-radius: 8px;
                    margin: 20px 0;
                    font-size: 1.05em;
                }

                .qs-comparison {
                    width: 100%;
                    border-collapse: collapse;
                    margin: 20px 0;
                    background: white;
                }
                .qs-comparison th {
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 15px;
                    text-align: left;
                    font-weight: bold;
                }
                .qs-comparison td {
                    padding: 12px 15px;
                    border-bottom: 1px solid #e0e0e0;
                }
                .qs-comparison tr:nth-child(even) { background: #f8f9fa; }
                .qs-comparison tr:hover { background: #e8eaf6; }
            </style>

            <div class="qs-header">
                <h1>🚀 ¡Bienvenido a GPT-SoVITS!</h1>
                <p>Una herramienta poderosa para síntesis de voz basada en IA</p>
            </div>
            """)

            # Title and Theme selector
            with gr.Row():
                with gr.Column(scale=3):
                    gr.Markdown("## 🎯 " + i18n("Elige tu camino según tus necesidades"))
                with gr.Column(scale=1):
                    theme_selector = gr.Radio(
                        label=i18n("Tema"),
                        choices=[i18n("Claro"), i18n("Oscuro")],
                        value=i18n("Claro"),
                        interactive=True
                    )

            gr.Markdown("---")

            # ========== OPTION 1: TTS ==========
            with gr.Accordion(label="📚 " + i18n("Opción 1: TTS Rápido (5-30 segundos)"), open=True) as acc1:
                with gr.Row():
                    with gr.Column(scale=7):
                        gr.HTML('<div class="qs-card">')
                        gr.Markdown("""
### ⏱️ **Lo más rápido para empezar**

Sintetiza voz **inmediatamente** sin entrenamiento previo.

**✅ Ventajas:**
- Solo 4 pasos simples
- Modelos ya entrenados y optimizados
- Resultados en segundos
- Sin necesidad de GPU

**🎯 Casos de uso:**
- Pruebas rápidas de la herramienta
- Demostraciones de cliente
- Prototipos
- Contenido no crítico
                        """)

                        gr.HTML('<div class="qs-steps">')
                        gr.Markdown("""
**Pasos:**
1️⃣ Elige modelo y versión (v2Pro recomendado)
2️⃣ Ingresa el texto a sintetizar
3️⃣ Configura la voz de referencia
4️⃣ ¡Genera tu audio!
                        """)
                        gr.HTML('</div>')
                        gr.HTML('</div>')

                    with gr.Column(scale=3):
                        tts_btn = gr.Button(
                            value="▶️ " + i18n("Ir a TTS"),
                            variant="primary",
                            size="lg",
                            elem_classes="qs-btn"
                        )
                        # Note: In actual integration, add: tts_btn.click(lambda: 1, outputs=tabs_main)

                        gr.Markdown("""
**⏱️ Tiempo:** 5-30 seg

**🎥 Tutorial:**
Ver demos en GitHub

**💡 Pro tip:**
Usa v2Pro para
mejor balance
                        """)

            # ========== OPTION 2: TRAIN ==========
            with gr.Accordion(label="🎓 " + i18n("Opción 2: Entrenar tu modelo (3-72 horas)"), open=False):
                with gr.Row():
                    with gr.Column(scale=7):
                        gr.HTML('<div class="qs-card">')
                        gr.Markdown("""
### 🎤 **Crea tu voz personalizada**

Entrena un modelo único con tu propia voz para máxima calidad.

**✅ Ventajas:**
- Voz completamente personalizada
- Herramientas automáticas
- Control total del proceso
- Calidad profesional

**🎯 Casos de uso:**
- Producción profesional
- Contenido comercial
- Proyectos a largo plazo
- Máxima personalización
                        """)

                        gr.HTML('<div class="qs-steps">')
                        gr.Markdown("""
**Flujo de trabajo:**

📊 **Paso 0:** Preparar datos
   • UVR5: Separa voz e instrumentos
   • Slicer: Divide en segmentos
   • ASR: Transcribe automáticamente

🔧 **Paso 1A:** Formatear datos

⚙️ **Paso 1B:** Entrenar modelo

🎵 **Paso 1C:** Usar modelo entrenado
                        """)
                        gr.HTML('</div>')
                        gr.HTML('</div>')

                    with gr.Column(scale=3):
                        train_btn = gr.Button(
                            value="▶️ " + i18n("Ir a Datos"),
                            variant="primary",
                            size="lg",
                            elem_classes="qs-btn"
                        )

                        gr.Markdown("""
**⏱️ Tiempo total:**
2-24 horas (GPU)
24-72 horas (CPU)

**📊 Datos ideales:**
50+ minutos audio
16kHz, WAV limpio

**💪 Requisitos:**
GPU 6GB+ VRAM
                        """)

            # ========== OPTION 3: VOICE CONVERSION ==========
            with gr.Accordion(label="🔄 " + i18n("Opción 3: Cambio de Voz (5-20 segundos)"), open=False):
                with gr.Row():
                    with gr.Column(scale=7):
                        gr.HTML('<div class="qs-card">')
                        gr.Markdown("""
### 🎭 **Transforma voces existentes**

Convierte una voz en otra usando audio de referencia.

**✅ Ventajas:**
- Sin entrenar nuevos modelos
- Resultados inmediatos
- Control fino de la voz
- Muy creativo y divertido

**🎯 Casos de uso:**
- Cambios de género
- Imitaciones
- Efectos creativos
- Experimentos de voz
                        """)

                        gr.HTML('<div class="qs-steps">')
                        gr.Markdown("""
**Pasos:**
1️⃣ Carga audio para transformar
2️⃣ Proporciona voz destino (3-10s)
3️⃣ Ajusta parámetros (opcional)
4️⃣ ¡Obtén resultado transformado!
                        """)
                        gr.HTML('</div>')
                        gr.HTML('</div>')

                    with gr.Column(scale=3):
                        voice_btn = gr.Button(
                            value="▶️ " + i18n("Ir a Cambio"),
                            variant="primary",
                            size="lg",
                            elem_classes="qs-btn"
                        )

                        gr.Markdown("""
**⏱️ Tiempo:** 5-20 seg

**🎬 Demostraciones:**
Ver en GitHub

**🎯 Calidad:**
Depende de la
voz referencia
                        """)

            # ========== OPTION 4: ADVANCED ==========
            with gr.Accordion(label="🚀 " + i18n("Opción 4: Funciones Avanzadas"), open=False):
                gr.HTML('<div class="qs-card">')
                gr.Markdown("""
### 🔬 **Características avanzadas para profesionales**

**Herramientas avanzadas:**
- Fine-tuning de modelos existentes
- Control de emociones y expresiones
- Síntesis en batch (múltiples archivos)
- API REST para integración
- Integración con sistemas externos
- Generación de audio con efectos

**Requisitos técnicos:**
- Conocimiento técnico moderado
- GPU muy potente (10GB+ VRAM)
- Datos extensos y bien organizados
- Paciencia para experimentación

**Documentación:**
Consulta GitHub Issues y Discussions para casos específicos.
                """)
                gr.HTML('</div>')

            gr.Markdown("---")

            # ========== FAQ ==========
            with gr.Accordion(label="❓ " + i18n("Preguntas Frecuentes"), open=False):
                with gr.Tabs():

                    # General FAQ
                    with gr.TabItem("🤔 " + i18n("General")):
                        gr.Markdown("""
### ¿Cuál es la mejor opción para mí?

| Opción | Tiempo | Dificultad | Personalización | Para |
|--------|--------|-----------|-----------------|------|
| **TTS** | Segundos | ⭐ Muy fácil | Baja | Pruebas rápidas |
| **Entrenar** | Horas | ⭐⭐⭐ Moderada | Muy alta | Producción |
| **Cambio voz** | Segundos | ⭐⭐ Fácil | Media | Creatividad |

### ¿Necesito conocimientos técnicos?
❌ **No.** La interfaz es muy amigable y guiada. Solo sigue los pasos.

### ¿Puedo cancelar entrenamientos?
✅ **Sí.** Haz clic en "Cerrar Proceso" en cualquier momento sin perder datos.

### ¿Es seguro?
✅ **Sí.** GPT-SoVITS es open-source. Revisa el código en GitHub.

### ¿Puedo usar esto comercialmente?
📋 **Depende.** GPT-SoVITS es MIT, pero verifica permisos de voces/contenido.
                        """)

                    # Technical FAQ
                    with gr.TabItem("⚙️ " + i18n("Técnico")):
                        gr.Markdown("""
### ¿Qué versión de modelo debo usar?

- **v1:** Legacy, no recomendado
- **v2Pro:** ⭐ **Recomendado** - Balance perfecto calidad/velocidad
  - Requisitos: GPU NVIDIA 6GB+ VRAM
  - Mejor para: Mayoría de casos

- **v2ProPlus:** Mejor calidad que v2Pro
  - Requisitos: GPU NVIDIA 8GB+ VRAM
  - Mejor para: Calidad crítica

- **v4:** Máxima calidad
  - Requisitos: GPU NVIDIA 10GB+ o A100
  - Mejor para: Producción premium

### ¿Necesito GPU?

**Recomendado:** GPU NVIDIA con 6GB+ VRAM (CUDA)
- RTX 3060/4060 funciona perfecto
- RTX series mejor que GTX

**Sin GPU (CPU):** Sí funciona pero:
- 10-50x más lento
- Entrenamientos son impracticables
- Solo TTS posible pero lento

**Requisitos de RAM:**
- Mínimo: 8GB
- Recomendado: 16GB

### ¿Qué requisitos de audio?

- **Formato:** WAV, MP3, OGG, FLAC (cualquiera)
- **Duración mínima:** 5-10 segundos por muestra
- **Duración recomendada:** 1+ minuto total
- **Frecuencia de muestreo:** 16kHz óptimo (16-48kHz OK)
- **Calidad:** Limpio, mínimo ruido de fondo
- **Mono:** Mejor que estéreo para entrenamiento
                        """)

                    # Quality FAQ
                    with gr.TabItem("📈 " + i18n("Mejora de calidad")):
                        gr.Markdown("""
### 🎤 Datos de entrenamiento

1. **Usa audio de alta calidad**
   - Limpio, sin ruido de fondo
   - Sin compresión si es posible

2. **Más datos = mejor modelo**
   - Mínimo: 20 minutos
   - Recomendado: 50+ minutos
   - Óptimo: 100+ minutos

3. **Consistencia**
   - Misma persona en todo el dataset
   - Similar calidad de grabación

4. **Variedadbla**
   - Diferentes emociones
   - Ritmos variados
   - Tonos distintos

### ⚙️ Configuración de entrenamiento

5. **Entrena suficientes épocas**
   - Típico: 200-400 épocas
   - Monitorea la pérdida

6. **Batch size apropiado**
   - Depende de tu GPU
   - Más grande = más rápido pero más RAM

7. **Validación regular**
   - Escucha samples durante entrenamiento
   - Para si empieza a empeorar

### 🎵 Durante inferencia

8. **Textos claros**
   - Bien estructurados
   - Puntuación correcta

9. **Audio de referencia de calidad**
   - 3-10 segundos
   - Claro y limpio
   - Misma emoción deseada

10. **Ajusta parámetros**
    - Temperatura (0.3-0.7 típico)
    - Valores de control
    - Experimenta
                        """)

            # Tip Box
            gr.HTML("""
            <div class="qs-tip">
                <h3>💡 Consejo de inicio rápido</h3>
                <ol style="margin: 15px 0; padding-left: 25px;">
                    <li><strong>Paso 1:</strong> Prueba TTS (Opción 1) primero para familiarizarte (5 min)</li>
                    <li><strong>Paso 2:</strong> Explora cambio de voz si tienes audio (10 min)</li>
                    <li><strong>Paso 3:</strong> Colecta datos para entrenar tu modelo (1-7 días)</li>
                    <li><strong>Paso 4:</strong> Entrena tu primer modelo (2-24 horas)</li>
                    <li><strong>Paso 5:</strong> Experimenta y mejora (continuo)</li>
                </ol>
                <p><strong>📚 Documentación oficial:</strong> <a href="https://github.com/RVC-Boss/GPT-SoVITS" target="_blank">GitHub - RVC-Boss/GPT-SoVITS</a></p>
                <p><strong>💬 Comunidad:</strong> Discord oficial para ayuda en tiempo real</p>
                <p><strong>🐛 Problemas:</strong> Revisa GitHub Issues - muchas preguntas ya resueltas</p>
            </div>
            """)

    return tabs_main
