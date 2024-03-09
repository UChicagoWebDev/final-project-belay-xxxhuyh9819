import React, {useEffect, useState} from 'react';
import { useNavigate } from 'react-router-dom';
import './styles/home.css';
import TopBar from "./topBar";

function Home({LoginCredentials}) {

    const api_key = localStorage.getItem("yunhaohu_belay_api_key")
    let username = localStorage.getItem("user_name");

    const navigate = useNavigate()
    const [totalChannels, setTotalChannels] = useState(0);
    const [selectedChannel, setSelectedChannel] = useState(null);
    const [channels, setChannels] = useState([])
    const [channelName, setChannelName] = useState()

    const baseUrl = "http://127.0.0.1:5000"

    // src: https://stackoverflow.com/questions/63605682/reactjs-call-function-on-startup-of-application-with-a-functional-component
    useEffect(() => {
        getChannels();
        setInterval(()=>getChannels(), 1000);
    }, []);

    function getChannels() {
        fetch(baseUrl +'/api/channels', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        }).then(response => response.json())
            .then(data => {
                setChannels(data)
            }).catch(error => console.log(error))
    }

    function handleCreateChannel() {

    }


    return <div className="home">

        <TopBar LoginCredentials={LoginCredentials} username={username}/>

        <div className="main-content">
            {/*<ChannelsList numOfChannels={value => setTotalChannels(value)} currentChannel={value => setSelectedChannel(value)} />*/}
            {/*<ChannelDetails numOfChannels={totalChannels} selectedChannel={selectedChannel} />*/}
            <div className="channels-list">
                <div className="title_block">
                    <div className="title">
                        <h2>Channels</h2>
                        <button onClick={handleCreateChannel}>Create Channel</button>
                    </div>
                    <input type="text"
                           id="channel_name"
                           name="channel_name"
                           placeholder="Enter the new channel's name"
                           value={channelName}
                           onChange={(e) => {
                               setChannelName(e.target.value)
                           }}
                           required/>
                </div>
                <ul>
                    {channels.map((data) => {
                        return (
                            <li
                                key={data.id}
                                // onClick={() => handleSelectedChannel(data)}
                                className={selectedChannel !== null && data.id === selectedChannel.id ? "selected": "other"}>
                                {data.name}
                            </li>
                        )
                    })}
                </ul>

            </div>

        </div>


    </div>
}

export default Home