import { BrowserRouter, Route, Routes } from "react-router-dom";
import Home from "../pages/Home";
import Interacions from "../pages/Interactions";
import Progress from "../pages/Progress";
import Status from "../pages/Status";
import { NavBar } from "../components/NavBar";

const Navigation = () => {

    return (
        <BrowserRouter>
                <NavBar />
                <Routes>
                    <Route path="/" element={<Home />} />
                    <Route path="/Actions" element={<Interacions />} />
                    <Route path="/Progress" element={<Progress />} />
                    <Route path="/Status" element={<Status/>} />
                </Routes>
        </BrowserRouter>
    )
}

export default Navigation;
