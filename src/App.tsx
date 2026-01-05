import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import DashboardLayout from './layouts/DashboardLayout';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import WarehouseList from './pages/WarehouseList';
import ShopList from './pages/ShopList';
import MedicineList from './pages/MedicineList';
import MedicineDetails from './pages/MedicineDetails';
import EditMedicalShop from './pages/EditMedicalShop';
import ApplicationSettings from './pages/ApplicationSettings';
import SystemSettings from './pages/SystemSettings';
import ExpiryLossReport from './pages/ExpiryLossReport';
import ReturnRefund from './pages/ReturnRefund';

// Auth guard component
function PrivateRoute({ children }: { children: React.ReactNode }) {
  const token = localStorage.getItem('access_token');
  return token ? <>{children}</> : <Navigate to="/login" replace />;
}

function App() {
  return (
    <Router>
      <Routes>
        {/* Public routes */}
        <Route path="/login" element={<Login />} />

        {/* Protected routes */}
        <Route path="/" element={
          <PrivateRoute>
            <DashboardLayout />
          </PrivateRoute>
        }>
          <Route index element={<Dashboard />} />

          {/* Warehouses */}
          <Route path="warehouses" element={<WarehouseList />} />
          <Route path="warehouses/:id" element={<WarehouseList />} />
          <Route path="warehouses/:id/edit" element={<WarehouseList />} />

          {/* Shops */}
          <Route path="shops" element={<ShopList />} />
          <Route path="shops/:id" element={<ShopList />} />
          <Route path="shops/:id/edit" element={<EditMedicalShop />} />

          {/* Medicines */}
          <Route path="medicines" element={<MedicineList />} />
          <Route path="medicines/:id" element={<MedicineDetails />} />
          <Route path="medicines/:id/batches" element={<MedicineDetails />} />

          {/* Inventory */}
          <Route path="inventory" element={<MedicineList />} />

          {/* Sales & Billing */}
          <Route path="sales" element={<Dashboard />} />
          <Route path="sales/pos" element={<Dashboard />} />
          <Route path="sales/invoices" element={<Dashboard />} />
          <Route path="sales/returns" element={<ReturnRefund />} />

          {/* Reports */}
          <Route path="reports" element={<Dashboard />} />
          <Route path="reports/expiry" element={<ExpiryLossReport />} />

          {/* Settings */}
          <Route path="settings" element={<ApplicationSettings />} />
          <Route path="settings/application" element={<ApplicationSettings />} />
          <Route path="settings/system" element={<SystemSettings />} />
        </Route>

        {/* Fallback */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  );
}

export default App;
