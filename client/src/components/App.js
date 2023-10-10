import React from "react";
// import { Switch, Route } from "react-router-dom";
import { Switch, Route } from "react-router-dom"
import About from './About'
import Login from './Login'
import MedicinePage from './MedicinePage'
import Header from './Header'
import Navbar from './Navbar'

function App() {
  return (
    <>
      <Header />
      <Navbar />
      <Switch>
        <Route exact path='/login'>
          <Login />
        </Route>
        <Route path='/about'>
          <About />
        </Route>
        <Route path='/medicinepage'>
          <MedicinePage />
        </Route>
      </Switch>
    </>
  )
}

export default App;
