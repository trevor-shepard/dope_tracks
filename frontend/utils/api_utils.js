import axios from 'axios';

axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";


export const requestUserHistory = (start) => (
    axios.get(`/api/history?start=${start}`)
)

export const requestUserStats = (days) => (
    axios.get(`/api/stats?days=${days}`)
)

