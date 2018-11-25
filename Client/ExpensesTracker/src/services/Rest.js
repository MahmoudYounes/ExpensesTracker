import Vue from 'vue';
import VueResource from 'vue-resource'


Vue.use(VueResource)

var rootUrl = "http://localhost:5000";

export var userToken = "";

export const SetUserToken = function (token) {
    userToken = token;
}

export const SendGetRequest = function(route)
{
    Vue.http.headers.common['x-access-token'] = userToken;
    let requestUrl = rootUrl + route;
    return Vue.http.get(requestUrl) 
}

export const SendPostRequest = function(route, data)
{
    Vue.http.headers.common['x-access-token'] = userToken;
    let requestUrl = rootUrl + route;
    return Vue.http.post(requestUrl, data);
}

export const SendDeleteRequest = function(route)
{
    Vue.http.headers.common['x-access-token'] = userToken;
    let requestUrl = rootUrl + route;
    return Vue.http.delete(requestUrl)
}

export const SendPutRequest = function(route, data)
{
    Vue.http.headers.common['x-access-token'] = userToken;
    let requestUrl = rootUrl + route;
    return Vue.http.put(requestUrl, data)
}