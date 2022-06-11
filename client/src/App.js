import { useEffect, useState } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { CategoriesPage } from './components/Categories/CategoriesPage';
import { LoginPage } from './components/Login/LoginPage';
import './App.css';
import { useAuth } from './hooks/Auth/useAuth';
import { CardsPage } from './components/Cards/CardsPage';
import { AddCategoryPopUp } from './components/AddCategory/AddCategoryPopUp';
import { getUser } from './hooks/Auth/getUser';
import { CostsPage } from './components/Costs/CostsPage';

function App() {
  const { tokenValue } = useAuth()
  const [currentUser, setCurrentUser] = useState({})
  const [token, setToken] = useState(tokenValue)
  const [categories, setCategories] = useState([])

  useEffect(() => {
    getUser(token).then((user) => {
      if (!user) {
        setToken("")
      } else {
        setCurrentUser(user)
      }
    })
  }, [])

  return (
    <>
      <Routes>
        <Route path="/" element={
          token ? <CategoriesPage token={token} categories={categories} user={currentUser} /> : <Navigate to="/login" />
        } />
        <Route path="/add_category" element={
          token ? (<><CategoriesPage token={token} categories={categories} user={currentUser} /><AddCategoryPopUp token={token} setCategories={setCategories} /></>) : <Navigate to="/login" />
        } />
        <Route path="/cards" element={
          token ? <CardsPage token={token} /> : <Navigate to="/login" />
        } />
        <Route path="/costs" element={
          token ? <CostsPage token={token} user={currentUser} /> : <Navigate to="/login" />
        } />
        <Route path="/login" element={<LoginPage token={token} setToken={setToken} />} />
      </Routes>
    </>
  )
}

export default App;
