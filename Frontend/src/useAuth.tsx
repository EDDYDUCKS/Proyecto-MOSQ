import { useState, useCallback, useEffect } from 'react';
import { AuthState, LoginCredentials, Usuario } from './types';

const STORAGE_KEY = 'auth_user';

export const useAuth = () => {
  const [authState, setAuthState] = useState<AuthState>({
    usuario: null,
    isAuthenticated: false,
    isLoading: false,
    error: null,
  });

  // Cargar usuario del localStorage al montar
  useEffect(() => {
    const storedUser = localStorage.getItem(STORAGE_KEY);
    if (storedUser) {
      try {
        const usuario = JSON.parse(storedUser);
        setAuthState({
          usuario,
          isAuthenticated: true,
          isLoading: false,
          error: null,
        });
      } catch (error) {
        localStorage.removeItem(STORAGE_KEY);
      }
    }
  }, []);

  const login = useCallback(async (credentials: LoginCredentials) => {
    setAuthState((prev) => ({ ...prev, isLoading: true, error: null }));

    try {
      // Simulación de autenticación
      // En una aplicación real, esto sería una llamada a un servidor
      await new Promise((resolve) => setTimeout(resolve, 1000));

      // Validación básica
      if (!credentials.correo || !credentials.contraseña) {
        throw new Error('Correo y contraseña son requeridos');
      }

      if (!credentials.correo.includes('@')) {
        throw new Error('Correo inválido');
      }

      if (credentials.contraseña.length < 6) {
        throw new Error('La contraseña debe tener al menos 6 caracteres');
      }

      // Crear usuario simulado
      const usuario: Usuario = {
        id: Math.random().toString(36).substr(2, 9),
        nombre: credentials.correo.split('@')[0],
        correo: credentials.correo,
        rol: 'estudiante',
      };

      // Guardar en localStorage
      localStorage.setItem(STORAGE_KEY, JSON.stringify(usuario));

      setAuthState({
        usuario,
        isAuthenticated: true,
        isLoading: false,
        error: null,
      });

      return usuario;
    } catch (error) {
      const errorMessage =
        error instanceof Error ? error.message : 'Error al iniciar sesión';
      setAuthState((prev) => ({
        ...prev,
        isLoading: false,
        error: errorMessage,
      }));
      throw error;
    }
  }, []);

  const logout = useCallback(() => {
    localStorage.removeItem(STORAGE_KEY);
    setAuthState({
      usuario: null,
      isAuthenticated: false,
      isLoading: false,
      error: null,
    });
  }, []);

  const clearError = useCallback(() => {
    setAuthState((prev) => ({ ...prev, error: null }));
  }, []);

  return {
    ...authState,
    login,
    logout,
    clearError,
  };
};
