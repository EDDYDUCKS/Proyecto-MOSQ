import { useState } from 'react';
import './styles.css';
import { Vista, Prestamo } from './types';
import { useAuth } from './useAuth';
import { LoginForm, EquipmentCard, LoanRow } from './components';

export default function App() {
  const [vistaActual, setVistaActual] = useState<Vista>('login');
  const [activeTab, setActiveTab] = useState<'prestamos' | 'inventario' | 'reportes'>('prestamos');
  const [loans, setLoans] = useState<Prestamo[]>([
    {
      id: '1',
      usuarioId: 'user1',
      equipoId: 'eq1',
      estado: 'pendiente',
      fechaSolicitud: new Date('2024-01-15'),
    },
    {
      id: '2',
      usuarioId: 'user2',
      equipoId: 'eq2',
      estado: 'aprobado',
      fechaSolicitud: new Date('2024-01-10'),
      fechaAprobacion: new Date('2024-01-11'),
    },
  ]);

  const { usuario, isAuthenticated, isLoading, error, login, logout, clearError } = useAuth();

  // --- PANTALLA DE LOGIN ---
  if (vistaActual === 'login' && !isAuthenticated) {
    return (
      <div className="login-container">
        <div className="login-header">
          <h2>La Salle | ULSA</h2>
          <h1>Sistema de gestión prestamos de equipos deportivos</h1>
        </div>

        <LoginForm
          onSubmit={async (correo, contraseña) => {
            await login({ correo, contraseña });
            setVistaActual('estudiante');
          }}
          isLoading={isLoading}
          error={error}
          onErrorDismiss={clearError}
        />
      </div>
    );
  }

  // --- PANTALLA DEL ESTUDIANTE ---
  if (vistaActual === 'estudiante' && isAuthenticated) {
    return (
      <div className="student-container">
        {/* Barra Lateral (Sidebar) */}
        <div className="sidebar">
          <h2>ULSA</h2>
          <ul>
            <li className="active" role="menuitem">
              Dashboard
            </li>
            <li role="menuitem">Buscar Préstamo</li>
            <li role="menuitem">Mis Solicitudes</li>
          </ul>
        </div>

        {/* Contenido Principal */}
        <div className="main-content">
          {/* Banner de Bienvenida */}
          <div className="welcome-banner">
            <div>
              <h1>Bienvenido, Estudiante</h1>
              <p>Solicita préstamos de equipos deportivos</p>
            </div>
            <button
              className="btn btn-danger"
              onClick={() => {
                logout();
                setVistaActual('login');
              }}
              aria-label="Cerrar sesión"
            >
              Cerrar Sesión
            </button>
          </div>

          <h2 className="section-title">Objetos Populares</h2>

          {/* Cuadrícula de Equipos */}
          <div className="equipment-grid">
            <EquipmentCard
              key="basketball"
              nombre="Balón de Básquet"
              descripcion="Apto para canchas exteriores e interiores."
              disponible={true}
              onRequestLoan={() => alert('Solicitud de préstamo enviada')}
            />

            <EquipmentCard
              key="chessboard"
              nombre="Tablero de Ajedrez"
              descripcion="Incluye piezas completas."
              disponible={true}
              onRequestLoan={() => alert('Solicitud de préstamo enviada')}
            />
          </div>
        </div>
      </div>
    );
  }

  // --- PANTALLA DE LA ENCARGADA ---
  if (vistaActual === 'encargada' && isAuthenticated) {
    const handleApproveLoan = (id: string) => {
      setLoans((prevLoans) =>
        prevLoans.map((loan) =>
          loan.id === id
            ? {
                ...loan,
                estado: 'aprobado' as const,
                fechaAprobacion: new Date(),
              }
            : loan
        )
      );
    };

    const handleRejectLoan = (id: string) => {
      setLoans((prevLoans) =>
        prevLoans.map((loan) =>
          loan.id === id ? { ...loan, estado: 'rechazado' as const } : loan
        )
      );
    };

    return (
      <div className="manager-container">
        {/* Barra Lateral (Sidebar) */}
        <div className="sidebar">
          <h2>ULSA</h2>
          <ul>
            <li
              className={activeTab === 'prestamos' ? 'active' : ''}
              onClick={() => setActiveTab('prestamos')}
              role="menuitem"
            >
              Todos los Préstamos
            </li>
            <li
              className={activeTab === 'inventario' ? 'active' : ''}
              onClick={() => setActiveTab('inventario')}
              role="menuitem"
            >
              Inventario
            </li>
            <li
              className={activeTab === 'reportes' ? 'active' : ''}
              onClick={() => setActiveTab('reportes')}
              role="menuitem"
            >
              Reportes
            </li>
          </ul>
        </div>

        {/* Contenido Principal */}
        <div className="manager-main">
          {/* Banner de Encargada */}
          <div className="manager-header">
            <div>
              <h1>Panel de Encargada</h1>
              <p>Gestión de inventario y préstamos</p>
            </div>
            <button
              className="btn btn-danger"
              onClick={() => {
                logout();
                setVistaActual('login');
              }}
              aria-label="Cerrar sesión"
            >
              Cerrar Sesión
            </button>
          </div>

          {/* Tabs */}
          <div className="tabs">
            <button
              className={`tab ${activeTab === 'prestamos' ? 'active' : ''}`}
              onClick={() => setActiveTab('prestamos')}
              aria-label="Todos los préstamos"
              aria-selected={activeTab === 'prestamos'}
            >
              Todos los Préstamos
            </button>
            <button
              className={`tab ${activeTab === 'inventario' ? 'active' : ''}`}
              onClick={() => setActiveTab('inventario')}
              aria-label="Inventario"
              aria-selected={activeTab === 'inventario'}
            >
              Inventario
            </button>
            <button
              className={`tab ${activeTab === 'reportes' ? 'active' : ''}`}
              onClick={() => setActiveTab('reportes')}
              aria-label="Reportes"
              aria-selected={activeTab === 'reportes'}
            >
              Reportes
            </button>
          </div>

          {/* Contenido de Tabs */}
          {activeTab === 'prestamos' && (
            <div>
              <h2 className="section-title">Todos los Préstamos</h2>
              <table className="loans-table" role="table">
                <thead>
                  <tr>
                    <th>Estudiante</th>
                    <th>Equipo</th>
                    <th>Estado</th>
                    <th>Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  {loans.map((loan) => (
                    <LoanRow
                      key={loan.id}
                      id={loan.id}
                      estudiante={`Usuario ${loan.usuarioId}`}
                      equipo={`Equipo ${loan.equipoId}`}
                      estado={loan.estado as 'pendiente' | 'aprobado' | 'rechazado'}
                      onApprove={handleApproveLoan}
                      onReject={handleRejectLoan}
                    />
                  ))}
                </tbody>
              </table>
            </div>
          )}

          {activeTab === 'inventario' && (
            <div>
              <h2 className="section-title">Inventario</h2>
              <p>Gestión de inventario en desarrollo...</p>
            </div>
          )}

          {activeTab === 'reportes' && (
            <div>
              <h2 className="section-title">Reportes</h2>
              <p>Reportes en desarrollo...</p>
            </div>
          )}
        </div>
      </div>
    );
  }

  // Fallback seguro (no debería alcanzarse con el tipado actual)
  return (
    <div style={{ padding: '2rem', fontFamily: 'sans-serif' }}>
      <p>Algo salió mal. Por favor intenta de nuevo.</p>
      <button
        className="btn btn-primary"
        onClick={() => {
          logout();
          setVistaActual('login');
        }}
      >
        Volver al Login
      </button>
    </div>
  );
}
