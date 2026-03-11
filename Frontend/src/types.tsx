// Tipos para la aplicación
export type Vista = 'login' | 'estudiante' | 'encargada';

export interface Usuario {
  id: string;
  nombre: string;
  correo: string;
  rol: 'estudiante' | 'encargada';
}

export interface Equipo {
  id: string;
  nombre: string;
  descripcion: string;
  disponible: boolean;
  cantidad: number;
}

export interface Prestamo {
  id: string;
  usuarioId: string;
  equipoId: string;
  estado: 'pendiente' | 'aprobado' | 'rechazado' | 'devuelto';
  fechaSolicitud: Date;
  fechaAprobacion?: Date;
  fechaDevolucion?: Date;
}

export interface AuthState {
  usuario: Usuario | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
}

export interface LoginCredentials {
  correo: string;
  contraseña: string;
}
