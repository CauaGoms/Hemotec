#!/usr/bin/env python3
"""
Script de teste para verificar se a alteração de senha funciona
"""
import sys
from data.repo import usuario_repo
from util.security import criar_hash_senha

def teste_alterar_senha():
    print("="*60)
    print("TESTE DE ALTERAÇÃO DE SENHA")
    print("="*60)
    
    # Teste 1: Verificar se existe algum usuário
    print("\n1. Buscando primeiro usuário no banco...")
    
    # Vamos tentar buscar o usuário com ID 1
    usuario = usuario_repo.obter_por_id(1)
    
    if not usuario:
        print("   ❌ Usuário com ID 1 não encontrado")
        print("   Tentando buscar qualquer usuário...")
        # Se não houver usuário 1, vamos criar um teste ou usar outro ID
        return False
    
    print(f"   ✓ Usuário encontrado: {usuario.nome} (ID: {usuario.cod_usuario})")
    print(f"   Email: {usuario.email}")
    
    # Teste 2: Criar hash de uma nova senha
    print("\n2. Criando hash da nova senha de teste...")
    nova_senha = "SenhaTeste123"
    senha_hash = criar_hash_senha(nova_senha)
    print(f"   ✓ Hash criado: {senha_hash[:50]}...")
    
    # Teste 3: Tentar atualizar a senha
    print("\n3. Tentando atualizar senha no banco...")
    try:
        sucesso = usuario_repo.atualizar_senha(usuario.cod_usuario, senha_hash)
        
        if sucesso:
            print("   ✅ SENHA ATUALIZADA COM SUCESSO!")
            
            # Teste 4: Verificar se realmente foi salvo
            print("\n4. Verificando se a senha foi realmente salva...")
            usuario_atualizado = usuario_repo.obter_por_id(usuario.cod_usuario)
            
            if usuario_atualizado.senha == senha_hash:
                print("   ✅ SENHA CONFIRMADA NO BANCO!")
                print("\n" + "="*60)
                print("TODOS OS TESTES PASSARAM! ✅")
                print("="*60)
                return True
            else:
                print("   ❌ Senha no banco é diferente da que foi salva")
                print(f"   Esperado: {senha_hash[:50]}...")
                print(f"   Obtido:   {usuario_atualizado.senha[:50]}...")
                return False
        else:
            print("   ❌ Falha ao atualizar senha (rowcount = 0)")
            return False
            
    except Exception as e:
        print(f"   ❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    resultado = teste_alterar_senha()
    sys.exit(0 if resultado else 1)
