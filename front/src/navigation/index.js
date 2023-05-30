import { BrowserRouter, Route, Routes } from "react-router-dom";
import Home from "../pages/Home";
import Interacions from "../pages/Interactions";
import { NavBar } from "../components/NavBar";

const Navigation = () => {

    return (
        <BrowserRouter>
                <NavBar />
                <Routes>
                    <Route path="/" element={<Home />} />
                    <Route path="/Actions" element={<Interacions />} />
                </Routes>
        </BrowserRouter>
    )
}

export default Navigation;
