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

## 🏗️ Arquitectura

```
📁 Clean Architecture - Separación por Capas
├── domain/          # Entidades, Interfaces, Excepciones
├── application/     # Servicios de Aplicación, DTOs
├── infrastructure/  # Implementaciones (DB, APIs externas)
└── presentation/    # Controllers, Middleware
```

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
```bash
cp .env.example .env
# Editar .env con tus API keys
```

### 5. Configurar Base de Datos
```bash
mysql -u root -p < db_setup.sql
```

### 6. Ejecutar la Aplicación
```bash
python app.py
```

## 🔧 Configuración

### Variables de Entorno Requeridas

```env
# APIs Externas
GEMINI_API_KEY=tu_gemini_api_key
STABILITY_API_KEY=tu_stability_api_key

# Base de Datos
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=tu_password
DB_NAME=santa_fe

# Seguridad
JWT_SECRET_KEY=tu_jwt_secret_super_seguro
```

### APIs Externas Utilizadas

- **Google Gemini 2.0-flash**: Generación de cuentos y extracción de escenarios
- **Stability AI**: Generación de imágenes con estilos pedagógicos
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

## 🛠️ API Endpoints

### Autenticación
```
POST /api/auth/login              # Login profesor
GET  /api/auth/profile            # Perfil usuario
```

### Cuentos
```
POST /api/generate-illustrated-story     # Genera y guarda completo
POST /api/preview-illustrated-story      # Preview sin guardar
POST /api/save-previewed-story           # Guarda preview en BD
GET  /api/illustrated-stories/:id        # Obtiene cuento completo
GET  /api/stories/teacher/:id            # Cuentos por profesor
```

### Imágenes
```
POST /api/regenerate-scenario-image/:id  # Regenera imagen específica
GET  /api/images/story/:id               # Imágenes por cuento
```

## 🧪 Testing

```bash
# Ejecutar tests
pytest

# Con cobertura
pytest --cov=application --cov=domain

# Tests específicos
pytest tests/test_story_service.py
```

## 📁 Estructura del Proyecto

```
story_illustration_api/
├── domain/                     # 🏛️ Capa de Dominio
│   ├── entities/              # Story, Scenario, Image, Teacher
│   ├── exceptions/            # Excepciones personalizadas
│   ├── interfaces/            # Contratos (repositories, services)
│   └── value_objects/         # Parámetros inmutables
├── application/               # 🔧 Capa de Aplicación
│   ├── dtos/                  # Request/Response DTOs
│   └── services/              # Story, Scenario, Image, Auth
├── infrastructure/            # 🔌 Capa de Infraestructura
│   ├── repositories/          # MySQL implementations
│   └── services/              # Gemini, Stability AI, JWT
├── presentation/              # 🌐 Capa de Presentación
│   ├── api/                   # Flask routes
│   └── middleware/            # Error handling, validation
├── static/images/             # 🖼️ Imágenes generadas
├── logs/                      # 📄 Logs de aplicación
├── requirements.txt           # 📦 Dependencias Python
├── app.py                     # 🚀 Punto de entrada
├── config.py                  # ⚙️ Configuración
└── db_setup.sql              # 🗄️ Schema de BD
```

## 🤝 Contribución

1. Fork del repositorio
2. Crear rama feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## 📄 Licencia

MIT License. Ver [LICENSE](LICENSE) para más detalles.

## 👥 Equipo

Desarrollado para la **Unidad Educativa Santa Fe** como parte del proyecto de innovación educativa con IA.

---

**¿Necesitas ayuda?** Abre un [issue](https://github.com/tu-usuario/tiyc-backend/issues) o contacta al equipo de desarrollo.
