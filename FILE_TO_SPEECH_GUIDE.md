# Funcionalidad de Conversión de Archivos a Voz

## 📄➡️🎙️ Resumen

Se ha implementado una **nueva funcionalidad completa** para convertir archivos (PDF, DOCX, TXT, MD) en audio utilizando GPT-SoVITS.

---

## 🚀 Características Implementadas

### ✅ Soporta múltiples formatos:
- **📋 PDF** - Extrae texto de todas las páginas
- **📝 DOCX** - Soporta párrafos y tablas
- **📄 TXT** - Texto plano
- **📋 Markdown** - Convierte limpiando sintaxis

### ✅ Procesamiento inteligente:
- Extracción automática de texto
- Limpieza de markdown (eliminación de # ** * _ etc)
- Validación de archivos (máximo 100MB)
- Preview del texto extraído

### ✅ Opciones de personalización:
- Selector de modelo (v2Pro, v2ProPlus, v4)
- Selección de emoción/expresión
- Control de velocidad de lectura
- Tamaño de segmento configurable
- Muestra de voz opcional para personalización

---

## 📁 Archivos Generados

### 1. **file_to_speech.py** (Módulo principal)
```python
- extract_text_from_file()  # Extrae texto de cualquier formato
- clean_markdown()          # Limpia sintaxis markdown
- validate_file()           # Valida archivos
- process_file()            # Procesa archivos cargados
- create_file_to_speech_tab()  # Crea la pestaña UI
```

### 2. **webui_complete.py** (Interfaz integrada)
- Incluye todas las 3 pestañas:
  - ⚡ Inicio Rápido
  - 📄➡️🎙️ Archivo a Voz
  - 📚 Documentación

---

## 🎯 Cómo Usar

### Opción 1: Ejecutar la interfaz completa
```bash
cd C:\Users\dfgar\OneDrive\reloges\GitHub
python webui_complete.py
# Abre http://localhost:7860
```

### Opción 2: Usar solo el módulo
```python
from file_to_speech import extract_text_from_file, process_file

# Extraer texto
text, format_type = extract_text_from_file("documento.pdf")
print(f"Extraído: {len(text)} caracteres de {format_type}")

# Procesar archivo cargado
text_preview, status = process_file(file_object)
```

---

## 📊 Flujo de uso

```
┌─────────────────────┐
│  1. Cargar archivo  │
│ (PDF/DOCX/TXT/MD)  │
└──────────┬──────────┘
           │
┌──────────▼──────────┐
│ 2. Extraer texto    │
│    Validar archivo  │
└──────────┬──────────┘
           │
┌──────────▼──────────┐
│ 3. Preview texto    │
│    Editar si es     │
│    necesario        │
└──────────┬──────────┘
           │
┌──────────▼──────────┐
│ 4. Configurar voz   │
│    Modelo, emoción  │
│    Velocidad, etc   │
└──────────┬──────────┘
           │
┌──────────▼──────────┐
│ 5. Generar audio    │
│    Síntesis TTS     │
└──────────┬──────────┘
           │
┌──────────▼──────────┐
│ 6. Descargar MP3    │
│    Audio generado   │
└─────────────────────┘
```

---

## 🔧 Funciones Técnicas

### `extract_text_from_file(file_path: str) -> Tuple[str, str]`
Extrae texto de archivos en diferentes formatos.

```python
# Uso
text, format_type = extract_text_from_file("documento.pdf")
# Retorna: (texto_extraído, "pdf")
```

**Soporta:**
- `.txt` - Lectura directa
- `.md` - Lectura + limpieza markdown
- `.pdf` - Extrae de todas las páginas (requiere pdfplumber)
- `.docx` - Párrafos y tablas (requiere python-docx)

---

### `clean_markdown(text: str) -> str`
Limpia sintaxis markdown para mejor lectura.

```python
# Entrada:
# ## Título
# **Texto importante** en *cursiva*

# Salida:
# Título
# Texto importante en cursiva
```

**Elimina:**
- Encabezados markdown (#)
- Énfasis (\*\*bold\*\*, \*italic\*)
- Listas (-, *, números)
- Enlaces markdown
- Código

---

### `validate_file(file_obj) -> Tuple[bool, str]`
Valida archivo antes de procesar.

```python
is_valid, message = validate_file(file_object)
# Retorna: (True, "✅ Archivo válido")
```

**Validaciones:**
- Formato soportado
- Tamaño máximo 100MB
- Archivo existe

---

### `process_file(file_obj) -> Tuple[str, str]`
Procesa archivo cargado y retorna preview.

```python
text_preview, status = process_file(file_object)
# Retorna: (primeros_5000_chars, estado_procesamiento)
```

---

## 📋 Parámetros de Configuración

### Configuración de voz
| Parámetro | Rango | Defecto | Descripción |
|-----------|-------|---------|-------------|
| **Modelo** | v2Pro, v2ProPlus, v4 | v2Pro | Versión del modelo |
| **Emoción** | Neutral, Feliz, Triste | Neutral | Expresión al hablar |
| **Velocidad** | 0.5 - 2.0 | 1.0 | Multiplicador de velocidad |

### Configuración avanzada
| Parámetro | Rango | Defecto | Descripción |
|-----------|-------|---------|-------------|
| **Chunk size** | 100 - 1000 | 500 | Caracteres por segmento |
| **Voz referencia** | Archivo | None | Muestra para personalización |

---

## 💾 Requisitos de Instalación

### Para soporte PDF:
```bash
pip install pdfplumber
```

### Para soporte DOCX:
```bash
pip install python-docx
```

### Dependencias base:
```bash
pip install gradio
```

---

## 📊 Estadísticas y Límites

### Límites de archivo:
- **Tamaño máximo:** 100 MB
- **Caracteres para síntesis:** 10,000 máximo
- **Formatos:** PDF, DOCX, TXT, MD

### Rendimiento estimado:
| Caracteres | Tiempo estimado |
|-----------|-----------------|
| 500 | 5-10 seg |
| 1,000 | 10-20 seg |
| 5,000 | 30-60 seg |
| 10,000 | 60-120 seg |

---

## 🎨 Interfaz Visual

### Pestaña "Archivo a Voz"

```
┌─────────────────────────────────────────────┐
│  📄➡️🎙️ Convertir Archivos a Voz             │
│  Sube tus documentos y conviértelos en audio │
└─────────────────────────────────────────────┘

┌──────────────────┐  ┌──────────────────┐
│ 📁 Cargar archivo│  │📖 Vista previa   │
│                  │  │                  │
│  (PDF/DOCX/etc)  │  │ (Texto extraído) │
└──────────────────┘  └──────────────────┘

┌──────────────────┐  ┌──────────────────┐
│🎙️ Configuración  │  │🎚️ Avanzado      │
│                  │  │                  │
│ Modelo           │  │ Chunk size       │
│ Emoción          │  │ Voz referencia   │
│ Velocidad        │  │                  │
└──────────────────┘  └──────────────────┘

┌──────────────────────────────────────────┐
│    🎙️ GENERAR AUDIO (Botón primario)    │
└──────────────────────────────────────────┘

┌──────────────────┐  ┌──────────────────┐
│🎵 Audio generado │  │⬇️ Descargar MP3  │
│                  │  │                  │
│ (Player HTML5)   │  │ (Descarga)       │
└──────────────────┘  └──────────────────┘
```

---

## 🔒 Seguridad y Privacidad

✅ **Validaciones implementadas:**
- Verificación de tipos de archivo
- Límite de tamaño (100MB)
- Limpieza de markdown
- Información del usuario no se almacena

⚠️ **Consideraciones:**
- Los archivos se procesan temporalmente
- Usa GPT-SoVITS localmente (no en la nube)
- Verifica permisos de copyright

---

## 🐛 Troubleshooting

### Error: "pdfplumber no instalado"
```bash
pip install pdfplumber
```

### Error: "python-docx no instalado"
```bash
pip install python-docx
```

### Error: "Archivo muy grande"
- Máximo permitido: 100MB
- Divide archivos grandes

### Error: "Formato no soportado"
- Usa: PDF, DOCX, TXT, Markdown
- Convierte otros formatos primero

---

## 📚 Ejemplos de Uso

### Ejemplo 1: Convertir TXT
```
1. Cargar: documento.txt
2. Preview: Se muestra el texto
3. Configurar: v2Pro, Neutral, 1.0x
4. Generar: Clic en botón
5. Descargar: documento_audio.mp3
```

### Ejemplo 2: Convertir PDF multipágina
```
1. Cargar: libro.pdf (10 páginas)
2. Preview: Muestra combinado de todas
3. Ajustar si es necesario
4. Generar audio
5. Resultado: Audio de libro completo
```

### Ejemplo 3: Personalizar con voz
```
1. Cargar: articulo.md
2. Subir muestra: mi_voz.wav
3. Modelo: v2ProPlus (mejor calidad)
4. Emoción: Feliz
5. Generar: Audio con mi voz personalizada
```

---

## 🎯 Casos de Uso

| Caso de Uso | Archivo | Config |
|------------|---------|--------|
| **Audiolibro** | PDF/DOCX grande | v4, Normal, 1.0x |
| **Presentación** | TXT corto | v2Pro, Feliz, 1.2x |
| **Narración** | Markdown | v2ProPlus, Normal, 1.0x |
| **Aprendizaje** | Notas TXT | v2Pro, Suave, 0.8x |
| **Podcasts** | DOCX guión | v4 + voz ref | 1.1x |

---

## 🚀 Próximos Pasos

1. **Corto plazo:**
   - Usar la funcionalidad
   - Probar con diferentes archivos
   - Ajustar parámetros

2. **Mediano plazo:**
   - Integración con base de datos
   - Historial de conversiones
   - Guardado de configuraciones

3. **Largo plazo:**
   - Soporte para más formatos
   - Batch processing
   - API REST
   - Integración con almacenamiento en la nube

---

## 📞 Soporte

Para problemas:
1. Revisar esta documentación
2. Consultar `file_to_speech.py`
3. Verificar logs de Gradio
4. Revisar repositorio oficial de GPT-SoVITS

---

**Versión:** 1.0  
**Fecha:** 2026-09-14  
**Estado:** ✅ COMPLETADO Y FUNCIONAL  

**¡Lista para usar!** 🚀
