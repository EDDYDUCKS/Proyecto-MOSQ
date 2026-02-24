import { useState } from 'react';

// Tipado explícito para las vistas válidas
type Vista = 'login' | 'estudiante' | 'encargada';

export default function App() {
  // Este estado controlará qué pantalla estamos viendo ('login', 'estudiante', 'encargada')
  const [vistaActual, setVistaActual] = useState<Vista>('login');

  // --- PANTALLA DE LOGIN ---
  if (vistaActual === 'login') {
    return (
      <div style={{ backgroundColor: '#051f14', minHeight: '100vh', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', color: 'white', fontFamily: 'sans-serif' }}>
        
        <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
          <h2 style={{ color: '#22c55e', margin: 0 }}>La Salle | ULSA</h2>
          <h1 style={{ fontSize: '1.5rem', fontWeight: 'normal', marginTop: '1rem' }}>
            Sistema de gestión<br />
            prestamos de equipos deportivos
          </h1>
        </div>

        <div style={{ backgroundColor: '#e5e7eb', padding: '2rem 3rem', borderRadius: '8px', textAlign: 'center', color: '#111827' }}>
          <h2 style={{ margin: '0 0 1.5rem 0', fontSize: '1.25rem' }}>Iniciar Sesión</h2>
          
          <button 
            style={{ backgroundColor: '#16a34a', color: 'white', border: 'none', padding: '0.75rem 1.5rem', borderRadius: '4px', fontSize: '1rem', cursor: 'pointer', width: '100%', fontWeight: 'bold' }}
            onClick={() => setVistaActual('estudiante')} // Por ahora, este botón nos manda directo a la vista del estudiante
          >
            Ingresar con correo
          </button>
          
          <p style={{ fontSize: '0.8rem', color: '#3b82f6', marginTop: '1rem', cursor: 'pointer' }}>
            ¿Problemas para ingresar?
          </p>
        </div>

      </div>
    );
  }

// --- PANTALLA DEL ESTUDIANTE ---
  if (vistaActual === 'estudiante') {
    return (
      <div style={{ display: 'flex', minHeight: '100vh', backgroundColor: '#f3f4f6', fontFamily: 'sans-serif' }}>
        
        {/* Barra Lateral (Sidebar) */}
        <div style={{ width: '250px', backgroundColor: '#051f14', color: 'white', padding: '2rem', display: 'flex', flexDirection: 'column' }}>
          <h2 style={{ color: '#22c55e', margin: '0 0 2rem 0', fontSize: '1.5rem' }}>ULSA</h2>
          <ul style={{ listStyle: 'none', padding: 0, margin: 0, display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            <li style={{ backgroundColor: '#16a34a', padding: '0.75rem 1rem', borderRadius: '8px', cursor: 'pointer', fontWeight: 'bold' }}>Dashboard</li>
            <li style={{ padding: '0.75rem 1rem', cursor: 'pointer', color: '#cbd5e1' }}>Buscar Préstamo</li>
            <li style={{ padding: '0.75rem 1rem', cursor: 'pointer', color: '#cbd5e1' }}>Mis Solicitudes</li>
          </ul>
        </div>

        {/* Contenido Principal */}
        <div style={{ flex: 1, padding: '2rem' }}>
          
          {/* Banner de Bienvenida */}
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', backgroundColor: '#0f172a', color: 'white', padding: '2rem', borderRadius: '12px', marginBottom: '2rem' }}>
            <div>
              <h1 style={{ margin: 0, fontSize: '1.75rem' }}>Bienvenido, Estudiante</h1>
              <p style={{ margin: '0.5rem 0 0 0', color: '#94a3b8' }}>Solicita préstamos de equipos deportivos</p>
            </div>
            <button 
              onClick={() => setVistaActual('login')} 
              style={{ backgroundColor: 'transparent', color: '#ef4444', border: '1px solid #ef4444', padding: '0.5rem 1.5rem', borderRadius: '8px', cursor: 'pointer', fontWeight: 'bold' }}
            >
              Cerrar Sesión
            </button>
          </div>

          <h2 style={{ color: '#1e293b', marginBottom: '1.5rem' }}>Objetos Populares</h2>
          
          {/* Cuadrícula de Equipos */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: '1.5rem' }}>
            
            {/* Tarjeta: Balón de Básquet */}
            <div style={{ backgroundColor: 'white', padding: '1.5rem', borderRadius: '12px', border: '1px solid #e2e8f0' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
                <h3 style={{ margin: 0, color: '#0f172a' }}>Balón de Básquet</h3>
                <span style={{ backgroundColor: '#dcfce7', color: '#16a34a', padding: '0.25rem 0.75rem', borderRadius: '999px', fontSize: '0.875rem', fontWeight: 'bold' }}>Disponible</span>
              </div>
              <p style={{ color: '#64748b', fontSize: '0.875rem', marginBottom: '1.5rem' }}>Apto para canchas exteriores e interiores.</p>
              <button style={{ width: '100%', backgroundColor: '#16a34a', color: 'white', border: 'none', padding: '0.75rem', borderRadius: '8px', cursor: 'pointer', fontWeight: 'bold' }}>
                Solicitar Préstamo
              </button>
            </div>

            {/* Tarjeta: Tablero de Ajedrez */}
            <div style={{ backgroundColor: 'white', padding: '1.5rem', borderRadius: '12px', border: '1px solid #e2e8f0' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
                <h3 style={{ margin: 0, color: '#0f172a' }}>Tablero de Ajedrez</h3>
                <span style={{ backgroundColor: '#dcfce7', color: '#16a34a', padding: '0.25rem 0.75rem', borderRadius: '999px', fontSize: '0.875rem', fontWeight: 'bold' }}>Disponible</span>
              </div>
              <p style={{ color: '#64748b', fontSize: '0.875rem', marginBottom: '1.5rem' }}>Incluye piezas completas.</p>
              <button style={{ width: '100%', backgroundColor: '#16a34a', color: 'white', border: 'none', padding: '0.75rem', borderRadius: '8px', cursor: 'pointer', fontWeight: 'bold' }}>
                Solicitar Préstamo
              </button>
            </div>

          </div>
        </div>
      </div>
    );
  }

  // --- PANTALLA DE LA ENCARGADA (Boceto inicial) ---
  if (vistaActual === 'encargada') {
    return (
      <div style={{ padding: '2rem', fontFamily: 'sans-serif' }}>
        <h1>Panel de Encargada</h1>
        <p>Gestión de inventario y préstamos.</p>
        <button 
          onClick={() => setVistaActual('login')}
          style={{ padding: '0.5rem 1rem', cursor: 'pointer' }}
        >
          Cerrar Sesión
        </button>
      </div>
    );
  }

  // Fallback seguro (no debería alcanzarse con el tipado actual)
  return (
    <div style={{ padding: '2rem', fontFamily: 'sans-serif' }}>
      <p>Vista no reconocida. Regresando al inicio...</p>
      <button 
        onClick={() => setVistaActual('login')}
        style={{ padding: '0.5rem 1rem', cursor: 'pointer' }}
      >
        Ir a Login
      </button>
    </div>
  );
}