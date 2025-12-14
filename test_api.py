import requests
import json

BASE_URL = "http://127.0.0.1:8000/api/users"

def print_response(title, response):
    print(f"\n{'='*60}")
    print(f"🔹 {title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"Response: {response.text}")
    print(f"{'='*60}\n")

def test_api():
    print("\n🚀 INICIANDO PRUEBAS DE API - USERS APP\n")
    
    # Test 1: Registro de usuario
    print("📝 TEST 1: Registro de nuevo usuario")
    register_data = {
        "email": "test@example.com",
        "password": "TestPassword123!"
    }
    response = requests.post(f"{BASE_URL}/register/", json=register_data)
    print_response("Registro de Usuario", response)
    
    # Test 2: Login
    print("🔐 TEST 2: Login de usuario")
    login_data = {
        "email": "test@example.com",
        "password": "TestPassword123!"
    }
    response = requests.post(f"{BASE_URL}/login/", json=login_data)
    print_response("Login de Usuario", response)
    
    if response.status_code == 200:
        token = response.json().get("token")
        headers = {"Authorization": f"Token {token}"}
        
        # Test 3: Ver perfil
        print("👤 TEST 3: Ver perfil del usuario autenticado")
        response = requests.get(f"{BASE_URL}/profile/", headers=headers)
        print_response("Ver Perfil", response)
        
        # Test 4: Actualizar perfil
        print("✏️ TEST 4: Actualizar perfil")
        update_data = {
            "first_name": "Updated",
            "last_name": "Name",
            "phone": "+34123456789"
        }
        response = requests.patch(f"{BASE_URL}/profile/", json=update_data, headers=headers)
        print_response("Actualizar Perfil", response)
        
        # Test 5: Listar todos los usuarios
        print("📋 TEST 5: Listar todos los usuarios")
        response = requests.get(f"{BASE_URL}/", headers=headers)
        print_response("Listar Usuarios", response)
        
        # Test 6: Cambiar contraseña
        print("🔑 TEST 6: Cambiar contraseña")
        change_password_data = {
            "old_password": "TestPassword123!",
            "new_password": "NewPassword123!",
            "new_password_confirm": "NewPassword123!"
        }
        response = requests.post(f"{BASE_URL}/change-password/", json=change_password_data, headers=headers)
        print_response("Cambiar Contraseña", response)
        
        if response.status_code == 200:
            new_token = response.json().get("token")
            headers = {"Authorization": f"Token {new_token}"}
            
            # Test 7: Login con nueva contraseña
            print("🔐 TEST 7: Login con nueva contraseña")
            login_data["password"] = "NewPassword123!"
            response = requests.post(f"{BASE_URL}/login/", json=login_data)
            print_response("Login con Nueva Contraseña", response)
    
    # Test 8: Intentar acceder sin autenticación
    print("🚫 TEST 8: Intentar acceder a perfil sin autenticación")
    response = requests.get(f"{BASE_URL}/profile/")
    print_response("Acceso sin Autenticación", response)
    
    # Test 9: Registro con email duplicado
    print("❌ TEST 9: Registro con email duplicado")
    bad_register_data = {
        "email": "test@example.com",  # Email ya registrado
        "password": "Password123!"
    }
    response = requests.post(f"{BASE_URL}/register/", json=bad_register_data)
    print_response("Registro con Email Duplicado", response)
    
    # Test 10: Login con credenciales incorrectas
    print("❌ TEST 10: Login con credenciales incorrectas")
    bad_login_data = {
        "email": "test@example.com",
        "password": "WrongPassword"
    }
    response = requests.post(f"{BASE_URL}/login/", json=bad_login_data)
    print_response("Login con Credenciales Incorrectas", response)
    
    print("\n✅ PRUEBAS COMPLETADAS\n")

if __name__ == "__main__":
    try:
        test_api()
    except Exception as e:
        print(f"\n❌ Error durante las pruebas: {str(e)}\n")
