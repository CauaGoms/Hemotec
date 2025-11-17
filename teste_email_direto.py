"""
Teste Direto - Envio de Email de Boas-Vindas
Execute: python teste_email_direto.py
"""

import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

print("\n" + "="*60)
print("🧪 TESTE DIRETO - EMAIL DE BOAS-VINDAS")
print("="*60 + "\n")

# Verificar variáveis de ambiente
print("📋 Variáveis de Ambiente:")
print(f"  RESEND_API_KEY: {'✅ Configurada' if os.getenv('RESEND_API_KEY') else '❌ NÃO CONFIGURADA'}")
print(f"  RESEND_FROM_EMAIL: {os.getenv('RESEND_FROM_EMAIL', 'NÃO CONFIGURADO')}")
print(f"  RESEND_FROM_NAME: {os.getenv('RESEND_FROM_NAME', 'NÃO CONFIGURADO')}")
print(f"  BASE_URL: {os.getenv('BASE_URL', 'NÃO CONFIGURADO')}\n")

# Importar e testar email service
print("📧 Testando EmailService...\n")

try:
    from util.email_service import email_service
    
    # Solicitar email de teste
    email_teste = input("Digite um EMAIL para teste: ").strip()
    nome_teste = input("Digite um NOME para teste: ").strip()
    
    if not email_teste or not nome_teste:
        print("❌ Email e nome são obrigatórios!")
        exit(1)
    
    print(f"\n{'='*60}")
    print(f"Enviando email de boas-vindas...")
    print(f"{'='*60}\n")
    
    resultado = email_service.enviar_boas_vindas(
        para_email=email_teste,
        para_nome=nome_teste
    )
    
    print(f"\n{'='*60}")
    if resultado:
        print(f"✅ SUCESSO! Email enviado.")
        print(f"Verifique a caixa de entrada de: {email_teste}")
    else:
        print(f"❌ FALHA! Email não foi enviado.")
        print(f"Verifique os logs acima para detalhes do erro.")
    print(f"{'='*60}\n")
    
except Exception as e:
    print(f"❌ ERRO CRÍTICO: {e}")
    import traceback
    traceback.print_exc()
