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
import { AccountPage } from './components/Account/AccountPage';
import { AddCardPopUp } from './components/addCard/addCardPopUp';

function App() {
  const { tokenValue } = useAuth()
  const [currentUser, setCurrentUser] = useState({})
  const [token, setToken] = useState(tokenValue)
  const [categories, setCategories] = useState([])
  const [cards, setCards] = useState([])

  useEffect(() => {
    getUser(token).then((user) => {
      if (!user) {
        setToken("")
      } else {
        setCurrentUser(user)
      }
    })
  }, [token])

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
          token ? <CardsPage token={token} cards={cards} /> : <Navigate to="/login" />
        } />
        <Route path="/add_card" element={
          token ? (<><CardsPage token={token} /><AddCardPopUp token={token} setCards={setCards} user={currentUser} /></>) : <Navigate to="/login" />
        } />
        <Route path="/costs" element={
          token ? <CostsPage token={token} user={currentUser} /> : <Navigate to="/login" />
        } />
        <Route path="/account" element={
          token ? <AccountPage token={token} user={currentUser} /> : <Navigate to="/login" />
        } />
        <Route path="/login" element={<LoginPage token={token} setToken={setToken} />} />
      </Routes>
    </>
  )
}

export default App;
