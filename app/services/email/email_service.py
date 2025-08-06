import os
import smtplib
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from fastapi import HTTPException, status

# Cargar variables de entorno
load_dotenv()

class EmailService:
    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER")
        self.smtp_port = int(os.getenv("SMTP_PORT", 2525))
        self.smtp_username = os.getenv("SMTP_USERNAME")
        self.smtp_password = os.getenv("SMTP_PASSWORD")
        self.smtp_from_email = os.getenv("SMTP_FROM_EMAIL")
        self.smtp_from_name = os.getenv("SMTP_FROM_NAME")
        
        # Validar configuración
        if not all([self.smtp_server, self.smtp_username, self.smtp_password, self.smtp_from_email]):
            raise RuntimeError("Faltan variables de configuración para el servicio de correo electrónico")
    
    async def send_verification_code(self, to_email: str, verification_code: str):
        """
        Envía un código de verificación al correo electrónico del usuario
        """
        print(f"[DEBUG] Iniciando envío de correo a: {to_email}")
        print(f"[DEBUG] Usando servidor SMTP: {self.smtp_server}:{self.smtp_port}")
        
        try:
            # Crear el mensaje
            subject = "Código de verificación - FoodPlaza"
            
            # Obtener el año actual
            current_year = datetime.datetime.now().year
            
            # Plantilla HTML del correo
            # Usamos formato de cadena raw (r""") para evitar problemas con las llaves en CSS
            html_content = r"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <title>Código de Verificación</title>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background-color: #4CAF50; color: white; padding: 10px 20px; text-align: center; }}
                    .content {{ padding: 20px; background-color: #f9f9f9; }}
                    .code {{ 
                        display: inline-block; 
                        padding: 15px 25px; 
                        font-size: 24px; 
                        font-weight: bold; 
                        letter-spacing: 2px; 
                        background-color: #4CAF50; 
                        color: white; 
                        margin: 20px 0;
                        border-radius: 5px;
                    }}
                    .footer {{ 
                        margin-top: 30px; 
                        text-align: center; 
                        font-size: 12px; 
                        color: #777; 
                        border-top: 1px solid #eee;
                        padding-top: 20px;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>Restablecimiento de Contraseña</h1>
                    </div>
                    <div class="content">
                        <p>Hola,</p>
                        <p>Hemos recibido una solicitud para restablecer tu contraseña en FoodPlaza. Utiliza el siguiente código de verificación:</p>
                        
                        <div style="text-align: center;">
                            <div class="code">{verification_code}</div>
                        </div>
                        
                        <p>Este código es válido por 15 minutos. Si no has solicitado este cambio, puedes ignorar este mensaje.</p>
                        
                        <p>Gracias,<br>El equipo de FoodPlaza</p>
                    </div>
                    <div class="footer">
                        <p> {current_year} FoodPlaza. Todos los derechos reservados.</p>
                    </div>
                </div>
            </body>
            </html>
            """.format(
                verification_code=verification_code,
                current_year=current_year
            )
            
            # Versión de texto plano para clientes de correo que no soportan HTML
            text_content = """
            Restablecimiento de Contraseña - FoodPlaza
            
            Hola,
            
            Hemos recibido una solicitud para restablecer tu contraseña en FoodPlaza. 
            Utiliza el siguiente código de verificación:
            
            {verification_code}
            
            Este código es válido por 15 minutos. Si no has solicitado este cambio, 
            puedes ignorar este mensaje.
            
            Gracias,
            El equipo de FoodPlaza
            
            {current_year} FoodPlaza. Todos los derechos reservados.
            """.format(
                verification_code=verification_code,
                current_year=current_year
            )
            
            # Crear el mensaje
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = f"{self.smtp_from_name} <{self.smtp_from_email}>"
            msg['To'] = to_email
            
            # Adjuntar versiones HTML y de texto plano
            part1 = MIMEText(text_content, 'plain')
            part2 = MIMEText(html_content, 'html')
            
            msg.attach(part1)
            msg.attach(part2)
            
            print(f"[DEBUG] Estableciendo conexión con {self.smtp_server}:{self.smtp_port}")
            
            # Configurar el timeout de la conexión
            server = smtplib.SMTP(timeout=10)
            
            try:
                # Establecer modo debug para ver la comunicación SMTP
                server.set_debuglevel(1)
                
                # Conectar al servidor
                print(f"[DEBUG] Conectando a {self.smtp_server}:{self.smtp_port}")
                server.connect(self.smtp_server, self.smtp_port)
                
                # Iniciar TLS si es necesario (usualmente para el puerto 587)
                if self.smtp_port in [587]:
                    print("[DEBUG] Iniciando TLS...")
                    server.starttls()
                
                # Autenticación
                print("[DEBUG] Intentando autenticación...")
                print(f"[DEBUG] Usuario: {self.smtp_username}")
                print(f"[DEBUG] Longitud de la contraseña: {len(self.smtp_password) if self.smtp_password else 0} caracteres")
                
                # Intentar autenticación con diferentes métodos
                try:
                    # Primero intentamos con LOGIN que es más común
                    server.login(self.smtp_username, self.smtp_password)
                except smtplib.SMTPAuthenticationError as auth_error:
                    print(f"[ERROR] Error de autenticación: {str(auth_error)}")
                    print("[DEBUG] Verifica que las credenciales en el archivo .env sean correctas")
                    print("[DEBUG] Asegúrate de que las variables SMTP_USERNAME y SMTP_PASSWORD estén configuradas correctamente")
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Error de autenticación con el servidor de correo. Verifica las credenciales configuradas."
                    )
                
                # Enviar correo
                print(f"[DEBUG] Enviando mensaje a {to_email}")
                server.send_message(msg)
                
                print(f"[DEBUG] Correo enviado exitosamente a {to_email}")
                return True
                
            except smtplib.SMTPException as e:
                error_msg = str(e)
                print(f"[ERROR] Error SMTP: {error_msg}")
                
                # Proporcionar mensajes más descriptivos basados en el error
                if "Invalid credentials" in error_msg or "535" in error_msg:
                    detail = "Credenciales de correo electrónico inválidas. Verifica el usuario y contraseña SMTP."
                elif "Connection unexpectedly closed" in error_msg:
                    detail = "El servidor SMTP cerró la conexión inesperadamente. Verifica la configuración del puerto y si el servidor está disponible."
                else:
                    detail = f"Error al conectar con el servidor de correo: {error_msg}"
                
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=detail
                )
                
            except Exception as e:
                error_msg = str(e)
                print(f"[ERROR] Error inesperado: {error_msg}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Error inesperado al enviar el correo: {error_msg}"
                )
                
            finally:
                try:
                    print("[DEBUG] Cerrando conexión SMTP...")
                    server.quit()
                except Exception as e:
                    print(f"[ADVERTENCIA] Error al cerrar la conexión SMTP: {str(e)}")
                    
        except Exception as e:
            print(f"[ERROR] Error general en send_verification_code: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al enviar el correo de verificación: {str(e)}"
            )

# Instancia global del servicio de correo
email_service = EmailService()
