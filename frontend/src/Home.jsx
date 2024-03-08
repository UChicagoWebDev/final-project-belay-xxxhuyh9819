import React, { useState } from 'react';
import {NavLink} from 'react-router-dom';
import './styles/home.css';
import TopBar from "./topBar";
// import TopBar from "../Components/TopBar";
// import ChannelsList from "../Components/ChannelsList";
// import ChannelDetails from "../Components/ChannelDetails";

function Home({LoginCredentials}) {

    let username = localStorage.getItem("user_name");
    const [totalChannels, setTotalChannels] = useState(0);
    const [selectedChannel, setSelectedChannel] = useState(null);


    // function handleLogOut() {
    //     if (window.confirm("Do you really want to leave?")) {
    //         localStorage.clear()
    //         LoginCredentials(null)
    //     }
    // }


    return <div className="home">

        <TopBar LoginCredentials={LoginCredentials} username={username}/>

        <div className="main-content">
            {/*<ChannelsList numOfChannels={value => setTotalChannels(value)} currentChannel={value => setSelectedChannel(value)} />*/}
            {/*<ChannelDetails numOfChannels={totalChannels} selectedChannel={selectedChannel} />*/}


        </div>
        <h1>Home</h1>

    </div>
}

export default Home