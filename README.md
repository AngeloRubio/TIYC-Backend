# 🤖 TIYC Backend - "Tú Inspiras, Yo Creo"

> Plataforma de generación de cuentos ilustrados con IA para profesores

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/flask-2.2.3-green.svg)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🎯 Descripción

TIYC es una API REST que permite a profesores generar cuentos ilustrados personalizados usando IA, con tres enfoques pedagógicos: **Montessori**, **Waldorf** y **Reggio Emilia**.

### Flujo Principal
1. **Profesor** ingresa contexto y selecciona enfoque pedagógico
2. **Gemini AI** genera cuento completo
3. **Gemini AI** extrae escenarios clave del cuento
4. **Stability AI** genera imágenes para cada escenario
5. **Profesor** puede regenerar imágenes y guardar en biblioteca



## 🚀 Instalación Rápida

### 1. Clonar el Repositorio
```bash
git clone https://github.com/tu-usuario/tiyc-backend.git
cd tiyc-backend
```

### 2. Configurar Entorno Virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
```

### 3. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar Variables de Entorno

# Editar .env con tus API keys


### 5. Configurar Base de Datos


### 6. Ejecutar la Aplicación
```bash
python app.py
```


### APIs Externas Utilizadas

- **Google Gemini 2.0-flash**: Generación de cuentos y extracción de escenarios
- **Stability AI**: Generación de imágenes con estilos pedagógicos  modelo es el core 2.0
- **MySQL**: Base de datos relacional

## 📚 Enfoques Pedagógicos

### 🔬 Montessori
- Escenas realistas y prácticas
- Materiales naturales
- Niños resolviendo problemas independientemente

### 🎨 Waldorf
- Estilo acuarela suave
- Elementos orgánicos y naturales
- Sensación etérea y onírica

### 📖 Reggio Emilia (Traditional)
- Colores brillantes y vividos
- Personajes expresivos
- Estilo de libro ilustrado clásico

## 📄 Licencia

MIT License. Ver [LICENSE](LICENSE) para más detalles.

## 👥 Equipo

Desarrollado para la **Unidad Educativa Santa Fe** como parte del proyecto de innovación educativa con IA con - Universidad de Guayaquil.

---

