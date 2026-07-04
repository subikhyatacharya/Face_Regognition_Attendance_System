import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import ScannerUI from './pages/ScannerUI';
import AdminDashboard from './pages/AdminDashboard';
import UserManagement from './pages/UserManagement';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<ScannerUI />} />
        <Route path="/admin" element={<AdminDashboard />} />
        <Route path="/admin/users" element={<UserManagement />} />
      </Routes>
    </Router>
  );
}

export default App;