import React, {useEffect} from 'react';
import './App.css';
import MenuPage from "./components/MenuPage/MenuPage";
import {Route, Routes} from "react-router-dom";
import {useTelegram} from "./hooks/useTelegram";
import Wrapper from "./components/Wrapper/Wrapper";
import Auto from "./components/Auto/Auto";
import ReferralPage from "./components/ReferralPage/ReferralPage";
import Location from "./components/Location/Location";

function App() {
    const {tg, showBackButton, toBack, onClose} = useTelegram()
    useEffect(() => {
        tg.ready();
        showBackButton(() => {
            if(window.location.pathname === '/')
                onClose();
            else
                toBack();
        });
    }, [])

    return (
        <div className="App">
            <Wrapper>
                <Routes>
                    <Route index element={<MenuPage/>}/>
                    <Route path='/auto' element={<Auto/>}/>
                    <Route path='/locations' element={<Location/>}/>
                    <Route path='/referral' element={<ReferralPage/>}/>
                </Routes>
            </Wrapper>
        </div>
    );
}

export default App;
