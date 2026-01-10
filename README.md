
---

# 📈 Stock Market Game

A stock market simulation game based on real market data, featuring an asynchronous matching engine, AI-driven bots, and real-time updates.

The system is built using an **event-driven architecture**, with a strong separation between API, market engine, and real-time communication.

---

## 🚀 Features

* Realistic stock market simulation
* BUY / SELL order system
* Independent market matching engine
* Real-time price & trade updates (WebSocket)
* AI bots trained on real market data

* Scalable, containerized architecture

---

## 🧱 Architecture Overview

```
Vue.js (Frontend)
   ↓ REST / WebSocket
Nginx
   ↓
Django (API + Admin)
   ↓
PostgreSQL
   ↑
Market Engine (separate container)
   ↓
Redis (Pub/Sub, Channels)
```

---

## 🛠 Tech Stack

**Backend**

* Django + Django REST Framework
* Django Channels (WebSocket)
* PostgreSQL
* Redis
* Celery + Celery Beat
* RabbitMQ

**Market Engine**

* Standalone Python service
* Database locking & transactions
* Event-driven execution

**Frontend**

* Vue.js
* WebSocket


---

## 🐳 Dockerized Setup

The entire system runs using **Docker Compose**.

Main services:

* Django API
* Market Engine
* PostgreSQL
* Redis
* RabbitMQ
* Nginx
* Prometheus / Grafana
* ELK

---

## ▶️ Running the project

```bash
docker-compose up --build
```

---
