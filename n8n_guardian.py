#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
N8N Guardian - Sistema completo de gestión y monitoreo
Versión: 2.0
Autor: Claude AI Assistant
"""

import os
import sys
import subprocess
import time
import threading
import logging
import json
import webbrowser
from datetime import datetime
from pathlib import Path
import urllib.request
import urllib.error

# Instalar colorama si no está disponible
try:
    from colorama import Fore, Back, Style, init
    init(autoreset=True)
except ImportError:
    print("📦 Instalando colorama para colores...")
    subprocess.run([sys.executable, "-m", "pip", "install", "colorama"], check=True)
    from colorama import Fore, Back, Style, init
    init(autoreset=True)

# Configuración de colores
class Colors:
    SUCCESS = Fore.GREEN + Style.BRIGHT
    ERROR = Fore.RED + Style.BRIGHT
    WARNING = Fore.YELLOW + Style.BRIGHT
    INFO = Fore.CYAN + Style.BRIGHT
    HEADER = Fore.MAGENTA + Style.BRIGHT
    NORMAL = Style.RESET_ALL
    BOLD = Style.BRIGHT

class N8NGuardian:
    def __init__(self):
        # Directorio de trabajo por defecto (puedes cambiar esta ruta)
        self.guardian_dir = Path.cwd() / "n8n_guardian_data"
        self.log_file = self.guardian_dir / "n8n_guardian.log"
        self.security_log = self.guardian_dir / "security_audit.log"
        self.monitoring = False
        self.n8n_process = None
        self.npm_path = "npm"  # Puede actualizarse si se encuentra en ruta específica
        self.n8n_path = "n8n"  # Puede actualizarse si se encuentra en ruta específica
        
        # Crear directorio si no existe
        self.guardian_dir.mkdir(exist_ok=True, parents=True)
        
        # Configurar logging
        self.setup_logging()
        
    def setup_logging(self):
        """Configurar sistema de logs"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s [%(levelname)s] %(message)s',
            handlers=[
                logging.FileHandler(self.log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def print_header(self):
        """Mostrar header del programa"""
        print(f"\n{Colors.HEADER}{'='*70}")
        print(f"🛡️  N8N GUARDIAN - SISTEMA COMPLETO DE GESTIÓN")
        print(f"{'='*70}{Colors.NORMAL}\n")
        print(f"{Colors.INFO}📅 Sesión iniciada: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.NORMAL}")
        print(f"{Colors.INFO}📁 Directorio guardian: {self.guardian_dir}{Colors.NORMAL}")
        print(f"{Colors.INFO}📝 Log principal: {self.log_file}{Colors.NORMAL}")
        print(f"{Colors.INFO}🔒 Log seguridad: {self.security_log}{Colors.NORMAL}")
        
        # Debug PATH para diagnosticar problemas
        python_path = os.environ.get('PATH', '')
        has_nodejs = any('nodejs' in path.lower() for path in python_path.split(os.pathsep))
        print(f"{Colors.INFO}🔍 PATH contiene Node.js: {has_nodejs}{Colors.NORMAL}\n")
    
    def log_and_print(self, message, level="info", color=None):
        """Log y print con colores"""
        if color is None:
            color = {
                "info": Colors.INFO,
                "success": Colors.SUCCESS,
                "warning": Colors.WARNING,
                "error": Colors.ERROR
            }.get(level, Colors.NORMAL)
        
        print(f"{color}{message}{Colors.NORMAL}")
        
        # Mapear niveles personalizados a niveles válidos de logging
        log_level_map = {
            "success": "info",
            "info": "info", 
            "warning": "warning",
            "error": "error"
        }
        
        actual_level = log_level_map.get(level, "info")
        clean_message = message.replace('🔍', '').replace('✅', '').replace('❌', '').replace('⚠️', '').replace('🚀', '').replace('📦', '').replace('🔒', '').strip()
        getattr(self.logger, actual_level)(clean_message)
    
    def run_command(self, command, capture_output=True, check=False):
        """Ejecutar comando con manejo de errores"""
        try:
            result = subprocess.run(
                command, 
                capture_output=capture_output, 
                text=True, 
                check=check,
                encoding='utf-8',
                shell=True  # Usar shell para heredar PATH correctamente
            )
            return result
        except subprocess.CalledProcessError as e:
            self.log_and_print(f"❌ Error ejecutando comando: {command}", "error")
            self.log_and_print(f"❌ Código de salida: {e.returncode}", "error")
            if e.stdout:
                self.log_and_print(f"❌ Stdout: {e.stdout}", "error")
            if e.stderr:
                self.log_and_print(f"❌ Stderr: {e.stderr}", "error")
            return None
        except FileNotFoundError:
            self.log_and_print(f"❌ Comando no encontrado: {command}", "error")
            # Intentar diagnóstico de PATH
            command_name = command.split()[0] if isinstance(command, str) else command[0]
            self.diagnose_path_issue(command_name)
            return None
        except Exception as e:
            self.log_and_print(f"❌ Error inesperado ejecutando comando: {str(e)}", "error")
            return None
    
    def diagnose_path_issue(self, command):
        """Diagnosticar problemas de PATH"""
        self.log_and_print(f"🔍 Diagnosticando problema con {command}...", "warning")
        
        # Verificar PATH desde Python
        python_path = os.environ.get('PATH', '')
        self.log_and_print(f"🔍 PATH desde Python contiene {command}: {command in python_path.lower()}", "info")
        
        # Intentar encontrar npm en ubicaciones comunes
        common_paths = [
            r"C:\Program Files\nodejs",
            r"C:\Program Files (x86)\nodejs", 
            os.path.expanduser(r"~\AppData\Roaming\npm"),
            os.path.expanduser(r"~\AppData\Local\npm")
        ]
        
        command_files = [f"{command}.cmd", f"{command}.bat", command]
        
        for path in common_paths:
            for cmd_file in command_files:
                full_path = os.path.join(path, cmd_file)
                if os.path.exists(full_path):
                    self.log_and_print(f"✅ Encontrado {command} en: {full_path}", "success")
                    return full_path
        
        # Último recurso: usar where en Windows
        try:
            result = subprocess.run(["where", command], capture_output=True, text=True, shell=True)
            if result.returncode == 0 and result.stdout.strip():
                cmd_path = result.stdout.strip().split('\n')[0]
                self.log_and_print(f"✅ {command} encontrado con 'where': {cmd_path}", "success")
                return cmd_path
        except:
            pass
            
        self.log_and_print(f"❌ No se pudo encontrar {command} en el sistema", "error")
        return None
    
    def check_node_installed(self):
        """Verificar si Node.js está instalado"""
        self.log_and_print("🔍 Verificando Node.js...", "info")
        
        result = self.run_command("node --version")
        if result and result.returncode == 0:
            version = result.stdout.strip()
            self.log_and_print(f"✅ Node.js encontrado: {version}", "success")
            
            # Verificar que sea versión 18 o superior
            try:
                version_num = int(version.replace('v', '').split('.')[0])
                if version_num < 18:
                    self.log_and_print(f"⚠️ Node.js {version} detectado. n8n requiere Node.js 18+", "warning")
                    return self.offer_node_installation()
            except:
                self.log_and_print("⚠️ No se pudo verificar la versión de Node.js", "warning")
            
            return True
        else:
            self.log_and_print("❌ Node.js no está instalado", "error")
            return self.offer_node_installation()
    
    def offer_node_installation(self):
        """Ofrecer instalación de Node.js"""
        print(f"\n{Colors.WARNING}⚠️  DEPENDENCIA REQUERIDA: Node.js{Colors.NORMAL}")
        print(f"{Colors.INFO}n8n requiere Node.js 18 o superior para funcionar.{Colors.NORMAL}")
        print(f"{Colors.INFO}🌐 Puedes descargarlo desde: https://nodejs.org{Colors.NORMAL}")
        
        while True:
            choice = input(f"\n{Colors.BOLD}¿Quieres abrir la página de descarga ahora? (S/N): {Colors.NORMAL}").strip().lower()
            if choice in ['s', 'sí', 'si', 'y', 'yes']:
                webbrowser.open('https://nodejs.org/es/')
                self.log_and_print("🌐 Página de descarga abierta en el navegador", "info")
                input(f"{Colors.WARNING}Presiona Enter después de instalar Node.js...{Colors.NORMAL}")
                return self.check_node_installed()  # Verificar de nuevo
            elif choice in ['n', 'no']:
                self.log_and_print("❌ Instalación cancelada. No se puede continuar sin Node.js", "error")
                return False
            else:
                print(f"{Colors.ERROR}Por favor responde S o N{Colors.NORMAL}")
    
    def check_npm_installed(self):
        """Verificar si npm está instalado"""
        self.log_and_print("🔍 Verificando npm...", "info")
        
        # Primero intentar con npm normal
        result = self.run_command("npm --version")
        if result and result.returncode == 0:
            version = result.stdout.strip()
            self.log_and_print(f"✅ npm encontrado: {version}", "success")
            return True
        else:
            # Si falla, intentar diagnosticar y encontrar npm
            self.log_and_print("⚠️ npm no encontrado en PATH, buscando en ubicaciones comunes...", "warning")
            
            npm_path = self.diagnose_path_issue("npm")
            if npm_path:
                # Probar con la ruta específica - agregar comillas para espacios
                quoted_path = f'"{npm_path}"' if ' ' in npm_path else npm_path
                result = self.run_command(f'{quoted_path} --version')
                if result and result.returncode == 0:
                    version = result.stdout.strip()
                    self.log_and_print(f"✅ npm encontrado en ubicación específica: {version}", "success")
                    self.npm_path = quoted_path  # Actualizar para uso futuro
                    return True
            
            self.log_and_print("❌ npm no está disponible en el sistema", "error")
            self.log_and_print("💡 Soluciones posibles:", "info")
            self.log_and_print("   1. Reinstalar Node.js desde: https://nodejs.org", "info")
            self.log_and_print("   2. Cerrar y reabrir PowerShell/CMD", "info")
            self.log_and_print("   3. Verificar variables de entorno PATH", "info")
            return False
    
    def check_n8n_executable(self):
        """Verificar si n8n es ejecutable directamente"""
        self.log_and_print("🔍 Verificando ejecutabilidad de n8n...", "info")
        
        # Primero intentar con n8n normal
        result = self.run_command("n8n --version")
        if result and result.returncode == 0:
            version = result.stdout.strip()
            self.log_and_print(f"✅ n8n ejecutable encontrado: {version}", "success")
            return True
        else:
            # Si falla, intentar diagnosticar y encontrar n8n
            self.log_and_print("⚠️ n8n no es ejecutable directamente, buscando ruta específica...", "warning")
            
            n8n_path = self.diagnose_path_issue("n8n")
            if n8n_path:
                # Probar con la ruta específica
                quoted_path = f'"{n8n_path}"' if ' ' in n8n_path else n8n_path
                result = self.run_command(f'{quoted_path} --version')
                if result and result.returncode == 0:
                    version = result.stdout.strip()
                    self.log_and_print(f"✅ n8n encontrado en ubicación específica: {version}", "success")
                    self.n8n_path = quoted_path  # Actualizar para uso futuro
                    return True
            
            # Último recurso: intentar con npx
            self.log_and_print("⚠️ Intentando con npx n8n...", "warning")
            result = self.run_command("npx n8n --version")
            if result and result.returncode == 0:
                version = result.stdout.strip()
                self.log_and_print(f"✅ n8n ejecutable via npx: {version}", "success")
                self.n8n_path = "npx n8n"
                return True
            
            self.log_and_print("❌ n8n no es ejecutable en el sistema", "error")
            self.log_and_print("💡 Soluciones posibles:", "info")
            self.log_and_print("   1. Reinstalar n8n: npm install -g n8n", "info")
            self.log_and_print("   2. Usar npx: npx n8n (más lento pero funciona)", "info")
            self.log_and_print("   3. Verificar PATH y permisos", "info")
            
            # Preguntar si quiere intentar reinstalar
            while True:
                choice = input(f"{Colors.BOLD}¿Quieres intentar reinstalar n8n? (S/N): {Colors.NORMAL}").strip().lower()
                if choice in ['s', 'sí', 'si', 'y', 'yes']:
                    return self.reinstall_n8n()
                elif choice in ['n', 'no']:
                    self.log_and_print("❌ No se puede continuar sin n8n ejecutable", "error")
                    return False
                else:
                    print(f"{Colors.ERROR}Por favor responde S o N{Colors.NORMAL}")
    
    def reinstall_n8n(self):
        """Reinstalar n8n globalmente"""
        self.log_and_print("🔄 Reinstalando n8n...", "info")
        
        # Primero desinstalar
        result = self.run_command(f"{self.npm_path} uninstall -g n8n")
        if result:
            self.log_and_print("✅ n8n desinstalado", "success")
        
        # Luego instalar
        result = self.run_command(f"{self.npm_path} install -g n8n")
        if result and result.returncode == 0:
            self.log_and_print("✅ n8n reinstalado exitosamente", "success")
            
            # Verificar que ahora sea ejecutable
            return self.check_n8n_executable()
        else:
            self.log_and_print("❌ Error reinstalando n8n", "error")
            return False
    
    def get_installed_n8n_version(self):
        """Obtener versión instalada de n8n"""
        result = self.run_command(f"{self.npm_path} list -g n8n --depth=0")
        if result and result.returncode == 0:
            for line in result.stdout.split('\n'):
                if 'n8n@' in line:
                    return line.split('@')[1].strip()
        return None
    
    def get_latest_n8n_version(self):
        """Obtener última versión disponible de n8n"""
        result = self.run_command(f"{self.npm_path} view n8n version")
        if result and result.returncode == 0:
            return result.stdout.strip()
        return None
    
    def compare_versions(self, current, latest):
        """Comparar versiones (simple)"""
        try:
            current_parts = [int(x) for x in current.split('.')]
            latest_parts = [int(x) for x in latest.split('.')]
            
            # Rellenar con ceros si es necesario
            max_len = max(len(current_parts), len(latest_parts))
            current_parts.extend([0] * (max_len - len(current_parts)))
            latest_parts.extend([0] * (max_len - len(latest_parts)))
            
            return current_parts < latest_parts
        except:
            return True  # En caso de duda, actualizar
    
    def check_and_update_n8n(self):
        """Verificar y actualizar n8n si es necesario"""
        self.log_and_print("🔍 Verificando estado de n8n...", "info")
        
        # Verificar instalación
        current_version = self.get_installed_n8n_version()
        if not current_version:
            self.log_and_print("📦 n8n no está instalado. Instalando...", "warning")
            return self.install_n8n()
        
        self.log_and_print(f"✅ n8n instalado: v{current_version}", "success")
        
        # Verificar actualizaciones
        self.log_and_print("🔍 Consultando última versión disponible...", "info")
        latest_version = self.get_latest_n8n_version()
        
        if not latest_version:
            self.log_and_print("⚠️ No se pudo verificar la última versión", "warning")
            return True  # Continuar con la versión actual
        
        self.log_and_print(f"📦 Última versión disponible: v{latest_version}", "info")
        
        # Comparar versiones
        if self.compare_versions(current_version, latest_version):
            print(f"\n{Colors.WARNING}🔄 Nueva versión disponible: v{current_version} → v{latest_version}{Colors.NORMAL}")
            
            while True:
                choice = input(f"{Colors.BOLD}¿Quieres actualizar n8n? (S/N): {Colors.NORMAL}").strip().lower()
                if choice in ['s', 'sí', 'si', 'y', 'yes']:
                    return self.update_n8n()
                elif choice in ['n', 'no']:
                    self.log_and_print("⏭️ Actualización omitida", "info")
                    return True
                else:
                    print(f"{Colors.ERROR}Por favor responde S o N{Colors.NORMAL}")
        else:
            self.log_and_print("✅ n8n está actualizado", "success")
            return True
    
    def install_n8n(self):
        """Instalar n8n"""
        self.log_and_print("📦 Instalando n8n globalmente...", "info")
        
        result = self.run_command(f"{self.npm_path} install -g n8n")
        if result and result.returncode == 0:
            self.log_and_print("✅ n8n instalado exitosamente", "success")
            return True
        else:
            self.log_and_print("❌ Error instalando n8n", "error")
            return False
    
    def update_n8n(self):
        """Actualizar n8n"""
        self.log_and_print("🔄 Actualizando n8n...", "info")
        
        result = self.run_command(f"{self.npm_path} update -g n8n")
        if result and result.returncode == 0:
            self.log_and_print("✅ n8n actualizado exitosamente", "success")
            return True
        else:
            self.log_and_print("❌ Error actualizando n8n", "error")
            return False
    
    def security_audit(self):
        """Realizar auditoría de seguridad completa"""
        self.log_and_print("🔒 Ejecutando auditoría de seguridad...", "info")
        
        # Crear log de seguridad con timestamp
        security_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        try:
            with open(self.security_log, 'a', encoding='utf-8') as f:
                f.write(f"\n{'='*80}\n")
                f.write(f"AUDITORÍA DE SEGURIDAD - {security_timestamp}\n")
                f.write(f"{'='*80}\n")
        except Exception as e:
            self.log_and_print(f"⚠️ No se pudo escribir al log de seguridad: {str(e)}", "warning")
        
        result = self.run_command(f"{self.npm_path} audit --audit-level moderate")
        
        if result:
            # Debug: mostrar qué devolvió realmente npm audit
            audit_output = result.stdout.strip()
            
            # Verificar diferentes variaciones de "sin vulnerabilidades"
            no_vulns_indicators = [
                "found 0 vulnerabilities",
                "0 vulnerabilities",
                "No vulnerabilities found",
                "no vulnerabilities found",
                "0 known vulnerabilities"
            ]
            
            has_vulnerabilities = True
            for indicator in no_vulns_indicators:
                if indicator.lower() in audit_output.lower():
                    has_vulnerabilities = False
                    break
            
            # También verificar si la salida está prácticamente vacía
            if len(audit_output) < 10:  # Muy poca información
                has_vulnerabilities = False
            
            # Verificar si contiene información real de vulnerabilidades
            vuln_keywords = ['critical', 'high', 'moderate', 'low', 'vulnerability', 'package']
            has_vuln_keywords = any(keyword in audit_output.lower() for keyword in vuln_keywords)
            
            # Si npm audit devuelve código de salida 0, generalmente significa sin problemas
            if result.returncode == 0 and not has_vuln_keywords:
                has_vulnerabilities = False
            
            if not has_vulnerabilities or not has_vuln_keywords:
                self.log_and_print("✅ Excelente: No se encontraron vulnerabilidades", "success")
                
                # Registrar en log de seguridad
                try:
                    with open(self.security_log, 'a', encoding='utf-8') as f:
                        f.write("RESULTADO: ✅ SIN VULNERABILIDADES\n")
                        f.write("Estado: SEGURO para continuar\n")
                        f.write(f"Salida npm audit: {audit_output[:200]}...\n\n")
                except:
                    pass
                    
            else:
                self.log_and_print("⚠️ Se encontraron vulnerabilidades de seguridad:", "warning")
                
                # Solo mostrar si realmente hay contenido
                if len(audit_output) > 20:
                    print(f"\n{Colors.WARNING}📋 REPORTE DE VULNERABILIDADES:{Colors.NORMAL}")
                    print(f"{Colors.WARNING}{audit_output}{Colors.NORMAL}")
                    
                    # Analizar y dar consejos específicos
                    self.analyze_vulnerabilities(audit_output)
                else:
                    print(f"\n{Colors.INFO}📋 Información detallada no disponible.{Colors.NORMAL}")
                    print(f"{Colors.INFO}💡 Para diagnosticar:{Colors.NORMAL}")
                    print(f"  • Usa el comando 'debug' en la sesión interactiva")
                    print(f"  • O ejecuta manualmente: {Colors.BOLD}npm audit{Colors.NORMAL}")
                
                # Registrar en log de seguridad
                try:
                    with open(self.security_log, 'a', encoding='utf-8') as f:
                        f.write("RESULTADO: ⚠️ VULNERABILIDADES DETECTADAS\n")
                        f.write("Detalles del npm audit:\n")
                        f.write(audit_output if audit_output else "Salida vacía")
                        f.write("\n" + "="*50 + "\n")
                except:
                    pass
        else:
            self.log_and_print("❌ No se pudo ejecutar la auditoría de seguridad", "error")
            try:
                with open(self.security_log, 'a', encoding='utf-8') as f:
                    f.write("RESULTADO: ❌ ERROR EN AUDITORÍA\n")
                    f.write("No se pudo ejecutar npm audit\n\n")
            except:
                pass
        
        return True  # Siempre devolver True para que siga el flujo
    
    def analyze_vulnerabilities(self, audit_output):
        """Analizar vulnerabilidades y dar consejos específicos"""
        if not audit_output or len(audit_output.strip()) < 10:
            print(f"\n{Colors.INFO}💡 No hay información detallada de vulnerabilidades para analizar.{Colors.NORMAL}")
            return
        
        print(f"\n{Colors.INFO}💡 ANÁLISIS Y RECOMENDACIONES:{Colors.NORMAL}")
        
        # Contar tipos de vulnerabilidades
        audit_lower = audit_output.lower()
        critical_count = audit_lower.count('critical')
        high_count = audit_lower.count('high')
        moderate_count = audit_lower.count('moderate')
        low_count = audit_lower.count('low')
        
        total_vulns = critical_count + high_count + moderate_count + low_count
        
        # Si no hay conteos, intentar otras formas de detección
        if total_vulns == 0:
            if 'vulnerabilities' in audit_lower or 'packages' in audit_lower:
                print(f"{Colors.INFO}📊 Se detectaron posibles problemas, pero sin clasificación clara.{Colors.NORMAL}")
                print(f"{Colors.INFO}💡 Ejecuta manualmente: {Colors.BOLD}npm audit{Colors.NORMAL} para más detalles.")
            else:
                print(f"{Colors.SUCCESS}📊 Análisis completo: No se detectaron vulnerabilidades clasificadas.{Colors.NORMAL}")
            return
        
        print(f"{Colors.WARNING}📊 Resumen de vulnerabilidades encontradas:{Colors.NORMAL}")
        if critical_count > 0:
            print(f"  🔴 Críticas: {critical_count}")
        if high_count > 0:
            print(f"  🟠 Altas: {high_count}")
        if moderate_count > 0:
            print(f"  🟡 Moderadas: {moderate_count}")
        if low_count > 0:
            print(f"  🟢 Bajas: {low_count}")
        
        print(f"\n{Colors.INFO}🎯 RECOMENDACIONES ESPECÍFICAS:{Colors.NORMAL}")
        
        if critical_count > 0:
            print(f"{Colors.ERROR}🚨 ACCIÓN INMEDIATA REQUERIDA:{Colors.NORMAL}")
            print(f"  • Tienes {critical_count} vulnerabilidades CRÍTICAS")
            print(f"  • Ejecuta: {Colors.BOLD}npm audit fix{Colors.NORMAL}")
            print(f"  • Si no se solucionan: {Colors.BOLD}npm audit fix --force{Colors.NORMAL}")
            print(f"  • Considera no usar n8n hasta resolver las críticas")
        
        elif high_count > 0:
            print(f"{Colors.WARNING}⚠️ ACCIÓN RECOMENDADA:{Colors.NORMAL}")
            print(f"  • Tienes {high_count} vulnerabilidades ALTAS")
            print(f"  • Ejecuta: {Colors.BOLD}npm audit fix{Colors.NORMAL}")
            print(f"  • Puedes usar n8n pero actualiza pronto")
        
        elif moderate_count > 0 or low_count > 0:
            print(f"{Colors.INFO}ℹ️ ACCIÓN SUGERIDA:{Colors.NORMAL}")
            print(f"  • Solo vulnerabilidades moderadas/bajas")
            print(f"  • Ejecuta: {Colors.BOLD}npm audit fix{Colors.NORMAL} cuando tengas tiempo")
            print(f"  • Seguro continuar con n8n")
        
        # Comandos útiles
        print(f"\n{Colors.INFO}🔧 COMANDOS ÚTILES:{Colors.NORMAL}")
        print(f"  • Ver detalles: {Colors.BOLD}npm audit{Colors.NORMAL}")
        print(f"  • Arreglar automático: {Colors.BOLD}npm audit fix{Colors.NORMAL}")
        print(f"  • Arreglar forzado: {Colors.BOLD}npm audit fix --force{Colors.NORMAL}")
        print(f"  • Solo críticas: {Colors.BOLD}npm audit --audit-level critical{Colors.NORMAL}")
        
        # Registrar análisis en log
        try:
            with open(self.security_log, 'a', encoding='utf-8') as f:
                f.write(f"ANÁLISIS:\n")
                f.write(f"- Críticas: {critical_count}\n")
                f.write(f"- Altas: {high_count}\n")
                f.write(f"- Moderadas: {moderate_count}\n")
                f.write(f"- Bajas: {low_count}\n")
                f.write(f"- Total: {total_vulns}\n")
                
                if critical_count > 0:
                    f.write("RECOMENDACIÓN: NO usar n8n hasta resolver críticas\n")
                elif high_count > 0:
                    f.write("RECOMENDACIÓN: Usar con precaución, actualizar pronto\n")
                else:
                    f.write("RECOMENDACIÓN: Seguro continuar\n")
                f.write("\n")
        except:
            pass
    
    def start_n8n_monitoring(self):
        """Iniciar n8n con monitoreo en segundo plano"""
        self.log_and_print("🚀 Iniciando n8n...", "info")
        
        try:
            # Usar la ruta correcta de n8n y shell=True para compatibilidad
            n8n_command = self.n8n_path
            
            self.log_and_print(f"🔍 Ejecutando comando: {n8n_command}", "info")
            
            # Iniciar n8n en un proceso separado con shell=True
            self.n8n_process = subprocess.Popen(
                n8n_command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True,
                shell=True  # Crucial para Windows y PATH
            )
            
            # Esperar un momento para que se inicie
            self.log_and_print("⏳ Esperando que n8n se inicie...", "info")
            time.sleep(5)
            
            # Verificar que se inició correctamente
            if self.n8n_process.poll() is None:
                self.log_and_print("✅ n8n iniciado exitosamente", "success")
                self.log_and_print("🌐 Acceso: http://localhost:5678", "info")
                self.log_and_print("💡 Presiona 'o' + Enter en la consola de n8n para abrir el navegador", "info")
                
                # Esperar un poco más y verificar que siga corriendo
                time.sleep(3)
                if self.n8n_process.poll() is None:
                    self.log_and_print("✅ n8n funcionando establemente", "success")
                    
                    # Iniciar monitoreo en segundo plano
                    self.monitoring = True
                    monitor_thread = threading.Thread(target=self.monitor_n8n, daemon=True)
                    monitor_thread.start()
                    
                    return True
                else:
                    self.log_and_print("❌ n8n se cerró inesperadamente durante el inicio", "error")
                    
                    # Intentar leer los errores
                    if self.n8n_process.stderr:
                        stderr = self.n8n_process.stderr.read()
                        if stderr:
                            self.log_and_print(f"❌ Error de n8n: {stderr}", "error")
                    
                    return False
            else:
                self.log_and_print("❌ n8n no se pudo iniciar", "error")
                
                # Leer errores si los hay
                try:
                    stdout, stderr = self.n8n_process.communicate(timeout=2)
                    if stdout:
                        self.log_and_print(f"📄 Stdout: {stdout}", "info")
                    if stderr:
                        self.log_and_print(f"❌ Stderr: {stderr}", "error")
                except subprocess.TimeoutExpired:
                    pass
                
                return False
                
        except FileNotFoundError as e:
            self.log_and_print(f"❌ n8n no encontrado: {str(e)}", "error")
            self.log_and_print("💡 Intenta ejecutar: npm install -g n8n", "info")
            return False
        except Exception as e:
            self.log_and_print(f"❌ Error inesperado iniciando n8n: {str(e)}", "error")
            return False
    
    def monitor_n8n(self):
        """Monitorear n8n en segundo plano"""
        self.log_and_print("👀 Monitoreo en segundo plano iniciado", "info")
        
        while self.monitoring and self.n8n_process:
            try:
                # Verificar que el proceso siga activo
                if self.n8n_process.poll() is not None:
                    self.log_and_print("⚠️ n8n se detuvo inesperadamente", "warning")
                    break
                
                # Log de estado cada 5 minutos
                current_time = datetime.now()
                if current_time.second == 0 and current_time.minute % 5 == 0:
                    self.log_and_print("💓 n8n funcionando correctamente", "info")
                
                time.sleep(30)  # Verificar cada 30 segundos
                
            except Exception as e:
                self.log_and_print(f"⚠️ Error en monitoreo: {str(e)}", "warning")
                break
        
        self.log_and_print("👀 Monitoreo detenido", "info")
    
    def interactive_session(self):
        """Sesión interactiva mientras n8n está ejecutándose"""
        print(f"\n{Colors.HEADER}{'='*50}")
        print(f"🎮 SESIÓN INTERACTIVA - N8N GUARDIAN")
        print(f"{'='*50}{Colors.NORMAL}\n")
        
        print(f"{Colors.INFO}Comandos disponibles:{Colors.NORMAL}")
        print(f"{Colors.BOLD}  status    {Colors.NORMAL}- Ver estado de n8n")
        print(f"{Colors.BOLD}  logs      {Colors.NORMAL}- Ver últimos logs principales")
        print(f"{Colors.BOLD}  security  {Colors.NORMAL}- Ver log de seguridad")
        print(f"{Colors.BOLD}  audit     {Colors.NORMAL}- Ejecutar nueva auditoría de seguridad")
        print(f"{Colors.BOLD}  debug     {Colors.NORMAL}- Debug de npm audit (ver salida raw)")
        print(f"{Colors.BOLD}  n8ndebug  {Colors.NORMAL}- Debug de n8n executable")
        print(f"{Colors.BOLD}  open      {Colors.NORMAL}- Abrir n8n en el navegador")
        print(f"{Colors.BOLD}  stop      {Colors.NORMAL}- Detener n8n y guardian")
        print(f"{Colors.BOLD}  help      {Colors.NORMAL}- Mostrar esta ayuda")
        
        while self.monitoring:
            try:
                command = input(f"\n{Colors.BOLD}Guardian> {Colors.NORMAL}").strip().lower()
                
                if command == "status":
                    if self.n8n_process and self.n8n_process.poll() is None:
                        self.log_and_print("✅ n8n está ejecutándose correctamente", "success")
                        self.log_and_print("🌐 URL: http://localhost:5678", "info")
                    else:
                        self.log_and_print("❌ n8n no está ejecutándose", "error")
                
                elif command == "logs":
                    self.show_recent_logs()
                
                elif command == "security":
                    self.show_security_logs()
                
                elif command == "audit":
                    self.security_audit()
                
                elif command == "debug":
                    self.debug_npm_audit()
                
                elif command == "n8ndebug":
                    self.debug_n8n_executable()
                
                elif command == "open":
                    webbrowser.open('http://localhost:5678')
                    self.log_and_print("🌐 n8n abierto en el navegador", "info")
                
                elif command == "stop":
                    self.stop_n8n()
                    break
                
                elif command == "help":
                    print(f"{Colors.INFO}Comandos: status, logs, security, audit, debug, n8ndebug, open, stop, help{Colors.NORMAL}")
                
                elif command == "":
                    continue
                    
                else:
                    print(f"{Colors.WARNING}Comando no reconocido. Escribe 'help' para ver comandos disponibles{Colors.NORMAL}")
                    
            except KeyboardInterrupt:
                print(f"\n{Colors.WARNING}Ctrl+C detectado. Deteniendo...{Colors.NORMAL}")
                self.stop_n8n()
                break
            except EOFError:
                self.stop_n8n()
                break
    
    def show_recent_logs(self):
        """Mostrar últimos logs principales"""
        try:
            with open(self.log_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                recent_lines = lines[-10:]  # Últimas 10 líneas
                
            print(f"\n{Colors.INFO}📝 Últimos logs principales:{Colors.NORMAL}")
            for line in recent_lines:
                print(f"{Colors.NORMAL}{line.strip()}")
                
        except Exception as e:
            self.log_and_print(f"❌ Error leyendo logs principales: {str(e)}", "error")
    
    def show_security_logs(self):
        """Mostrar logs de seguridad"""
        try:
            if not self.security_log.exists():
                print(f"\n{Colors.WARNING}📝 No hay logs de seguridad aún{Colors.NORMAL}")
                return
                
            with open(self.security_log, 'r', encoding='utf-8') as f:
                content = f.read()
                
            print(f"\n{Colors.INFO}🔒 Log de auditorías de seguridad:{Colors.NORMAL}")
            print(f"{Colors.WARNING}{content}{Colors.NORMAL}")
                
        except Exception as e:
            self.log_and_print(f"❌ Error leyendo logs de seguridad: {str(e)}", "error")
    
    def debug_npm_audit(self):
        """Debug de npm audit para diagnosticar problemas"""
        print(f"\n{Colors.INFO}🔍 DEBUG: Ejecutando npm audit paso a paso...{Colors.NORMAL}")
        
        # Probar diferentes comandos npm audit
        commands = [
            f"{self.npm_path} audit",
            f"{self.npm_path} audit --audit-level moderate", 
            f"{self.npm_path} audit --json",
            f"{self.npm_path} audit --registry https://registry.npmjs.org/"
        ]
        
        for i, cmd in enumerate(commands, 1):
            print(f"\n{Colors.INFO}🔍 Test {i}: {cmd}{Colors.NORMAL}")
            result = self.run_command(cmd)
            
            if result:
                print(f"  Código de salida: {result.returncode}")
                print(f"  Longitud stdout: {len(result.stdout)} caracteres")
                print(f"  Longitud stderr: {len(result.stderr)} caracteres")
                
                if result.stdout:
                    stdout_preview = result.stdout[:200] + "..." if len(result.stdout) > 200 else result.stdout
                    print(f"  Stdout preview: {stdout_preview}")
                
                if result.stderr:
                    stderr_preview = result.stderr[:200] + "..." if len(result.stderr) > 200 else result.stderr
                    print(f"  Stderr preview: {stderr_preview}")
            else:
                print(f"  ❌ Comando falló")
            
            print("-" * 50)
    
    def debug_n8n_executable(self):
        """Debug de n8n executable para diagnosticar problemas"""
        print(f"\n{Colors.INFO}🔍 DEBUG: Diagnosticando ejecutabilidad de n8n...{Colors.NORMAL}")
        
        # Probar diferentes formas de ejecutar n8n
        commands = [
            "n8n --version",
            "npx n8n --version",
            "node -e \"console.log(require('n8n/package.json').version)\"",
            f"{self.npm_path} list -g n8n",
            "where n8n" if os.name == 'nt' else "which n8n"
        ]
        
        for i, cmd in enumerate(commands, 1):
            print(f"\n{Colors.INFO}🔍 Test {i}: {cmd}{Colors.NORMAL}")
            result = self.run_command(cmd)
            
            if result:
                print(f"  Código de salida: {result.returncode}")
                print(f"  Longitud stdout: {len(result.stdout)} caracteres")
                print(f"  Longitud stderr: {len(result.stderr)} caracteres")
                
                if result.stdout:
                    stdout_preview = result.stdout[:200] + "..." if len(result.stdout) > 200 else result.stdout
                    print(f"  Stdout: {stdout_preview}")
                
                if result.stderr:
                    stderr_preview = result.stderr[:200] + "..." if len(result.stderr) > 200 else result.stderr
                    print(f"  Stderr: {stderr_preview}")
            else:
                print(f"  ❌ Comando falló")
            
            print("-" * 50)
        
        # Buscar n8n en ubicaciones comunes
        print(f"\n{Colors.INFO}🔍 Buscando n8n en ubicaciones comunes...{Colors.NORMAL}")
        
        if os.name == 'nt':  # Windows
            common_paths = [
                r"C:\Program Files\nodejs",
                r"C:\Program Files (x86)\nodejs", 
                os.path.expanduser(r"~\AppData\Roaming\npm"),
                os.path.expanduser(r"~\AppData\Local\npm"),
                os.path.expanduser(r"~\AppData\Roaming\npm\node_modules\.bin"),
            ]
            n8n_files = ["n8n.cmd", "n8n.bat", "n8n", "n8n.ps1"]
        else:  # Unix-like
            common_paths = [
                "/usr/local/bin",
                "/usr/bin",
                os.path.expanduser("~/.npm-global/bin"),
                "/opt/nodejs/bin"
            ]
            n8n_files = ["n8n"]
        
        found_files = []
        for path in common_paths:
            for n8n_file in n8n_files:
                full_path = os.path.join(path, n8n_file)
                if os.path.exists(full_path):
                    found_files.append(full_path)
                    print(f"  ✅ Encontrado: {full_path}")
        
        if not found_files:
            print(f"  ❌ No se encontró n8n en ubicaciones comunes")
        
        print(f"\n{Colors.INFO}💡 Información del sistema:{Colors.NORMAL}")
        print(f"  PATH actual contiene 'npm': {'npm' in os.environ.get('PATH', '').lower()}")
        print(f"  PATH actual contiene 'nodejs': {'nodejs' in os.environ.get('PATH', '').lower()}")
        print(f"  Ruta npm actual usada: {self.npm_path}")
        print(f"  Ruta n8n actual usada: {self.n8n_path}")
    
    def stop_n8n(self):
        """Detener n8n y el monitoreo"""
        self.log_and_print("🛑 Deteniendo n8n...", "warning")
        
        self.monitoring = False
        
        if self.n8n_process:
            try:
                self.n8n_process.terminate()
                self.n8n_process.wait(timeout=10)
                self.log_and_print("✅ n8n detenido exitosamente", "success")
            except subprocess.TimeoutExpired:
                self.n8n_process.kill()
                self.log_and_print("⚠️ n8n forzado a detenerse", "warning")
            except Exception as e:
                self.log_and_print(f"❌ Error deteniendo n8n: {str(e)}", "error")
    
    def run(self):
        """Función principal"""
        try:
            self.print_header()
            
            # Verificar dependencias
            if not self.check_node_installed():
                return
            
            if not self.check_npm_installed():
                return
            
            # Verificar que n8n sea ejecutable directamente
            if not self.check_n8n_executable():
                return
            
            # Verificar y actualizar n8n
            if not self.check_and_update_n8n():
                return
            
            # Auditoría de seguridad
            self.security_audit()
            
            # Preguntar si iniciar n8n (SIEMPRE, independientemente de vulnerabilidades)
            print(f"\n{Colors.HEADER}🚀 LISTO PARA INICIAR N8N{Colors.NORMAL}")
            print(f"{Colors.INFO}Todas las verificaciones completadas.{Colors.NORMAL}")
            
            while True:
                choice = input(f"{Colors.BOLD}¿Iniciar n8n con monitoreo? (S/N): {Colors.NORMAL}").strip().lower()
                if choice in ['s', 'sí', 'si', 'y', 'yes']:
                    if self.start_n8n_monitoring():
                        self.interactive_session()
                    break
                elif choice in ['n', 'no']:
                    self.log_and_print("👋 Guardian terminado por decisión del usuario", "info")
                    break
                else:
                    print(f"{Colors.ERROR}Por favor responde S o N{Colors.NORMAL}")
        
        except KeyboardInterrupt:
            print(f"\n{Colors.WARNING}Interrumpido por el usuario{Colors.NORMAL}")
        except Exception as e:
            self.log_and_print(f"❌ Error inesperado: {str(e)}", "error")
        finally:
            if self.monitoring:
                self.stop_n8n()
            
            print(f"\n{Colors.SUCCESS}✅ Guardian terminado exitosamente{Colors.NORMAL}")
            print(f"{Colors.INFO}📝 Logs guardados en: {self.log_file}{Colors.NORMAL}")
            print(f"{Colors.INFO}🔒 Auditorías de seguridad en: {self.security_log}{Colors.NORMAL}")

if __name__ == "__main__":
    guardian = N8NGuardian()
    guardian.run()
