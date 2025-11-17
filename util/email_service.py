import os
import resend
from typing import Optional

class EmailService:
    def __init__(self):
        # Remove espaços em branco extras da API key
        self.api_key = os.getenv('RESEND_API_KEY', '').strip()
        self.from_email = os.getenv('RESEND_FROM_EMAIL', 'noreply@seudominio.com').strip()
        self.from_name = os.getenv('RESEND_FROM_NAME', 'Sistema').strip()

        # Configura a API key do Resend
        if self.api_key:
            resend.api_key = self.api_key
            print(f"[EMAIL SERVICE INIT] ✅ Configurado com API key: {self.api_key[:10]}...")
        else:
            print(f"[EMAIL SERVICE INIT] ❌ API key não encontrada!")

    def enviar_email(
        self,
        para_email: str,
        para_nome: str,
        assunto: str,
        html: str,
        texto: Optional[str] = None
    ) -> bool:
        """Envia e-mail via Resend.com"""
        print(f"\n[EMAIL SERVICE] Tentando enviar email...")
        print(f"  Para: {para_email}")
        print(f"  Assunto: {assunto}")
        print(f"  API Key configurada: {'Sim' if self.api_key else 'NÃO'}")
        print(f"  From: {self.from_name} <{self.from_email}>")
        
        if not self.api_key:
            print("❌ ERRO: RESEND_API_KEY não configurada no .env")
            return False

        params = {
            "from": f"{self.from_name} <{self.from_email}>",
            "to": [para_email],
            "subject": assunto,
            "html": html
        }

        try:
            print(f"  Chamando Resend API...")
            email = resend.Emails.send(params)  # type: ignore[arg-type]
            print(f"✅ E-mail enviado com sucesso para {para_email}")
            print(f"  ID do email: {email.get('id', 'N/A')}")
            return True
        except Exception as e:
            print(f"❌ ERRO ao enviar e-mail: {e}")
            import traceback
            traceback.print_exc()
            return False

    def enviar_recuperacao_senha(self, para_email: str, para_nome: str, token: str) -> bool:
        """Envia e-mail de recuperação de senha"""
        # Usa a URL do .env ou URL padrão do site
        base_url = os.getenv('BASE_URL', 'https://hemotec.cachoeiro.es')
        url_recuperacao = f"{base_url}/redefinir-senha?token={token}"

        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px; background-color: #f9f9f9; border-radius: 10px;">
                <h2 style="color: #c41e3a;">Recuperação de Senha</h2>
                <p>Olá <strong>{para_nome}</strong>,</p>
                <p>Você solicitou a recuperação de senha no sistema Hemotec.</p>
                <p>Clique no botão abaixo para redefinir sua senha:</p>
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{url_recuperacao}" 
                       style="background-color: #c41e3a; color: white; padding: 12px 30px; 
                              text-decoration: none; border-radius: 5px; display: inline-block;">Redefinir Senha</a>
                </div>
                <p style="color: #666; font-size: 14px;">Este link expira em 1 hora.</p>
                <p style="color: #666; font-size: 14px;">Se você não solicitou esta recuperação, ignore este e-mail.</p>
                <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
                <p style="color: #999; font-size: 12px;">Hemotec - Sistema de Gestão de Doação de Sangue</p>
            </div>
        </body>
        </html>
        """

        return self.enviar_email(
            para_email=para_email,
            para_nome=para_nome,
            assunto="Recuperação de Senha - Hemotec",
            html=html
        )

    def enviar_boas_vindas(self, para_email: str, para_nome: str) -> bool:
        """Envia e-mail de boas-vindas"""
        # base_url = os.getenv('BASE_URL', 'http://localhost:8000')
        base_url = os.getenv('BASE_URL', 'https://hemotec.cachoeiro.es')
        url_login = f"{base_url}/login"
        
        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px; background-color: #f9f9f9; border-radius: 10px;">
                <h2 style="color: #c41e3a;">Bem-vindo(a) ao Hemotec! 🎉</h2>
                <p>Olá <strong>{para_nome}</strong>,</p>
                <p>Seu cadastro foi realizado com <strong>sucesso</strong>!</p>
                <p>Agora você pode acessar o sistema Hemotec com seu e-mail e senha.</p>
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{url_login}" 
                       style="background-color: #c41e3a; color: white; padding: 12px 30px; 
                              text-decoration: none; border-radius: 5px; display: inline-block;">Fazer Login</a>
                </div>
                <p style="color: #666; font-size: 14px;">Com o Hemotec, você pode:</p>
                <ul style="color: #666; font-size: 14px;">
                    <li>Agendar doações de sangue</li>
                    <li>Acompanhar seu histórico de doações</li>
                    <li>Receber notificações importantes</li>
                    <li>Contribuir para salvar vidas</li>
                </ul>
                <p>Obrigado por fazer parte desta causa! ❤️</p>
                <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
                <p style="color: #999; font-size: 12px;">Hemotec - Sistema de Gestão de Doação de Sangue</p>
            </div>
        </body>
        </html>
        """

        return self.enviar_email(
            para_email=para_email,
            para_nome=para_nome,
            assunto="Bem-vindo ao Hemotec! 🎉",
            html=html
        )

# Instância global
email_service = EmailService()