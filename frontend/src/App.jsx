import { useState } from 'react'
import { BrowserRouter as Router ,Routes,Route} from 'react-router-dom'
import Home from './components/Home'
import Login from './components/Login'
import Signup from './components/Signup'
import Navbar from './components/Navbar'


function App() {
  const [count, setCount] = useState(0)

  return (
    <div className='container'>      
      <Router>
        <Navbar/>
        <Routes>
          <Route path="/" element={<Home/>} />
          <Route path="/login" element={<Login/>} />
          <Route path="/signup" element={<Signup/>} />
        </Routes>
      </Router>
    </div>
  )
}

export default App
