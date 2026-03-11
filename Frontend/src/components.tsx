import React from 'react';

interface LoginFormProps {
  onSubmit: (correo: string, contraseña: string) => Promise<void>;
  isLoading: boolean;
  error: string | null;
  onErrorDismiss: () => void;
}

export const LoginForm: React.FC<LoginFormProps> = ({
  onSubmit,
  isLoading,
  error,
  onErrorDismiss,
}) => {
  const [correo, setCorreo] = React.useState('');
  const [contraseña, setContraseña] = React.useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await onSubmit(correo, contraseña);
    } catch {
      // Error ya está manejado en el hook
    }
  };

  return (
    <form onSubmit={handleSubmit} className="login-card">
      <h2>Iniciar Sesión</h2>

      {error && (
        <div className="error-message" role="alert">
          {error}
          <button
            type="button"
            onClick={onErrorDismiss}
            aria-label="Cerrar mensaje de error"
            style={{
              background: 'none',
              border: 'none',
              color: 'inherit',
              cursor: 'pointer',
              marginLeft: '0.5rem',
              fontWeight: 'bold',
            }}
          >
            ✕
          </button>
        </div>
      )}

      <div className="form-group">
        <label htmlFor="correo">Correo Electrónico</label>
        <input
          id="correo"
          type="email"
          placeholder="tu.correo@ulsa.edu.mx"
          value={correo}
          onChange={(e) => setCorreo(e.target.value)}
          disabled={isLoading}
          required
          aria-label="Correo electrónico"
        />
      </div>

      <div className="form-group">
        <label htmlFor="contraseña">Contraseña</label>
        <input
          id="contraseña"
          type="password"
          placeholder="Ingresa tu contraseña"
          value={contraseña}
          onChange={(e) => setContraseña(e.target.value)}
          disabled={isLoading}
          required
          aria-label="Contraseña"
        />
      </div>

      <button
        type="submit"
        className="btn btn-primary"
        disabled={isLoading}
        aria-label="Iniciar sesión"
      >
        {isLoading && <span className="loading-spinner" />}
        {isLoading ? 'Iniciando sesión...' : 'Iniciar Sesión'}
      </button>

      <p className="login-help" role="button" tabIndex={0}>
        ¿Problemas para ingresar?
      </p>
    </form>
  );
};

interface EquipmentCardProps {
  nombre: string;
  descripcion: string;
  disponible: boolean;
  onRequestLoan: () => void;
}

export const EquipmentCard: React.FC<EquipmentCardProps> = ({
  nombre,
  descripcion,
  disponible,
  onRequestLoan,
}) => {
  return (
    <div className="equipment-card">
      <div className="equipment-card-header">
        <h3>{nombre}</h3>
        <span
          className={`status-badge ${
            disponible ? 'status-available' : 'status-unavailable'
          }`}
          role="status"
          aria-label={disponible ? 'Disponible' : 'No disponible'}
        >
          {disponible ? 'Disponible' : 'No Disponible'}
        </span>
      </div>
      <p>{descripcion}</p>
      <button
        className="btn btn-primary"
        onClick={onRequestLoan}
        disabled={!disponible}
        aria-label={`Solicitar préstamo de ${nombre}`}
      >
        Solicitar Préstamo
      </button>
    </div>
  );
};

interface LoanRowProps {
  id: string;
  estudiante: string;
  equipo: string;
  estado: 'pendiente' | 'aprobado' | 'rechazado';
  onApprove: (id: string) => void;
  onReject: (id: string) => void;
}

export const LoanRow: React.FC<LoanRowProps> = ({
  id,
  estudiante,
  equipo,
  estado,
  onApprove,
  onReject,
}) => {
  const getStatusClass = () => {
    switch (estado) {
      case 'pendiente':
        return 'status-pending';
      case 'aprobado':
        return 'status-approved';
      case 'rechazado':
        return 'status-rejected';
      default:
        return '';
    }
  };

  return (
    <tr>
      <td>{estudiante}</td>
      <td>{equipo}</td>
      <td>
        <span className={getStatusClass()}>{estado}</span>
      </td>
      <td>
        <div className="action-buttons">
          <button
            className="btn btn-primary btn-sm"
            onClick={() => onApprove(id)}
            disabled={estado !== 'pendiente'}
            aria-label={`Aprobar préstamo de ${estudiante}`}
          >
            Aprobar
          </button>
          <button
            className="btn btn-danger btn-sm"
            onClick={() => onReject(id)}
            disabled={estado !== 'pendiente'}
            aria-label={`Rechazar préstamo de ${estudiante}`}
          >
            Rechazar
          </button>
        </div>
      </td>
    </tr>
  );
};
