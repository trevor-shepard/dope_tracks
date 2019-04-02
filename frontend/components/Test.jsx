import React, { Component } from 'react'

import * as apiUtil from '../utils/api_utils';



class Test extends Component {
    constructor(props) {
        super(props)
        this.state = {}
    }

    sendRequest(apiRequest, params) {
        return () => {
            apiRequest(params)
            .then(() => {
                debugger
            })
        }
    }

    render() {
        let now = new Date()

        let yesterday = new Date(now.getFullYear(), now.getMonth(), now.getDay() - 1)
        
        return(
            <div>
                <h1>Actions</h1>
                <ul>
                    <li>
                        GET: /api/history <button onClick={this.sendRequest(apiUtil.requestUserHistory, yesterday.getTime())} >Send</button>
                    </li>
                </ul>
                <ul>
                    <li>
                        GET: /api/top <button onClick={this.sendRequest(apiUtil.requestUserStats, 1)} >Send</button>
                    </li>
                </ul>
            </div>
        )
    }
}

export default Test;