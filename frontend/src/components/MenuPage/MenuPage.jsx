import React from 'react';
import Header from "../semantics/Header/Header";
import Divider from "../Divider/Divider";
import Promo from "../Promo/Promo";

function MenuPage() {
    return (
        <div className="App-wrapper">
            <div className="padding-wrapper">
                <Header/>
                <Divider/>
                <Promo/>
            </div>
        </div>
    );
}

export default MenuPage;
