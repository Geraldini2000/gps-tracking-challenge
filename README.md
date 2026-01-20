# 🚗 GPS Tracking System

Sistema de rastreamento GPS com autenticação JWT, processamento de pacotes hexadecimais e API REST.

**🌐 Aplicação em Produção:** (http://147.93.5.237:8000/api/docs/)

---

## 📋 Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Arquitetura](#arquitetura)
- [Como Funciona](#como-funciona)
- [Endpoints da API](#endpoints-da-api)
- [Instalação e Uso](#instalação-e-uso)
- [Melhorias Futuras](#melhorias-futuras)

---

## 🎯 Sobre o Projeto

Sistema completo para rastreamento de dispositivos GPS que:
- Recebe pacotes hexadecimais de dispositivos GPS via TCP ou HTTP
- Processa e decodifica os pacotes no formato SFT9001
- Armazena localizações em PostgreSQL
- Fornece API REST autenticada com JWT

---

## 🛠️ Tecnologias Utilizadas

### **Backend**
- **Python 3.12** - Linguagem principal
- **Django 5.2.7** - Framework web
- **Django REST Framework 3.16** - API REST
- **djangorestframework-simplejwt 5.5.1** - Autenticação JWT
- **drf-spectacular** - Documentação OpenAPI/Swagger
- **psycopg2-binary** - Driver PostgreSQL
- **python-dotenv** - Gestão de variáveis de ambiente

### **Banco de Dados**
- **PostgreSQL** - Armazenamento de localizações e usuários

### **DevOps**
- **Docker** - Containerização
- **Docker Compose** - Orquestração de serviços
- **GitHub Actions** - Pipeline CI (build e testes automatizados)

### **Testes**
- **pytest 9.0.2** - Framework de testes
- **pytest-asyncio 1.3.0** - Suporte para testes assíncronos

### **Protocolo GPS**
- **SFT9001** - Protocolo proprietário de dispositivos GPS
- Suporte a pacotes hexadecimais

---

## 🏗️ Arquitetura

### **Padrões Implementados**

**1. Hexagonal Architecture (Ports & Adapters)**
```
├── tcp_gateway/              # Núcleo da aplicação
│   ├── decoder/              # Decodificação hex → bytes
│   ├── parser/               # Parser do protocolo SFT9001
│   ├── handlers/             # Handlers por tipo de mensagem
│   ├── factory/              # Factory para criar handlers
│   ├── repositories/         # Interfaces e implementações
│   └── adapters/             # Adaptadores HTTP/TCP
```

**2. Repository Pattern**
- Interface abstrata para persistência
- Implementações: PostgreSQL e Fake (testes)
- Facilita troca de banco de dados

**3. Factory Pattern**
- `MessageHandlerFactory` cria handlers dinamicamente
- Suporta múltiplos tipos de mensagens GPS

**4. Strategy Pattern**
- Handlers específicos por tipo de pacote (Location, Ping, etc.)

**5. Domain-Driven Design (DDD)**
- Camada de **Domínio**: Entidades (UserDevice), Value Objects (Location), Services (DeviceAuthorizationService)
- Camada de **Aplicação**: Use Cases (RegisterDevice, GetUserDevices, GetDeviceLocation)
- Camada de **Infraestrutura**: Repositórios Django ORM
- Camada de **Interfaces**: Controllers e Serializers

### **Fluxo de Dados**

```
Dispositivo GPS
    ↓ (pacote hex via TCP/HTTP)
HttpInputAdapter
    ↓
HexDecoder (hex → bytes)
    ↓
SFT9001Parser (bytes → objeto)
    ↓
MessageHandlerFactory (tipo → handler)
    ↓
LocationHandler
    ↓
PostgresLocationRepository
    ↓
PostgreSQL Database
```

---

## ⚙️ Como Funciona

### **1. Autenticação JWT**

```python
# Registro simplificado - apenas username e password
POST /api/auth/register
{
  "username": "usuario",
  "password": "senha123"
}

# Login - recebe tokens JWT
POST /api/auth/login
{
  "username": "usuario",
  "password": "senha123"
}
# Retorna: { "access": "token...", "refresh": "token..." }
```

### **2. Simulação de Pacotes GPS**

```python
# Envia pacote hex e vincula dispositivo automaticamente ao usuário
POST /simulate
Authorization: Bearer {token}
{
  "payload": "50F70A3F73025EFCF950156F017D784000008CA0F8003C013026A1029E72BD73C4"
}
```

**O que acontece:**
1. Decodifica o hexadecimal
2. Extrai informações (device_id, lat, long, speed, etc.)
3. **Vincula automaticamente** o `device_id` ao usuário autenticado
4. Salva a localização no banco

### **3. Consulta de Localização**

```python
# Retorna última localização do dispositivo (apenas se for seu)
GET /api/v1/location/{device_id}
Authorization: Bearer {token}
```

**Segurança:** Verifica se o `device_id` pertence ao usuário antes de retornar dados.

---

## 📡 Endpoints da API

### **🔐 Autenticação**

| Método | Endpoint | Descrição | Auth |
|--------|----------|-----------|------|
| POST | `/api/auth/register` | Criar nova conta | ❌ |
| POST | `/api/auth/login` | Login e obter tokens JWT | ❌ |
| POST | `/api/auth/refresh` | Renovar access token | ❌ |

### **📱 Dispositivos**

| Método | Endpoint | Descrição | Auth |
|--------|----------|-----------|------|
| GET | `/api/devices` | Listar meus dispositivos | ✅ |

### **📍 Localização**

| Método | Endpoint | Descrição | Auth |
|--------|----------|-----------|------|
| GET | `/api/v1/location/{device_id}` | Última localização do dispositivo | ✅ |
| POST | `/simulate` | Simular pacote GPS (vincula device) | ✅ |

### **📚 Documentação**

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/docs/` | Documentação Swagger UI |
| GET | `/api/schema/` | Schema OpenAPI JSON |

**🔗 Acesse a documentação completa:** (http://147.93.5.237:8000/api/docs/)

---

## 📊 Exemplo de Uso Completo

### **Fluxo completo de uso da API:**

#### **1️⃣ Registrar um novo usuário**
```bash
curl -X POST http://147.93.5.237:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "meu_usuario",
    "password": "senha123"
  }'
```

**Resposta:**
```json
{
  "message": "Usuário criado com sucesso"
}
```

---

#### **2️⃣ Fazer login e obter o token de acesso**
```bash
curl -X POST http://147.93.5.237:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "meu_usuario",
    "password": "senha123"
  }'
```

**Resposta:**
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**⚠️ IMPORTANTE:** Copie o valor do campo `"access"` - você precisará dele para todas as próximas chamadas!

---

#### **3️⃣ Simular um pacote GPS (vincula device automaticamente)**

**Agora use o token obtido no passo anterior:**

```bash
curl -X POST http://147.93.5.237:8000/simulate \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "payload": "50F70A3F73025EFCF950156F017D784000008CA0F8003C013026A1029E72BD73C4"
  }'
```

**Resposta:**
```json
{
  "device_id": "ABC123",
  "timestamp": 1737379200,
  "latitude": -23.550520,
  "longitude": -46.633308,
  "speed_kmh": 60,
  "ignition_on": true,
  "gps_fixed": true,
  "gps_historical": false
}
```

**✅ O dispositivo foi automaticamente vinculado ao seu usuário!**

---

#### **4️⃣ Listar seus dispositivos vinculados**

```bash
curl -X GET http://147.93.5.237:8000/api/devices \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

**Resposta:**
```json
[
  {
    "id": 1,
    "device_id": "ABC123",
    "device_name": "Device ABC123"
  }
]
```

---

#### **5️⃣ Consultar última localização do dispositivo**

```bash
curl -X GET http://147.93.5.237:8000/api/v1/location/ABC123 \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

**Resposta:**
```json
{
  "device_id": "ABC123",
  "timestamp": 1737379200,
  "latitude": -23.550520,
  "longitude": -46.633308,
  "speed_kmh": 60,
  "ignition_on": true,
  "gps_fixed": true,
  "gps_historical": false
}
```

---

### **🔑 Sobre o Token de Acesso**

- O `access` token tem validade de **24 horas**
- Deve ser incluído no header `Authorization: Bearer {token}` em **todas as requisições protegidas**
- Se o token expirar, use o endpoint `/api/auth/refresh` com o `refresh` token para obter um novo `access` token
- Tokens são vinculados ao usuário - você só acessa dispositivos vinculados a você

---

### **🚫 O que acontece se tentar acessar sem token ou com token inválido?**

```bash
# Sem token
curl -X GET http://147.93.5.237:8000/api/devices
```

**Resposta:**
```json
{
  "detail": "Authentication credentials were not provided."
}
```

---

### **🔒 O que acontece se tentar acessar dispositivo de outro usuário?**

```bash
curl -X GET http://147.93.5.237:8000/api/v1/location/DEVICE_DE_OUTRO_USUARIO \
  -H "Authorization: Bearer {seu_token}"
```

**Resposta:**
```json
{
  "detail": "Você não tem permissão para acessar este dispositivo"
}
```

---

## 🎯 Melhorias Futuras

### **🏛️ Arquitetura**

#### **1. Separação de Responsabilidades**
- [ ] Separar Django API e TCP Gateway em serviços independentes
- [ ] Implementar Message Queue (RabbitMQ/Redis) para comunicação assíncrona
- [ ] Usar Event-Driven Architecture para desacoplar processamento

```
TCP Gateway → RabbitMQ → Workers → PostgreSQL
                  ↓
              Django API (leitura)
```
### **💻 Código**

#### **1. Testes**
- [ ] Implementar testes de carga (Locust/K6)

#### **2. Validações e Segurança**
- [ ] Rate limiting por usuário/IP
- [ ] Validação mais rigorosa de payloads hexadecimais
- [ ] Implementar HTTPS obrigatório
- [ ] Rotação automática de tokens JWT

#### **3. Performance**
- [ ] Paginação em listagens de dispositivos e localizações
- [ ] Índices otimizados no PostgreSQL
- [ ] Lazy loading e eager loading estratégico

#### **4. Features**
- [ ] Histórico completo de localizações (não apenas última)
- [ ] WebSocket para rastreamento em tempo real

### **📦 DevOps**

- [ ] Implementar CD (Continuous Deployment) no GitHub Actions para deploy automático
- [ ] Multi-stage Docker builds (reduzir tamanho da imagem)
- [ ] Kubernetes para orquestração em produção
- [ ] Backup automático do PostgreSQL
- [ ] Blue-Green deployment ou Canary releases
- [ ] Secrets management (Vault, AWS Secrets Manager)



🌐 **Servidor em Produção:** (http://147.93.5.237:8000/api/docs/)

