<p align="center">
  <img src="./docs/assets/logo.png" width="220" alt="Agente FarmaQIA Logo" />
</p>

<p align="center">
  <a href="https://fastapi.tiangolo.com/" target="_blank">
    <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/fastapi/fastapi-original.svg" width="42" alt="FastAPI" />
  </a>
  &nbsp;&nbsp;
  <a href="https://www.python.org/" target="_blank">
    <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" width="42" alt="Python" />
  </a>
  &nbsp;&nbsp;
  <a href="https://openrouter.ai/" target="_blank">
    <img src="https://openrouter.ai/favicon.ico" width="42" alt="OpenRouter" />
  </a>
  &nbsp;&nbsp;
  <a href="https://www.docker.com/" target="_blank">
    <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/docker/docker-original.svg" width="42" alt="Docker" />
  </a>
</p>

<p align="center">
  <strong>Asistente Inteligente para Farmacias</strong><br/>
  Microservicio de Inteligencia Artificial para FarmaQ IA construido con FastAPI · Python · OpenRouter
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-3776AB?style=flat&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/FastAPI-0.115-009688?style=flat&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/Pydantic-v2-E92063?style=flat" />
  <img src="https://img.shields.io/badge/OpenRouter-AI-black?style=flat" />
  <img src="https://img.shields.io/badge/OpenAI%20SDK-Compatible-412991?style=flat" />
  <img src="https://img.shields.io/badge/Docker-ready-2496ED?style=flat&logo=docker&logoColor=white" />
  <img src="https://img.shields.io/badge/license-UNLICENSED-red?style=flat" />
</p>

---

# 💊 ¿Qué es Agente_FarmaQIA?

**Agente_FarmaQIA** es el microservicio de Inteligencia Artificial del ecosistema **FarmaQ IA**.

Su objetivo es convertirse en el asistente virtual oficial de la farmacia, permitiendo que los clientes interactúen mediante **WhatsApp**, reciban orientación farmacéutica segura, consulten productos disponibles y, posteriormente, generen pedidos que serán atendidos desde el Punto de Venta del ERP.

Este proyecto sigue una filosofía de desarrollo incremental:

> **Primero un asistente funcional. Después un asistente inteligente.**

---

# 🚀 Objetivos del MVP

La primera versión tendrá únicamente las siguientes capacidades:

- Conversar mediante WhatsApp.
- Responder preguntas generales relacionadas con farmacia.
- Mantener conversaciones naturales utilizando IA.
- Integrarse con OpenRouter como proveedor de modelos.
- Preparar la arquitectura para futuras integraciones con el ERP.

Posteriormente se incorporarán:

- Consulta de productos.
- Consulta de precios.
- Consulta de stock.
- Consulta de promociones.
- Generación de pedidos.
- Integración con el Punto de Venta.

---

# 🏗 Arquitectura General

```text
Cliente

↓

WhatsApp

↓

Meta Cloud API

↓

Agente_FarmaQIA

↓

OpenRouter

↓

Modelo de IA

↓

Respuesta

↓

WhatsApp
```

Próximamente:

```text
Chat Service

↓

Tools

↓

ERP Client

↓

FarmaQ IA API (NestJS)

↓

PostgreSQL
```

---

# 📂 Estructura del Proyecto

```text
Agente_FarmaQIA/

├── app/
│   ├── api/
│   ├── config/
│   ├── providers/
│   ├── services/
│   ├── schemas/
│   ├── utils/
│   └── main.py
│
├── docs/
│
├── docker/
│
├── tests/
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

---

# 🛠 Stack Tecnológico

| Componente | Tecnología |
|------------|------------|
| Lenguaje | Python 3.12 |
| Framework | FastAPI |
| Validación | Pydantic v2 |
| Servidor | Uvicorn |
| Cliente HTTP | HTTPX |
| IA | OpenRouter |
| SDK | OpenAI Compatible |
| Contenedores | Docker |
| Integración | WhatsApp Business Cloud API |
| ERP | FarmaQ IA (NestJS) |

---

# 🧠 Filosofía de Arquitectura

El proyecto sigue una arquitectura simple y desacoplada.

Cada componente tiene una única responsabilidad.

```text
FastAPI

↓

Chat Service

↓

Prompt Service

↓

Provider

↓

OpenRouter

↓

Modelo
```

Cuando el MVP esté validado se agregarán las herramientas del ERP sin modificar la arquitectura principal.

---

# 📅 Roadmap

## ✅ Fase 0

- Proyecto base
- Docker
- FastAPI
- OpenRouter
- README
- Configuración inicial

---

## 🚧 Fase 1

- Integración con WhatsApp Business
- Webhooks
- Conversación básica
- MVP funcional

---

## 🔜 Fase 2

- Personalidad del asistente
- Prompt profesional
- Contexto farmacéutico
- Restricciones médicas

---

## 🔜 Fase 3

Integración con FarmaQ IA.

- Buscar productos
- Buscar stock
- Buscar precios
- Promociones
- Sucursales

---

## 🔜 Fase 4

Pedidos.

- Crear pedido
- Consultar pedido
- Modificar pedido
- Cancelar pedido

---

## 🔮 Futuro

- Memoria conversacional
- Redis
- OCR de recetas
- Embeddings
- RAG
- Base vectorial
- Dashboard
- Observabilidad
- Agentes especializados

---

# 🚀 Inicio Rápido

## Requisitos

- Python 3.12+
- Docker
- Git
- Cuenta en OpenRouter
- Cuenta en Meta Developers (WhatsApp Business)

---

## Clonar

```bash
git clone https://github.com/BrayamHC/Agente-FarmaQIA.git

cd Agente-FarmaQIA
```

---

## Variables de entorno

```bash
cp .env.example .env
```

Configurar:

- OPENROUTER_API_KEY
- OPENROUTER_MODEL
- META_ACCESS_TOKEN
- META_VERIFY_TOKEN
- META_PHONE_NUMBER_ID

---

## Docker

```bash
docker compose up --build
```

---

## Ejecutar localmente

```bash
python -m venv .venv

source .venv/bin/activate
```

Windows

```powershell
.venv\Scripts\activate
```

Instalar dependencias

```bash
pip install -r requirements.txt
```

Ejecutar

```bash
uvicorn app.main:app --reload
```

---

# 🤝 Ecosistema FarmaQ IA

Este proyecto forma parte del ecosistema **FarmaQ IA**.

| Proyecto | Descripción |
|----------|-------------|
| FarmaQ IA ERP | Gestión de farmacia |
| Agente_FarmaQIA | Asistente Inteligente |
| Punto de Venta | Ventas y Cobro |
| Inventario | Control de Stock |

---

# 👨‍💻 Autor

**Brayam Herrera Cruz**

Ingeniero en Tecnologías de la Información

Proyecto desarrollado como parte del ecosistema **FarmaQ IA**, una plataforma orientada a la digitalización y automatización inteligente de farmacias mediante Inteligencia Artificial.