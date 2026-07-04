import { Navigate } from 'react-router-dom';

/**
 * Wraps a route and redirects to /login if no auth token is present.
 * Usage: <Route path="/admin" element={<ProtectedRoute><AdminDashboard /></ProtectedRoute>} />
 */
const ProtectedRoute = ({ children }) => {
  const token = localStorage.getItem('token');

  if (!token) {
    return <Navigate to="/login" replace />;
  }

  return children;
};

export default ProtectedRoute;
