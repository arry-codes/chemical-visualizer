import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './Login';
import Dashboard from './Dashboard';

function App() {
  const [auth, setAuth] = useState(null);

  useEffect(() => {
    const storedAuth = localStorage.getItem('auth');
    if (storedAuth) {
      setAuth(JSON.parse(storedAuth));
    }
  }, []);

  return (
    <Router>
      <Routes>
        <Route
          path="/login"
          element={!auth ? <Login setAuth={setAuth} /> : <Navigate to="/dashboard" />}
        />
        <Route
          path="/dashboard"
          element={auth ? <Dashboard auth={auth} /> : <Navigate to="/login" />}
        />
        <Route
          path="/"
          element={<Navigate to={auth ? "/dashboard" : "/login"} />}
        />
      </Routes>
    </Router>
  );
}

export default App;
