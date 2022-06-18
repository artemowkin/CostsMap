import { useEffect, useState } from 'react'
import { Routes, Route, Navigate, useNavigate } from 'react-router-dom'
import { CategoriesPage } from './components/Categories/CategoriesPage'
import { LoginPage } from './components/Login/LoginPage'
import { useAuth } from './hooks/Auth/useAuth'
import { CardsPage } from './components/Cards/CardsPage'
import { AddCategoryPopUp } from './components/AddCategory/AddCategoryPopUp'
import { getUser } from './hooks/Auth/getUser'
import { CostsPage } from './components/Costs/CostsPage'
import { AccountPage } from './components/Account/AccountPage'
import { AddCardPopUp } from './components/addCard/addCardPopUp'
import { CardMenu } from './components/CardMenu/CardMenu'
import { getUserCards } from './components/Cards/services'
import { getTotalCosts, getUserCategories } from './components/Categories/services'
import { AddCostPopUp } from './components/addCost/AddCostPopUp'

import './App.css'
import { getUserCosts } from './components/Costs/services'

function App() {
  const { tokenValue } = useAuth()
  const [currentUser, setCurrentUser] = useState({})
  const [token, setToken] = useState(tokenValue)
  const [categories, setCategories] = useState([])
  const [cards, setCards] = useState([])
  const [costs, setCosts] = useState([])
  const [monthCosts, setMonthCosts] = useState(0)

  const navigate = useNavigate();

  useEffect(() => {
    const userPromise = getUser(token)

    userPromise.then((user) => {
      if (!user) {
        setToken("")
      } else {
        setCurrentUser(user)
      }
    })

    userPromise.catch(() => {
      localStorage.clear()
      navigate("/login")
    })
  }, [token])

  useEffect(() => {
    getUserCards(token).then((cards) => setCards(cards))
    getUserCategories(token).then((categories) => setCategories(categories))
    getUserCosts(token).then((costs) => setCosts(costs))
    getTotalCosts(token).then((response) => setMonthCosts(response.total_costs))
  }, [token])

  return (
    <>
      <Routes>
        <Route path="/" element={
          token ? <CategoriesPage categories={categories} user={currentUser} monthCosts={monthCosts} /> : <Navigate to="/login" />
        } />
        <Route path="/add_category" element={
          token ? (<><CategoriesPage categories={categories} user={currentUser} monthCosts={monthCosts} /><AddCategoryPopUp token={token} setCategories={setCategories} /></>) : <Navigate to="/login" />
        } />
        <Route path="/add_cost/:categoryId" element={
          token ? (<><CategoriesPage categories={categories} user={currentUser} monthCosts={monthCosts} /><AddCostPopUp token={token} setCosts={setCosts} setCategories={setCategories} setMonthCosts={setMonthCosts} setCards={setCards} user={currentUser} categories={categories} cards={cards}/></>) : <Navigate to="/login" />
        } />
        <Route path="/cards" element={
          token ? <CardsPage token={token} cards={cards} /> : <Navigate to="/login" />
        } />
        <Route path="/add_card" element={
          token ? (<><CardsPage token={token} cards={cards} /><AddCardPopUp token={token} setCards={setCards} user={currentUser} /></>) : <Navigate to="/login" />
        } />
        <Route path="/card_menu/:cardId" element={
          token ? (<><CardsPage token={token} cards={cards} /><CardMenu token={token} setCards={setCards} /></>) : <Navigate to="/login" />
        } />
        <Route path="/costs" element={
          token ? <CostsPage costs={costs} /> : <Navigate to="/login" />
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
