"""
Serviço de envio de emails usando Resend.com
"""
import os
import random
from datetime import datetime, timedelta
from typing import Optional

# Configuração do Resend
RESEND_API_KEY = os.getenv("RESEND_API_KEY", "re_AYaBRPa8_3cw1yj3pb7XA2NMWKwqkqtFG")
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "pihemotec@gmail.com")
SENDER_NAME = os.getenv("SENDER_NAME", "Hemotec")
DEBUG = os.getenv("DEBUG", "True").lower() == "true"  # Modo desenvolvimento

def gerar_codigo_verificacao() -> str:
    """Gera um código de verificação de 6 dígitos"""
    return str(random.randint(100000, 999999))

def enviar_email_verificacao(email: str, nome: str, codigo: str) -> bool:
    """
    Envia email com código de verificação usando Resend
    
    Args:
        email: Email do destinatário
        nome: Nome do destinatário
        codigo: Código de verificação de 6 dígitos
    
    Returns:
        True se o email foi enviado com sucesso, False caso contrário
    """
    # Modo desenvolvimento: apenas simula envio
    if DEBUG:
        print(f"")
        print(f"{'='*60}")
        print(f"📧 MODO DESENVOLVIMENTO - EMAIL NÃO ENVIADO")
        print(f"{'='*60}")
        print(f"Para: {email}")
        print(f"Nome: {nome}")
        print(f"Código de Verificação: {codigo}")
        print(f"{'='*60}")
        print(f"")
        return True
    
    try:
        import resend
        
        # Configurar API key
        resend.api_key = RESEND_API_KEY
        
        # Criar HTML do email
        html_content = f"""
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Verificação de Email - Hemotec</title>
        </head>
        <body style="margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f5f5f5;">
            <table role="presentation" style="width: 100%; border-collapse: collapse;">
                <tr>
                    <td align="center" style="padding: 40px 0;">
                        <table role="presentation" style="width: 600px; border-collapse: collapse; background-color: #ffffff; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                            <!-- Header -->
                            <tr>
                                <td style="padding: 40px 40px 20px 40px; text-align: center; background: linear-gradient(135deg, #dc3545 0%, #c82333 100%); border-radius: 8px 8px 0 0;">
                                    <h1 style="margin: 0; color: #ffffff; font-size: 28px; font-weight: 600;">
                                        🩸 Hemotec
                                    </h1>
                                    <p style="margin: 10px 0 0 0; color: #ffffff; font-size: 14px; opacity: 0.9;">
                                        Plataforma de Doação de Sangue
                                    </p>
                                </td>
                            </tr>
                            
                            <!-- Content -->
                            <tr>
                                <td style="padding: 40px;">
                                    <h2 style="margin: 0 0 20px 0; color: #333333; font-size: 24px; font-weight: 600;">
                                        Bem-vindo(a), {nome}!
                                    </h2>
                                    
                                    <p style="margin: 0 0 20px 0; color: #666666; font-size: 16px; line-height: 1.6;">
                                        Obrigado por se cadastrar na Hemotec. Para completar seu cadastro e ter acesso à plataforma, 
                                        por favor, verifique seu endereço de email usando o código abaixo:
                                    </p>
                                    
                                    <!-- Código de Verificação -->
                                    <table role="presentation" style="width: 100%; border-collapse: collapse; margin: 30px 0;">
                                        <tr>
                                            <td align="center">
                                                <div style="background-color: #f8f9fa; border: 2px dashed #dc3545; border-radius: 8px; padding: 20px;">
                                                    <p style="margin: 0 0 10px 0; color: #666666; font-size: 14px; text-transform: uppercase; letter-spacing: 1px;">
                                                        Seu Código de Verificação
                                                    </p>
                                                    <p style="margin: 0; color: #dc3545; font-size: 36px; font-weight: bold; letter-spacing: 8px; font-family: 'Courier New', monospace;">
                                                        {codigo}
                                                    </p>
                                                </div>
                                            </td>
                                        </tr>
                                    </table>
                                    
                                    <p style="margin: 20px 0 0 0; color: #666666; font-size: 14px; line-height: 1.6;">
                                        <strong>⏰ Este código expira em 30 minutos.</strong>
                                    </p>
                                    
                                    <p style="margin: 20px 0 0 0; color: #666666; font-size: 14px; line-height: 1.6;">
                                        Se você não criou uma conta na Hemotec, por favor ignore este email.
                                    </p>
                                </td>
                            </tr>
                            
                            <!-- Footer -->
                            <tr>
                                <td style="padding: 20px 40px; background-color: #f8f9fa; border-radius: 0 0 8px 8px; text-align: center;">
                                    <p style="margin: 0; color: #999999; font-size: 12px; line-height: 1.6;">
                                        Este é um email automático, por favor não responda.<br>
                                        © 2025 Hemotec. Todos os direitos reservados.
                                    </p>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
            </table>
        </body>
        </html>
        """
        
        # Enviar email
        params = {
            "from": f"{SENDER_NAME} <{SENDER_EMAIL}>",
            "to": [email],
            "subject": f"Código de Verificação Hemotec - {codigo}",
            "html": html_content,
        }
        
        response = resend.Emails.send(params)
        print(f"✓ Email enviado com sucesso para {email}. ID: {response.get('id')}")
        return True
        
    except Exception as e:
        print(f"✗ Erro ao enviar email para {email}: {str(e)}")
        return False

def validar_codigo_verificacao(codigo_fornecido: str, codigo_armazenado: str, data_codigo: str, minutos_validade: int = 30) -> bool:
    """
    Valida se o código de verificação está correto e ainda é válido
    
    Args:
        codigo_fornecido: Código informado pelo usuário
        codigo_armazenado: Código armazenado no banco
        data_codigo: Data/hora em que o código foi gerado (string ISO format)
        minutos_validade: Tempo de validade do código em minutos (padrão: 30)
    
    Returns:
        True se o código é válido, False caso contrário
    """
    if not codigo_fornecido or not codigo_armazenado:
        return False
    
    # Verificar se o código está correto
    if codigo_fornecido.strip() != codigo_armazenado.strip():
        return False
    
    # Verificar se o código ainda é válido (não expirou)
    try:
        data_codigo_dt = datetime.fromisoformat(data_codigo)
        data_expiracao = data_codigo_dt + timedelta(minutes=minutos_validade)
        
        if datetime.now() > data_expiracao:
            return False
        
        return True
        
    except (ValueError, TypeError):
        return False
