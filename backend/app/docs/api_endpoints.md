# CTech API — Documentación de Endpoints

> **Base URL:** `http://localhost:8000/api/v1`
> **Documentación interactiva:** `http://localhost:8000/docs`
> **Versión:** 1.0.0

---

## Convenciones

| Símbolo | Significado |
|---|---|
| 🔓 | Endpoint público — no requiere token |
| 🔐 | Endpoint protegido — requiere `Authorization: Bearer <token>` |
| 👑 | Solo accesible por rol `admin` |

---

## 🔑 Auth — `/api/v1/auth`

| Método | Ruta | Acceso | Descripción |
|---|---|---|---|
| `POST` | `/auth/register` | 🔓 | Registra un nuevo usuario. Valida nombre (solo letras), email único, existencia de comunidad y código de invitación |
| `POST` | `/auth/login` | 🔓 | Autentica al usuario. Retorna JWT con `access_token`, `token_type` y datos del usuario (`id`, `email`, `role`, `name`) |
| `POST` | `/auth/logout` | 🔐 | Invalida el token actual (añade a `token_blocklist`) |
| `POST` | `/auth/reset-password` | 🔓 | Actualiza la contraseña del usuario mediante token de recuperación |

### Registro — Body `POST /auth/register`
```json
{
  "name_user": "string (solo letras y espacios)",
  "email": "string (único en BD)",
  "password": "string",
  "community_id": "integer",
  "invite_code": "string (debe coincidir con community.code)",
  "rol_id": "integer (opcional, default: 4 = user)"
}
```

### Login — Body `POST /auth/login`
```json
{
  "email": "string",
  "password": "string"
}
```

### Login — Response exitoso
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "usuario@example.com",
    "role": "admin | mentor | leader | user",
    "name": "Nombre del usuario"
  }
}
```

### Mapeo de Roles en el Token
| `rol_id` en BD | Nombre en token |
|---|---|
| 1 | `admin` |
| 2 | `mentor` |
| 3 | `leader` |
| 4 | `user` |

---

## 🏘️ Communities — `/api/v1/communities`

| Método | Ruta | Acceso | Descripción |
|---|---|---|---|
| `GET` | `/communities/` | 🔓 | Lista todas las comunidades |
| `POST` | `/communities/` | 🔓* | Crea una nueva comunidad |
| `PATCH` | `/communities/{id}` | 🔓* | Actualización parcial de una comunidad |
| `DELETE` | `/communities/{id}` | 🔓* | Elimina una comunidad |

> *El guard de autenticación está preparado en el código pero comentado temporalmente durante desarrollo.

---

## 📅 Events — `/api/v1/events`

| Método | Ruta | Acceso | Descripción |
|---|---|---|---|
| `GET` | `/events/` | 🔓 | Lista todos los eventos (públicos y privados, filtrado a nivel de lógica) |
| `POST` | `/events/` | 🔐 | Crea un nuevo evento |
| `POST` | `/events/upload` | 🔐 | Sube imagen del evento a Cloudinary. Retorna URL pública |

### Crear Evento — Body `POST /events/`
```json
{
  "title": "string",
  "description": "string",
  "event_date": "datetime",
  "location": "string",
  "image_url": "string (URL Cloudinary)"
}
```

---

## 📚 Courses — `/api/v1/courses`

| Método | Ruta | Acceso | Descripción |
|---|---|---|---|
| `GET` | `/courses/` | 🔓 | Lista todos los cursos (vista pública: solo fichas de cursos públicos) |
| `POST` | `/courses/` | 🔐 | Crea un nuevo curso |
| `GET` | `/courses/{id}` | 🔐 | Obtiene detalle completo de un curso |
| `PUT` | `/courses/{id}` | 🔐 | Actualización completa de un curso |
| `DELETE` | `/courses/{id}` | 🔐 | Elimina un curso |

### Crear / Actualizar Curso — Body
```json
{
  "title": "string",
  "description": "string",
  "is_premium": false,
  "technologies": ["React", "TypeScript"],
  "content_links": {
    "pdfs": [],
    "books": [],
    "videos": []
  },
  "thumbnail_url": "string",
  "mentor_id": "integer",
  "community_id": "integer",
  "specialty_id": "integer"
}
```

---

## 🎓 Mentoring Sessions — `/api/v1/sessions`

| Método | Ruta | Acceso | Descripción |
|---|---|---|---|
| `POST` | `/sessions/` | 🔐 | Crea una sesión de mentoría. El `mentor_id` se toma automáticamente del token |
| `GET` | `/sessions/course/{course_id}` | 🔓 | Lista sesiones disponibles para un curso |
| `POST` | `/sessions/{id}/reserve` | 🔐 | Reserva una sesión disponible. El `student_id` se toma del token |
| `DELETE` | `/sessions/{id}/cancel` | 🔐 | Cancela una sesión reservada |

### Estados posibles de una sesión
| Estado | Descripción |
|---|---|
| `available` | Sesión disponible para ser reservada |
| `reserved` | Sesión ya reservada por un estudiante |
| `cancelled` | Sesión cancelada |

---

## 📊 Metrics — `/api/v1/metrics`

| Método | Ruta | Acceso | Descripción |
|---|---|---|---|
| `GET` | `/metrics/admin` | 🔐 | Retorna métricas del dashboard administrativo (totales de usuarios, comunidades, cursos, eventos) |

---

## 🛡️ Admin — `/api/v1/admin`

| Método | Ruta | Acceso | Descripción |
|---|---|---|---|
| `GET` | `/admin/` | 👑 | Verifica acceso al panel administrativo. Solo válido para rol `admin` |

---

## 🗂️ Specialties — `/api/v1/specialties`

> Endpoints para catalogar especialidades técnicas (Frontend, Backend, Data, etc.)

| Método | Ruta | Acceso | Descripción |
|---|---|---|---|
| `GET` | `/specialties/` | 🔓 | Lista todas las especialidades disponibles |
| `POST` | `/specialties/` | 🔐 | Crea una nueva especialidad |
| `PUT` | `/specialties/{id}` | 🔐 | Actualiza una especialidad |
| `DELETE` | `/specialties/{id}` | 🔐 | Elimina una especialidad |

---

## 💻 Technologies — `/api/v1/technologies`

> Catálogo de tecnologías que se asocian a cursos.

| Método | Ruta | Acceso | Descripción |
|---|---|---|---|
| `GET` | `/technologies/` | 🔓 | Lista todas las tecnologías |
| `POST` | `/technologies/` | 🔐 | Crea una nueva tecnología |
| `PUT` | `/technologies/{id}` | 🔐 | Actualiza una tecnología |
| `DELETE` | `/technologies/{id}` | 🔐 | Elimina una tecnología |

---

## 👤 Users — `/api/v1/users`

| Método | Ruta | Acceso | Descripción |
|---|---|---|---|
| `GET` | `/users/` | 🔐 | Lista todos los usuarios |
| `GET` | `/users/{id}` | 🔐 | Obtiene un usuario por ID |
| `PATCH` | `/users/{id}` | 🔐 | Actualización parcial del perfil de un usuario |
| `DELETE` | `/users/{id}` | 👑 | Elimina un usuario (solo admin) |

---

## 📄 Errores comunes

| Código | Significado |
|---|---|
| `400` | Datos inválidos (email duplicado, código incorrecto, nombre con caracteres no permitidos) |
| `401` | Contraseña incorrecta o token inválido |
| `403` | Acceso denegado por rol insuficiente |
| `404` | Recurso no encontrado (usuario, comunidad, curso, sesión) |
| `422` | Error de validación Pydantic (campo faltante o formato incorrecto) |
