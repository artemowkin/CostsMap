import { useState } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { CategoriesPage } from './components/Categories/CategoriesPage';
import { LoginPage } from './components/Login/LoginPage';
import './App.css';
import { useAuth } from './hooks/Auth/useAuth';
import { CardsPage } from './components/Cards/CardsPage';
import { AddCategoryPopUp } from './components/AddCategory/AddCategoryPopUp';

function App() {
  const { tokenValue } = useAuth();
  const [token, setToken] = useState(tokenValue);

  return (
    <>
      <Routes>
        <Route path="/" element={
          token ? <CategoriesPage token={token} /> : <Navigate to="/login" />
        } />
        <Route path="/add_category" element={
          token ? (<><CategoriesPage token={token} /><AddCategoryPopUp token={token} /></>) : <Navigate to="/login" />
        } />
        <Route path="/cards" element={
          token ? <CardsPage token={token} /> : <Navigate to="/login" />
        } />
        <Route path="/login" element={<LoginPage token={token} setToken={setToken} />} />
      </Routes>
    </>
  );
}

export default App;
