import { NavLink } from "react-router-dom/cjs/react-router-dom.min"


function Navbar() {
    return (
        <div className="nav-container">
            <NavLink
                activeStyle={{ backgroundColor: '#7895CB' }}
                className='nav-btn nav-text'
                exact to='/about'>
                About
            </NavLink>
        </div>
    )
}

export default Navbar