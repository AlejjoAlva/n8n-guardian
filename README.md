# 🛡️ N8N Guardian

**Sistema completo de gestión y monitoreo para n8n con Node.js/npm**

[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![n8n Version](https://img.shields.io/badge/n8n-1.93+-purple.svg)](https://n8n.io)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)](https://github.com)

## 📋 Descripción

N8N Guardian es una herramienta avanzada diseñada para gestionar de forma segura y automatizada las instalaciones locales de **n8n** usando **Node.js y npm**. Proporciona verificación de dependencias, actualizaciones inteligentes, auditoría de seguridad en tiempo real y monitoreo continuo.

### ¿Qué es n8n?

[n8n](https://n8n.io) es una herramienta de automatización de flujos de trabajo de código abierto que permite crear integraciones complejas entre diferentes servicios y APIs sin necesidad de programación avanzada. Es una alternativa poderosa a servicios como Zapier o Microsoft Power Automate.

### ¿Por qué usar npm/Node.js en lugar de Docker?

Aunque Docker ofrece mayor aislamiento de seguridad, la instalación via **npm/Node.js** tiene ventajas específicas:

| Aspecto | npm/Node.js | Docker |
|---------|-------------|--------|
| **Rendimiento** | ⭐⭐⭐⭐⭐ Mayor velocidad | ⭐⭐⭐⭐ Buena velocidad |
| **Facilidad de uso** | ⭐⭐⭐⭐⭐ Instalación directa | ⭐⭐⭐ Curva de aprendizaje |
| **Integración del sistema** | ⭐⭐⭐⭐⭐ Acceso completo | ⭐⭐⭐ Limitado |
| **Recursos** | ⭐⭐⭐⭐⭐ Menor consumo RAM | ⭐⭐⭐ Mayor consumo |
| **Desarrollo/testing** | ⭐⭐⭐⭐⭐ Ideal para pruebas | ⭐⭐⭐ Más complejo |

**N8N Guardian** mitiga los riesgos de seguridad de npm mediante monitoreo activo, auditorías automáticas y mejores prácticas de gestión.

## ✨ Características principales

### 🔒 Seguridad avanzada
- **Auditoría automática** de vulnerabilidades npm
- **Análisis inteligente** de tipos de vulnerabilidades (críticas, altas, moderadas, bajas)
- **Recomendaciones específicas** de seguridad por contexto
- **Logs detallados** de todas las auditorías
- **Monitoreo en tiempo real** de comportamientos anómalos

### 🔄 Gestión automatizada
- **Verificación automática** de Node.js y npm
- **Actualización inteligente** (solo cuando es necesario)
- **Instalación automática** de dependencias faltantes
- **Comparación de versiones** avanzada
- **Reinstalación automática** si se detectan problemas

### 👀 Monitoreo en tiempo real
- **Monitoreo en segundo plano** mientras n8n está ejecutándose
- **Detección de paradas** inesperadas
- **Monitoreo de recursos** (memoria, CPU)
- **Verificación de conectividad** de puertos
- **Alertas automáticas** de problemas

### 🎮 Interfaz interactiva
- **Sesión interactiva** con comandos en tiempo real
- **Debug avanzado** para diagnóstico de problemas
- **Logs categorizados** (principal y seguridad)
- **Comandos útiles** integrados
- **Colores dinámicos** para mejor UX

## 🚀 Instalación

### Prerrequisitos

1. **Python 3.7+** - [Descargar aquí](https://python.org/downloads/)
2. **Node.js 18+** - [Descargar aquí](https://nodejs.org/) (incluye npm)

### Instalación rápida

```bash
# 1. Clonar el repositorio
git clone https://github.com/AlejjoAlva/n8n-guardian.git
cd n8n-guardian

# 2. El script instalará automáticamente las dependencias Python necesarias
python n8n_guardian.py
```

### Instalación manual de dependencias Python

```bash
pip install -r requirements.txt
```

## 📖 Uso

### Uso básico

```bash
python n8n_guardian.py
```

El guardian ejecutará automáticamente:

1. ✅ **Verificación** de Node.js y npm
2. ✅ **Instalación/actualización** de n8n (si es necesario)
3. ✅ **Auditoría de seguridad** completa
4. ✅ **Inicio de n8n** con monitoreo
5. ✅ **Sesión interactiva** para gestión

### Comandos interactivos

Una vez que n8n está ejecutándose, puedes usar estos comandos:

| Comando | Descripción |
|---------|-------------|
| `status` | Ver estado actual de n8n |
| `logs` | Mostrar últimos logs principales |
| `security` | Ver historial de auditorías de seguridad |
| `audit` | Ejecutar nueva auditoría de seguridad |
| `debug` | Debug de npm audit (salida raw) |
| `n8ndebug` | Debug de ejecutabilidad de n8n |
| `open` | Abrir n8n en el navegador |
| `stop` | Detener n8n y guardian |
| `help` | Mostrar ayuda de comandos |

### Ejemplo de sesión

```
🛡️ N8N GUARDIAN - SISTEMA COMPLETO DE GESTIÓN
📅 Sesión iniciada: 2025-05-24 12:00:00
✅ Node.js encontrado: v22.14.0
✅ npm encontrado: 10.9.2
✅ n8n instalado: v1.93.0
✅ n8n está actualizado
✅ No se encontraron vulnerabilidades
🚀 n8n iniciado exitosamente
🌐 Acceso: http://localhost:5678

Guardian> status
✅ n8n está ejecutándose correctamente
🌐 URL: http://localhost:5678

Guardian> audit
🔒 Ejecutando nueva auditoría de seguridad...
✅ No se encontraron vulnerabilidades
```

## 🔧 Configuración

### Rutas configurables

El guardian usa por defecto las siguientes rutas:

```python
# Directorio principal
./n8n_guardian_data/

# Logs
n8n_guardian.log          # Log principal
security_audit.log        # Log de auditorías de seguridad
```

### Personalización

Puedes modificar las rutas editando estas líneas en el código:

```python
self.guardian_dir = Path.cwd() / "n8n_guardian_data"
```

## 🛡️ Consideraciones de seguridad

### Riesgos de npm/Node.js

La instalación de n8n via npm conlleva algunos riesgos inherentes:

- **Acceso completo al sistema** de archivos
- **Ejecución de código** de terceros (dependencias)
- **Vulnerabilidades** en paquetes npm
- **Permisos elevados** del usuario

### Mitigaciones implementadas

N8N Guardian mitiga estos riesgos mediante:

1. **Auditoría continua** de vulnerabilidades
2. **Monitoreo de comportamiento** anómalo
3. **Logs detallados** de todas las actividades
4. **Verificación de integridad** de paquetes
5. **Recomendaciones específicas** de seguridad

### Mejores prácticas recomendadas

- ✅ **No ejecutar workflows** de fuentes no confiables
- ✅ **Revisar código** antes de importar workflows
- ✅ **Mantener n8n actualizado** siempre
- ✅ **Ejecutar auditorías** regularmente
- ✅ **Usar cuentas** con permisos limitados cuando sea posible

## 📊 Análisis de vulnerabilidades

El guardian proporciona análisis inteligente de vulnerabilidades:

### Tipos de vulnerabilidades

| Tipo | Acción recomendada | Impacto |
|------|-------------------|--------|
| **🔴 Críticas** | No usar n8n hasta resolver | Alto riesgo |
| **🟠 Altas** | Usar con precaución, actualizar pronto | Riesgo moderado |
| **🟡 Moderadas** | Actualizar cuando sea conveniente | Riesgo bajo |
| **🟢 Bajas** | Actualizar en mantenimiento rutinario | Riesgo mínimo |

### Comandos de remediación

```bash
# Ver detalles de vulnerabilidades
npm audit

# Arreglar automáticamente
npm audit fix

# Arreglar forzadamente (con cuidado)
npm audit fix --force

# Solo vulnerabilidades críticas
npm audit --audit-level critical
```

## 🔍 Diagnóstico y solución de problemas

### Problemas comunes

#### n8n no se encuentra
```bash
# Verificar instalación
npm list -g n8n

# Reinstalar si es necesario
npm install -g n8n
```

#### npm no encontrado
```bash
# Verificar Node.js
node --version

# Reinstalar Node.js si es necesario
# Descargar desde: https://nodejs.org
```

#### Problemas de PATH
```bash
# Verificar PATH (Windows)
echo %PATH%

# Buscar npm manualmente
where npm
where n8n
```

### Debug avanzado

El guardian incluye herramientas de debug integradas:

```bash
Guardian> debug        # Debug de npm audit
Guardian> n8ndebug     # Debug de n8n executable
Guardian> logs         # Ver logs principales
Guardian> security     # Ver logs de seguridad
```

## 📁 Estructura del proyecto

```
n8n-guardian/
├── n8n_guardian.py           # Script principal
├── README.md                 # Esta documentación
├── LICENSE                   # Licencia MIT
├── requirements.txt          # Dependencias Python
├── .gitignore               # Archivos a ignorar
└── n8n_guardian_data/       # Directorio de logs (generado automáticamente)
    ├── n8n_guardian.log      # Log principal
    └── security_audit.log    # Auditorías de seguridad
```

## 🤝 Contribuir

Las contribuciones son bienvenidas. Para contribuir:

1. **Fork** el proyecto
2. **Crea** una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. **Push** a la rama (`git push origin feature/AmazingFeature`)
5. **Abre** un Pull Request

### Áreas de mejora

- [ ] Soporte mejorado para Linux/macOS
- [ ] Interfaz gráfica (GUI)
- [ ] Integración con Docker como opción
- [ ] Notificaciones de escritorio
- [ ] Backup automático de workflows
- [ ] Métricas de rendimiento avanzadas

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## ⚠️ Descargo de responsabilidad

Este software se proporciona "tal como está", sin garantías de ningún tipo. El uso de n8n y la gestión de dependencias npm conlleva riesgos inherentes de seguridad. Los usuarios son responsables de:

- Evaluar los riesgos de seguridad en su entorno específico
- Implementar medidas de seguridad adicionales según sea necesario
- Mantener copias de seguridad de datos importantes
- Revisar y aprobar la ejecución de workflows de terceros

## 🙏 Agradecimientos

- **[n8n.io](https://n8n.io)** - Por crear una herramienta de automatización increíble
- **[Node.js](https://nodejs.org)** - Por el runtime JavaScript
- **[npm](https://npmjs.com)** - Por el gestor de paquetes
- **[Python](https://python.org)** - Por el lenguaje de scripting
- **[Colorama](https://pypi.org/project/colorama/)** - Por los colores en consola

## 📞 Soporte

Si encuentras problemas o tienes preguntas:

1. **Revisa** la sección de solución de problemas
2. **Busca** en los issues existentes
3. **Crea** un nuevo issue con detalles completos
4. **Incluye** logs relevantes y pasos para reproducir

---

### 🌟 ¡Si este proyecto te resulta útil, considera darle una estrella!

**Desarrollado con ❤️ para la comunidad de n8n**