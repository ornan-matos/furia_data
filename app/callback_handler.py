import streamlit as st
from app.x_api import trocar_codigo_por_token

def processar_callback():
    params = st.query_params
    code = params.get("code", None)

    # ✅ Só tenta trocar o código se ainda não está autenticado
    if code and not st.session_state.get("x_autenticado"):
        print(f"[DEBUG] Código de autorização recebido: {code}")

        try:
            sucesso = trocar_codigo_por_token(code)
            if sucesso:
                st.session_state["x_autenticado"] = True
                st.success("✅ Conectado com o X com sucesso!")
                st.rerun()  # atualiza para evitar reprocessar
            else:
                # Evita mostrar erro visual, apenas loga
                print("[DEBUG] Código inválido ou já utilizado, ignorado.")
        except Exception as e:
            print(f"[ERRO] Falha ao trocar código por token: {str(e)}")
